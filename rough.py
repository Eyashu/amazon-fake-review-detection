import os
import json
from typing import List, Optional
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

# --- Configuration ---

# Load API key from .env file
load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# The Amazon product URL you want to scrape
AMAZON_PRODUCT_URL = "https://www.amazon.in/CartaDen-Wooden-Serving-Modern-Breakfast/dp/B0BFBV4JKK/?encoding=UTF8&pd_rd_w=nqYiJ&content-id=amzn1.sym.dceab7e0-54de-407b-ad1f-7d5f79fffeeb&pf_rd_p=dceab7e0-54de-407b-ad1f-7d5f79fffeeb&pf_rd_r=PVBZRQ4KXDHA5HYGRY3G&pd_rd_wg=q0GXh&pd_rd_r=9ca92f76-b7f1-4b4b-9823-19faffc7febb&ref=pd_hp_d_btf_kar_gw_pc_en_&th=1"

# Output text file name (relative to script location)
OUTPUT_FILE_NAME = "amazon_product_data.txt"
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the full path for the output file
OUTPUT_FILE_PATH = os.path.join(SCRIPT_DIR, OUTPUT_FILE_NAME)

# Headers to mimic a browser for direct requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
}

# --- Data Structure Definitions ---

class ReviewItem(BaseModel):
    reviewer_name: Optional[str] = Field(None, description="Name of the person who wrote the review")
    rating: Optional[str] = Field(None, description="Rating given by the reviewer (e.g., '5.0 out of 5 stars')")
    review_title: Optional[str] = Field(None, description="Title of the review")
    review_text: Optional[str] = Field(None, description="The main text content of the review")
    review_date: Optional[str] = Field(None, description="Date the review was posted")
    is_verified_purchase: Optional[bool] = Field(None, description="Whether the purchase is marked as verified")

class ProductInfo(BaseModel):
    product_name: Optional[str] = Field(None, description="The main name or title of the product")
    description: Optional[str] = Field(None, description="The detailed description text of the product")
    features: Optional[List[str]] = Field(None, description="List of key features or bullet points")
    average_rating: Optional[str] = Field(None, description="The overall average star rating for the product")
    total_ratings_count: Optional[str] = Field(None, description="The total number of ratings the product has received")
    price: Optional[str] = Field(None, description="The current price of the product")
    reviews: Optional[List[ReviewItem]] = Field(None, description="A list of customer reviews found on the page")

# --- Scraping Functions ---

def scrape_amazon_product_with_firecrawl(api_key: str, url: str) -> Optional[dict]:
    """Attempts to scrape using Firecrawl API."""
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found. Please set it in your .env file.")
        return None

    print(f"Initializing FirecrawlApp...")
    try:
        app = FirecrawlApp(api_key=api_key)
    except Exception as e:
        print(f"Error initializing FirecrawlApp: {e}")
        return None

    print(f"Attempting to scrape URL with Firecrawl: {url}")
    try:
        response = app.scrape_url(url=url)
        print(f"Response type: {type(response)}")
        
        # Try to extract HTML content for direct parsing
        html_content = None
        if hasattr(response, 'content'):
            html_content = response.content
        elif hasattr(response, 'html'):
            html_content = response.html
        
        # Return the HTML content if found
        if html_content:
            return {"html_content": html_content}
        else:
            print("No HTML content found in Firecrawl response")
            return None
            
    except Exception as e:
        print(f"Error with Firecrawl: {e}")
        return None

def scrape_amazon_directly(url: str) -> Optional[str]:
    """Scrapes the Amazon page directly using requests and returns the HTML."""
    print(f"Attempting to scrape URL directly: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve page: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error making direct request: {e}")
        return None

def parse_amazon_html(html: str) -> dict:
    """Parses Amazon product HTML and extracts structured information."""
    product_info = {}
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract product name
    try:
        product_name_elem = soup.select_one('#productTitle')
        if product_name_elem:
            product_info['product_name'] = product_name_elem.text.strip()
    except Exception as e:
        print(f"Error extracting product name: {e}")
    
    # Extract price
    try:
        price_whole = soup.select_one('.a-price-whole')
        price_fraction = soup.select_one('.a-price-fraction')
        price_symbol = soup.select_one('.a-price-symbol')
        
        if price_whole and price_fraction and price_symbol:
            price = f"{price_symbol.text}{price_whole.text}{price_fraction.text}"
            product_info['price'] = price
    except Exception as e:
        print(f"Error extracting price: {e}")
    
    # Extract rating
    try:
        rating_elem = soup.select_one('#acrPopover')
        if rating_elem and 'title' in rating_elem.attrs:
            product_info['average_rating'] = rating_elem['title']
            
        ratings_count_elem = soup.select_one('#acrCustomerReviewText')
        if ratings_count_elem:
            product_info['total_ratings_count'] = ratings_count_elem.text.strip()
    except Exception as e:
        print(f"Error extracting rating: {e}")
    
    # Extract features
    try:
        feature_bullets = soup.select('#feature-bullets ul li')
        if feature_bullets:
            product_info['features'] = [bullet.text.strip() for bullet in feature_bullets]
    except Exception as e:
        print(f"Error extracting features: {e}")
    
    # Extract description
    try:
        description_elem = soup.select_one('#productDescription')
        if description_elem:
            product_info['description'] = description_elem.text.strip()
    except Exception as e:
        print(f"Error extracting description: {e}")
    
    # Extract reviews
    try:
        reviews = []
        review_elements = soup.select('#cm-cr-dp-review-list .review')
        
        for review_elem in review_elements:
            review = {}
            
            # Reviewer name
            name_elem = review_elem.select_one('.a-profile-name')
            if name_elem:
                review['reviewer_name'] = name_elem.text.strip()
            
            # Rating
            rating_elem = review_elem.select_one('i.review-rating')
            if rating_elem:
                review['rating'] = rating_elem.text.strip()
            
            # Review title
            title_elem = review_elem.select_one('.review-title')
            if title_elem:
                review['review_title'] = title_elem.text.strip()
            
            # Review text
            text_elem = review_elem.select_one('.review-text')
            if text_elem:
                review['review_text'] = text_elem.text.strip()
            
            # Review date
            date_elem = review_elem.select_one('.review-date')
            if date_elem:
                review['review_date'] = date_elem.text.strip()
            
            # Verified purchase
            verified_elem = review_elem.select_one('.a-color-state')
            if verified_elem and 'verified' in verified_elem.text.lower():
                review['is_verified_purchase'] = True
            else:
                review['is_verified_purchase'] = False
            
            reviews.append(review)
        
        if reviews:
            product_info['reviews'] = reviews
    except Exception as e:
        print(f"Error extracting reviews: {e}")
    
    return product_info

def format_data_as_text(data: dict) -> str:
    """Formats the extracted data as readable text."""
    text_output = []
    
    # Try to format based on our structure
    try:
        # Product information
        if 'product_name' in data and data['product_name']:
            text_output.append(f"PRODUCT NAME: {data['product_name']}")
        if 'price' in data and data['price']:
            text_output.append(f"PRICE: {data['price']}")
        if 'average_rating' in data and data['average_rating']:
            text_output.append(f"RATING: {data['average_rating']}")
        if 'total_ratings_count' in data and data['total_ratings_count']:
            text_output.append(f"TOTAL RATINGS: {data['total_ratings_count']}")
        
        # Features
        if 'features' in data and data['features']:
            text_output.append("\nFEATURES:")
            for i, feature in enumerate(data['features'], 1):
                text_output.append(f"{i}. {feature}")
        
        # Description
        if 'description' in data and data['description']:
            text_output.append("\nDESCRIPTION:")
            text_output.append(data['description'])
        
        # Reviews
        if 'reviews' in data and data['reviews']:
            text_output.append("\nREVIEWS:")
            for i, review in enumerate(data['reviews'], 1):
                text_output.append(f"\nReview #{i}:")
                if 'reviewer_name' in review and review['reviewer_name']:
                    text_output.append(f"Reviewer: {review['reviewer_name']}")
                if 'rating' in review and review['rating']:
                    text_output.append(f"Rating: {review['rating']}")
                if 'review_date' in review and review['review_date']:
                    text_output.append(f"Date: {review['review_date']}")
                if 'review_title' in review and review['review_title']:
                    text_output.append(f"Title: {review['review_title']}")
                if 'review_text' in review and review['review_text']:
                    text_output.append(f"Review: {review['review_text']}")
                if 'is_verified_purchase' in review:
                    text_output.append(f"Verified Purchase: {'Yes' if review['is_verified_purchase'] else 'No'}")
        
        # If we have no data
        if len(text_output) == 0:
            text_output.append("No product data could be extracted.")
        
    except Exception as e:
        text_output.append(f"Error formatting data: {e}")
        text_output.append(str(data))
    
    return "\n".join(text_output)

def save_to_text_file(formatted_text: str, full_filepath: str):
    """Saves formatted text to the specified full file path."""
    print(f"Saving extracted data to {full_filepath}...")
    try:
        # Use the full filepath provided
        with open(full_filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print("Data successfully saved to text file.")
    except IOError as e:
        print(f"Error saving data to text file: {e}")
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred during file saving: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Try Firecrawl first
    firecrawl_result = scrape_amazon_product_with_firecrawl(FIRECRAWL_API_KEY, AMAZON_PRODUCT_URL)
    
    html_content = None
    
    # If Firecrawl returned HTML content
    if firecrawl_result and 'html_content' in firecrawl_result:
        html_content = firecrawl_result['html_content']
        print("Using HTML content from Firecrawl")
    
    # If no HTML from Firecrawl, try direct scraping
    if not html_content:
        print("Falling back to direct scraping...")
        html_content = scrape_amazon_directly(AMAZON_PRODUCT_URL)
    
    # If we have HTML content, parse it
    if html_content:
        print("Parsing HTML content...")
        product_data = parse_amazon_html(html_content)
        
        # Format and save the data
        if product_data:
            formatted_text = format_data_as_text(product_data)
            # Pass the full path to the save function
            save_to_text_file(formatted_text, OUTPUT_FILE_PATH)
        else:
            print("Failed to extract product data from HTML.")
    else:
        print("Failed to retrieve HTML content from any source.")