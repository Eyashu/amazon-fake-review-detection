from flask import Flask, request, jsonify, send_from_directory  # Import send_from_directory
import re
import json
from flask_cors import CORS  # Required for handling requests from the frontend
import os  # Import os to construct path and get API key
import google.generativeai as genai  # Import Gemini library
from dotenv import load_dotenv  # Optional: To load .env file for API key

# Import necessary functions and constants from rough.py
try:
    from rough import (
        scrape_amazon_product_with_firecrawl,
        scrape_amazon_directly,
        parse_amazon_html,
        HEADERS  # Import HEADERS constant
    )
    print("Successfully imported functions from rough.py")
except ImportError as e:
    print(f"Error importing from rough.py: {e}. Make sure rough.py is in the same directory.")
    def scrape_amazon_product_with_firecrawl(*args, **kwargs): return None
    def scrape_amazon_directly(*args, **kwargs): return None
    def parse_amazon_html(*args, **kwargs): return {}
    HEADERS = {}  # Define empty HEADERS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- Configure Gemini API ---
try:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=google_api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')  # changed model from Gemini 2.0 to Gemini 1.5 flash latest
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    gemini_model = None

# --- Helper function to extract product ID ---
def extract_product_id(url):
    match_dp = re.search(r'/dp/([A-Z0-9]{10})', url)
    if match_dp:
        return match_dp.group(1)

    match_reviews = re.search(r'/product-reviews/([A-Z0-9]{10})', url)
    if match_reviews:
        return match_reviews.group(1)

    return None

# --- Flask Route to handle review analysis ---
@app.route('/analyze_reviews', methods=['POST'])
def analyze_reviews():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured. Check server logs."}), 500

    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_api_key:
        print("Warning: FIRECRAWL_API_KEY not found in environment. Firecrawl scraping will be skipped.")

    data = request.form
    product_url = data.get('product_url')

    if not product_url:
        return jsonify({"error": "No product_url provided"}), 400

    product_id = extract_product_id(product_url)

    if not product_id:
        if '/product-reviews/' in product_url:
            match_reviews_direct = re.search(r'/product-reviews/([A-Z0-9]{10})', product_url)
            if match_reviews_direct:
                product_id = match_reviews_direct.group(1)
        if not product_id:
            return jsonify({"error": "Could not extract product ID from URL"}), 400

    reviews_url = f"https://www.amazon.in/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    product_page_url = f"https://www.amazon.in/dp/{product_id}"

    product_html_content = None
    reviews_html_content = None

    print(f"Getting product page HTML: {product_page_url}")
    if firecrawl_api_key:
        fc_result = scrape_amazon_product_with_firecrawl(firecrawl_api_key, product_page_url)
        if fc_result and 'html_content' in fc_result:
            product_html_content = fc_result['html_content']
            print("Using Firecrawl HTML for product page.")
    if not product_html_content:
        print("Falling back to direct request for product page.")
        product_html_content = scrape_amazon_directly(product_page_url)

    print(f"Getting reviews page HTML: {reviews_url}")
    if firecrawl_api_key:
        fc_result = scrape_amazon_product_with_firecrawl(firecrawl_api_key, reviews_url)
        if fc_result and 'html_content' in fc_result:
            reviews_html_content = fc_result['html_content']
            print("Using Firecrawl HTML for reviews page.")
    if not reviews_html_content:
        print("Falling back to direct request for reviews page.")
        reviews_html_content = scrape_amazon_directly(reviews_url)

    product_parsed_data = {}
    reviews_parsed_data = {}

    if product_html_content:
        print("Parsing product page HTML...")
        product_parsed_data = parse_amazon_html(product_html_content)
    else:
        print("Failed to get product page HTML.")

    if reviews_html_content:
        print("Parsing reviews page HTML...")
        reviews_parsed_data = parse_amazon_html(reviews_html_content)
    else:
        print("Failed to get reviews page HTML.")

    product_info = {
        "title": product_parsed_data.get("product_name", "N/A"),
        "price": product_parsed_data.get("price", "N/A")
    }

    raw_reviews = reviews_parsed_data.get("reviews", [])
    if not raw_reviews:
        raw_reviews = product_parsed_data.get("reviews", [])
        if raw_reviews:
            print("Used reviews found on the main product page.")

    reviews_data = []
    for raw_review in raw_reviews:
        mapped_review = {
            "username": raw_review.get("reviewer_name", "N/A"),
            "timestamp": "N/A",
            "rating": "N/A",
            "review_text": raw_review.get("review_text", "")
        }

        raw_date = raw_review.get("review_date", "N/A")
        if raw_date != 'N/A':
            date_match = re.search(r'on\s+(.*)', raw_date)
            mapped_review["timestamp"] = date_match.group(1).strip() if date_match else raw_date

        raw_rating = raw_review.get("rating", "N/A")
        if raw_rating != 'N/A':
            rating_match = re.match(r'(\d+\.?\d*)', raw_rating)
            mapped_review["rating"] = rating_match.group(1) if rating_match else raw_rating

        if mapped_review['username'] != 'N/A' and mapped_review['review_text'] != '' and mapped_review['rating'] != 'N/A':
            reviews_data.append(mapped_review)

    if not reviews_data and product_info.get('title', 'N/A') == 'N/A':
        error_msg = "Could not scrape/parse product information or reviews."
        details = "Check server logs for errors from rough.py functions."
        return jsonify({"error": error_msg, "details": details}), 404
    elif not reviews_data:
        print("Warning: Product info retrieved, but no reviews found or parsed.")
        pass

    MAX_REVIEWS_FOR_GEMINI = 50
    reviews_to_analyze = reviews_data[:MAX_REVIEWS_FOR_GEMINI]

    prompt_reviews = []
    for i, review in enumerate(reviews_to_analyze):
        prompt_reviews.append({
            "id": i,
            "username": review.get('username', 'N/A'),
            "timestamp": review.get('timestamp', 'N/A'),
            "rating": review.get('rating', 'N/A'),
            "review_text": review.get('review_text', '')
        })

    prompt = f"""
Analyze the following Amazon product reviews for the product titled "{product_info.get('title', 'Unknown Product')}".
For each review, determine if it seems like a "fake" review or a "real" review based on its content, language, rating, and context. Consider factors like overly positive/negative generic language, mentions of incentives, suspicious patterns, or lack of specific detail.

Reviews:
{json.dumps(prompt_reviews, indent=2)}

Please provide your analysis ONLY in the following JSON format: A list of objects, where each object corresponds to a review in the input list (use the 'id' field for mapping). Each object must contain the 'id' and a field 'classification' which should be either the string "fake" or the string "real".

Example Output Format:
[
  {{ "id": 0, "classification": "real" }},
  {{ "id": 1, "classification": "fake" }},
  ...
]

Provide ONLY the JSON list as your response.
"""

    report_data = []
    try:
        print(f"Sending {len(prompt_reviews)} reviews to Gemini...")
        if not prompt_reviews:
            print("No reviews extracted/mapped to send to Gemini.")
            return jsonify({
                "product_info": product_info,
                "review_report": [],
                "message": "Product info retrieved, but no reviews could be successfully parsed/mapped for analysis."
            })

        response = gemini_model.generate_content(prompt)

        response_text = response.text.strip()
        json_match = re.search(r'```json\s*(\[.*?\])\s*```|(\[.*?\])', response_text, re.DOTALL | re.IGNORECASE)

        if json_match:
            json_string = json_match.group(1) if json_match.group(1) else json_match.group(2)
            try:
                gemini_results = json.loads(json_string)
                if not isinstance(gemini_results, list):
                    raise json.JSONDecodeError("Expected a JSON list", json_string, 0)

                results_map = {result['id']: result['classification'] for result in gemini_results if isinstance(result, dict) and 'id' in result and 'classification' in result}

                for i, review in enumerate(reviews_to_analyze):
                    classification = results_map.get(i, "error")
                    if classification not in ["real", "fake"]:
                        print(f"Warning: Unexpected classification '{classification}' for review ID {i}. Defaulting to 'error'.")
                        classification = "error"
                    report_data.append({
                        "username": review.get('username', 'N/A'),
                        "timestamp": review.get('timestamp', 'N/A'),
                        "classification": classification  # changed output field
                    })
                print("Successfully processed Gemini response.")

            except json.JSONDecodeError as json_e:
                print(f"Error decoding JSON response from Gemini: {json_e}")
                print(f"Attempted to parse JSON string:\n{json_string}")
                print(f"Original Gemini response text:\n{response.text}")
                return jsonify({"error": "Failed to parse Gemini response (JSON decode error)"}), 500
        else:
            print("Error: Could not find valid JSON list in Gemini response.")
            print(f"Raw Gemini response text:\n{response.text}")
            return jsonify({"error": "Failed to parse Gemini response (JSON structure not found)"}), 500

    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        try:
            if 'response' in locals() and hasattr(response, 'prompt_feedback'):
                print(f"Gemini Safety Feedback: {response.prompt_feedback}")
        except Exception as feedback_e:
            print(f"Could not retrieve Gemini safety feedback: {feedback_e}")
        return jsonify({"error": f"Gemini API request failed: {e}"}), 500

    if len(reviews_data) > MAX_REVIEWS_FOR_GEMINI:
        for review in reviews_data[MAX_REVIEWS_FOR_GEMINI:]:
            report_data.append({
                "username": review.get('username', 'N/A'),
                "timestamp": review.get('timestamp', 'N/A'),
                "classification": "not_analyzed"  # changed output field
            })

    response_data = {
        "product_info": product_info,
        "review_report": report_data
    }

    return jsonify(response_data)

# --- Route to serve the index.html file ---
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
