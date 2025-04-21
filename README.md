# Amazon Fake Review Detection

An AI-powered application to analyze and classify Amazon product reviews as potentially "fake" or "real".

## Description

This project provides a web-based tool for identifying potentially inauthentic reviews on Amazon product pages. Leveraging advanced web scraping techniques and sophisticated natural language processing powered by Google's Gemini API, the application extracts product and review data from a given Amazon URL. It then analyzes the sentiment, linguistic patterns, and characteristics of individual reviews to determine their likelihood of being fake based on the AI model's assessment. The goal is to help users make more informed purchasing decisions by highlighting reviews that may be misleading.

The application presents the analysis results through a user-friendly web interface, making it easy to input Amazon links and visualize which reviews are flagged as potentially fake. It also exposes a programmatic API endpoint for integration into other systems.

The backend is built using the lightweight Python Flask web framework, while the frontend utilizes standard HTML, CSS, and JavaScript for a dynamic user experience. Essential configuration details, such as API keys, are managed securely using environment variables loaded from a `.env` file.

## Features

*   **Web Scraping:** Automatically extracts essential product information (title, price, etc.) and comprehensive review data from Amazon product URLs.
*   **AI-Powered Analysis:** Classifies individual reviews as "fake" or "real" using the cutting-edge capabilities of the Google Gemini API.
*   **User Interface:** Provides an intuitive web interface where users can paste an Amazon link and view the analysis results presented clearly, with distinct indicators for review classification.
*   **API Endpoint:** Offers a dedicated `/analyze_reviews` endpoint allowing programmatic submission of URLs and retrieval of analysis results in JSON format.
*   **Environment Configuration:** Securely loads sensitive configuration (like API keys) from environment variables, typically managed via a local `.env` file.
*   **Dependency Management:** Uses `requirements.txt` for easy installation and management of all necessary Python libraries.
*   **Error Handling:** Includes basic error handling for issues like invalid URLs or API communication problems.

## Technologies Used

The project utilizes the following key technologies and libraries:

*   **Python 3.x:** The core programming language used for the backend logic, data processing, and API interactions.
*   **Flask:** A minimalist Python web framework that handles routing, request processing, and serving the web interface.
*   **Google Generative AI (Gemini API):** Provides access to the powerful Gemini models (`gemini-1.5-flash-latest` is currently used) for performing the AI-driven classification of review text.
*   **Firecrawl API:** Employed for robust and efficient web scraping of Amazon product and review pages, converting web content into structured data.
*   **BeautifulSoup 4 (`bs4`):** A Python library used for parsing HTML and XML documents. It might be used in conjunction with Firecrawl or as a fallback method for extracting specific data points from the scraped HTML.
*   **Requests:** A widely used Python library for making HTTP requests, used here for interacting with external APIs like Firecrawl and potentially for direct web scraping if needed.
*   **Python-dotenv:** A library specifically designed to load environment variables from a `.env` file into the application's environment, facilitating secure handling of API keys and other configuration.
*   **HTML, CSS, JavaScript:** Standard frontend technologies used to build the interactive user interface (`index.html`), handle user input, make asynchronous requests to the backend, and dynamically display the analysis results.

## Project Structure

The project is organized into a logical structure to separate different concerns:
amazon-fake-review-detection/
├── app.py # Main backend Flask application file
├── requirements.txt # Lists all Python dependencies
├── .env.example # Example file showing required environment variables (SAFE TO COMMIT)
├── .env # Your local configuration file with actual secrets (IGNORED BY GIT)
├── .gitignore # Specifies files/directories to be ignored by Git (.env, pycache, etc.)
├── templates/ # Directory containing HTML template files served by Flask
│ └── index.html # The main HTML file for the web interface
└── rough.py # Standalone utility/test script for scraping and parsing logic (OPTIONAL, NOT USED BY APP)

*   `app.py`: Contains the primary Flask application instance. It defines the URL routes (`/`, `/analyze_reviews`), handles incoming requests from the web interface or API calls, orchestrates the scraping and AI analysis process, and renders the `index.html` template.
*   `requirements.txt`: A comprehensive list of all Python libraries and their specific versions required to run the project. Used with `pip install -r` for easy setup.
*   `.env.example`: Provides a clear template showing the names of the environment variables that need to be set up (e.g., `GOOGLE_API_KEY`, `FIRECRAWL_API_KEY`). It contains placeholder values and is safe to include in the repository.
*   `.env`: This file is **created locally by the user** by copying `.env.example` and contains their actual, sensitive API keys and configuration values. It is explicitly listed in `.gitignore` and is **never committed to the repository**.
*   `.gitignore`: A crucial file that tells Git which files and directories to ignore, preventing sensitive data (`.env`) and temporary files (`__pycache__`, etc.) from being included in the version history on GitHub.
*   `templates/`: The standard directory used by Flask to store HTML template files.
*   `templates/index.html`: The main HTML file that defines the structure, layout, and interactive elements of the web page. It includes JavaScript code to communicate with the backend and display the analysis results dynamically.
*   `rough.py`: (Optional) Based on your description, this file appears to be a standalone script containing code for developing or testing the scraping and parsing logic in isolation, perhaps with a hardcoded URL. The main application (`app.py`) likely uses similar functions, but `rough.py` itself is not typically needed for the Flask app to run. It can be kept in the repository as a utility or example script.

## Setup and Installation

To get this project up and running on your local machine, follow these detailed steps:

1.  **Prerequisites:**
    *   Ensure you have **Python 3.7+** and `pip` (Python's package installer) installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).
    *   You will need to obtain API keys for **Google Gemini** and **Firecrawl**.

2.  **Clone the repository:**
    Open your terminal or command prompt and clone the project repository from GitHub:
    ```bash
    git clone https://github.com/YourUsername/amazon-fake-review-detection.git
    cd amazon-fake-review-detection
    ```
    *(Replace `YourUsername/amazon-fake-review-detection.git` with the actual path to your repository if it's different.)*

3.  **Create a Virtual Environment (Highly Recommended):**
    It is standard practice to use a virtual environment to isolate the project's dependencies and avoid conflicts with other Python projects or your system's Python installation.
    ```bash
    # On macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate

    # On Windows:
    python -m venv venv
    venv\Scripts\activate
    ```
    *(You should see `(venv)` or similar at the beginning of your terminal prompt when the virtual environment is active. Remember to activate it in each new terminal session you use for the project.)*

4.  **Install Dependencies:**
    With your virtual environment activated, install the required Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    This command reads the `requirements.txt` file and installs all listed libraries (like Flask, google-generative-ai, firecrawl-python, python-dotenv, beautifulsoup4, requests) into your virtual environment.

5.  **Configuration (Environment Variables):**
    This project requires API keys to access the Google Gemini and Firecrawl services. These keys must be stored securely using environment variables and *not* hardcoded into any scripts that are committed to Git.

    *   Locate the `.env.example` file in the root directory of the project.
    *   **Copy** this file and rename the copy to `.env`.
        ```bash
        # On macOS/Linux:
        cp .env.example .env

        # On Windows:
        copy .env.example .env
        ```
    *   Open the newly created `.env` file in a text editor.
    *   Replace the placeholder values (e.g., `YOUR_GOOGLE_API_KEY_HERE`) with your actual, obtained API keys.
        ```
        # Example .env file content (after you've edited it)
        GOOGLE_API_KEY=AIzaSyA...YourActualGoogleAPIKey...XyZ
        FIRECRAWL_API_KEY=fc-a1b2c3d4e5f6...YourActualFirecrawlAPIKey...7890
        ```
    *   Save the `.env` file.
    *   **Security Note:** Your `.env` file contains sensitive information. The `.gitignore` file is configured to prevent this file from being committed to the repository. **Ensure you never manually add or commit your `.env` file.**

## Usage

Once the setup is complete and your virtual environment is active, you can run the Flask application:

1.  **Activate Virtual Environment** (if not already active):
    ```bash
    # On macOS/Linux:
    source venv/bin/activate

    # On Windows:
    venv\Scripts\activate
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    Flask will start a local development server. You should see output indicating the server is running, typically on `http://127.0.0.1:5000/`.
    ```
     * Serving Flask app 'app'
     * Debug mode: off
     WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

3.  **Access the Web Interface:**
    Open your web browser and navigate to the address displayed in the terminal (usually `http://127.0.0.1:5000/`). You should see the project's homepage with an input field where you can paste an Amazon product URL for analysis.

4.  **Using the API Endpoint:**
    You can also interact with the application programmatically via the `/analyze_reviews` endpoint using a POST request. This is useful for integrating the functionality into other scripts or applications.

    *   **URL:** `http://127.0.0.1:5000/analyze_reviews` (When running locally)
    *   **Method:** `POST`
    *   **Request Body (JSON):** The request body should be a JSON object containing a single key, `"url"`, with the Amazon product URL as its value.
        ```json
        {
          "url": "https://www.amazon.in/dp/YOUR_PRODUCT_ASIN/"
        }
        ```
    *   **Response (JSON):** The endpoint will return a JSON response containing the analysis results. The exact structure depends on the backend implementation but typically includes product details and a list of reviews, each with its text and a `"classification"` property (e.g., `"REAL"` or `"FAKE"`).
        ```json
        {
          "product_title": "Example Product Name",
          "product_price": "$XX.XX",
          "reviews": [
            {
              "text": "This is a review...",
              "classification": "REAL"
            },
            {
              "text": "Another review...",
              "classification": "FAKE"
            },
            // ... more reviews
          ]
        }
        ```

## Notes and Limitations

*   **Amazon.in Specific:** The current implementation is primarily tested and configured to work with **Amazon India (.in)** URLs due to potential differences in website structure across Amazon domains. Functionality with other Amazon domains (.com, .co.uk, etc.) is not guaranteed without modifications.
*   **Gemini Model Version:** The application uses the `gemini-1.5-flash-latest` model for classification. The accuracy of fake review detection is dependent on the capabilities and current version of this model.
*   **Review Processing Limit:** To manage API costs and processing time, the application may process a limited number of reviews per product URL (e.g., a maximum of 50 reviews sent to Gemini per request, as noted previously).
*   **AI Accuracy:** Detecting fake reviews is an inherently complex task. The AI's classification is an analysis based on patterns and probabilities and should be considered an indicator or a tool to aid human judgment, not a definitive proof of authenticity or inauthenticity.
*   **Scraping Reliability:** Web scraping can be fragile due to website structure changes. While Firecrawl is robust, changes to Amazon's site layout could potentially affect scraping accuracy.

## Contributing

Contributions to this project are welcome! If you would like to improve the application, add features, or fix bugs, please follow these steps:

1.  Fork the repository on GitHub.
2.  Create a new branch for your contribution (`git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix`).
3.  Implement your changes, ensuring adherence to standard Python practices and including necessary documentation or comments.
4.  Test your changes thoroughly.
5.  Commit your changes with clear and descriptive commit messages.
6.  Push your branch to your forked repository (`git push origin feature/your-feature-name`).
7.  Open a Pull Request from your branch to the main branch of this repository on GitHub, describing the changes you have made.

## License

This project is licensed under the MIT License. You can find the full text of the license in the `LICENSE` file in the root of the repository.

---

*(This README provides detailed information for the project based on the provided files and discussed architecture: `app.py`, `requirements.txt`, `templates/index.html`, `.env.example`, `.env` [ignored], `rough.py` [utility].)*
