# Amazon Fake Review Detection

An AI-powered application to analyze and classify Amazon product reviews as potentially "fake" or "real".

## Description

This project provides a user-friendly, web-based tool designed to assist in identifying potentially inauthentic reviews on Amazon product pages. Leveraging a combination of advanced web scraping techniques and sophisticated natural language processing powered by Google's Gemini API, the application extracts detailed product information and customer reviews from any given Amazon product URL. It then analyzes the characteristics, sentiment, and linguistic patterns of each individual review to assess its likelihood of being fake based on the AI model's classification.

The primary goal is to provide users with more transparency when evaluating product credibility, helping them make better purchasing decisions by highlighting reviews that may be misleading or fraudulent.

The application consists of a robust backend built with the lightweight Python Flask web framework, responsible for handling the core logic: receiving user requests, managing data extraction, interacting with external AI and scraping APIs, and processing the results. The frontend, developed using standard HTML, CSS, and JavaScript, offers an intuitive interface for users to input Amazon links and dynamically displays the analysis results in a clear, easy-to-understand format. Sensitive configuration details, such as API keys required for external services, are managed securely using environment variables loaded from a `.env` file.

## Features

*   **Automated Web Scraping:** Efficiently extracts essential product information (like title, price, average rating, total ratings count) and comprehensive review data (reviewer name, rating, title, text, date, verified purchase status) directly from Amazon product pages.
*   **AI-Powered Review Classification:** Utilizes the capabilities of the Google Gemini API (`gemini-1.5-flash-latest` model) to analyze review text and classify each review as either "REAL" or "FAKE" based on AI-driven patterns and analysis.
*   **Interactive Web Interface:** Provides an easy-to-use single-page web application where users can simply paste an Amazon product URL and trigger the analysis, viewing results directly in their browser with distinct visual cues for review classifications.
*   **Programmatic API Endpoint:** Exposes a dedicated `/analyze_reviews` endpoint allowing external scripts or applications to submit Amazon URLs via a POST request and receive structured analysis results in JSON format.
*   **Secure Configuration:** Manages sensitive API keys and other configuration details using environment variables loaded from a `.env` file, keeping secrets out of the codebase and version control.
*   **Dependency Management:** Uses a `requirements.txt` file to list all necessary Python libraries and their versions, enabling straightforward and reproducible installation of the project's dependencies.
*   **Basic Error Handling:** Includes mechanisms to catch common errors such as invalid URLs, issues during scraping, or problems with API communication, providing feedback to the user or logging details.

## Technologies Used

The project leverages the following key technologies and libraries to deliver its functionality:

*   **Python 3.7+:** The foundational programming language for all backend development, scripting, and data processing.
*   **Flask:** A minimalist Python web framework that provides the structure for the backend application, handling URL routing, processing HTTP requests, and serving the frontend template.
*   **Google Generative AI (`google-generativeai`):** The official Python client library for interacting with the Google Gemini API, specifically used here to send review text to the AI model for classification.
*   **Firecrawl (`firecrawl-py`):** A powerful web scraping API and its Python client library used for robustly and efficiently extracting structured data from Amazon product and review pages, handling complexities often encountered in modern websites.
*   **BeautifulSoup 4 (`bs4`):** A Python library for pulling data out of HTML and XML files. It may be used to further parse or refine data obtained from Firecrawl or for fallback direct scraping.
*   **Requests:** A popular Python library for making simple HTTP requests, used for communicating with external APIs and potentially for direct page fetches if Firecrawl is not used or fails.
*   **Python-dotenv (`python-dotenv`):** A Python library that reads key-value pairs from a `.env` file and sets them as environment variables, ensuring sensitive credentials are not hardcoded in the application.
*   **HTML, CSS, JavaScript:** Standard frontend web technologies used to build the interactive user interface (`index.html`), manage client-side logic, handle user input, send requests to the backend using Fetch API or XMLHttpRequest, and dynamically update the page content with analysis results.

## Project Structure

The project is organized into a clear and logical structure to separate different components and concerns:
```text
amazon-fake-review-detection/
├── app.py # Main backend Flask application file with routes and logic
├── requirements.txt # Lists all Python dependencies required for the project
├── .env.example # Example file showing required environment variables (SAFE TO COMMIT)
├── .env # Your local configuration file with actual secrets (IGNORED BY GIT)
├── .gitignore # Specifies files/directories to be ignored by Git (.env, pycache, etc.)
├── templates/ # Directory containing HTML template files served by Flask
│ └── index.html # The main HTML file for the web interface
└── rough.py # Standalone utility/test script for scraping and parsing logic (OPTIONAL - not used by app.py)
```

*   `app.py`: This file contains the core logic of the Flask application. It sets up the Flask server, defines the URL routes (like `/` to serve the homepage and `/analyze_reviews` for processing requests), handles incoming data from the user, calls functions to perform scraping and AI analysis, and formats the results before returning them.
*   `requirements.txt`: This file lists all external Python libraries that your project depends on. Running `pip install -r requirements.txt` will install exactly these versions of libraries, ensuring the project runs correctly.
*   `.env.example`: This file serves as a template to show users which environment variables are needed for the project to run. It contains the names of the variables (e.g., `GOOGLE_API_KEY`) and placeholder values, making it clear what needs to be configured. Since it contains no actual secrets, it is safe to include in the public repository.
*   `.env`: This file is **created locally by the user** (by copying `.env.example`) and contains their personal, sensitive API keys and configuration settings. It is crucial that this file is **never committed to the repository** and is therefore explicitly listed in the `.gitignore` file.
*   `.gitignore`: This file tells the Git version control system which files and directories in the project should be ignored and not tracked. It's essential for preventing sensitive files like `.env` and temporary build artifacts like `__pycache__/` from being accidentally committed and shared on GitHub.
*   `templates/`: This is a standard directory name recognized by Flask for storing HTML template files. Flask uses these templates to generate the dynamic web pages served by the application.
*   `templates/index.html`: The single HTML file for the user interface. It contains the basic structure of the web page, input forms, areas to display results, CSS for styling, and JavaScript code to handle user interactions and communicate with the backend API.
*   `rough.py`: (Optional) Based on its content, this appears to be a separate script used during development or testing, likely for verifying the scraping and parsing parts of the application in isolation, perhaps using a hardcoded example URL. The main application's logic will use similar functions, but `rough.py` itself is not typically run as part of the main web application. It can be included in the repository as a reference or utility.

## Setup and Installation

To get the Amazon Fake Review Detection project running on your local machine, follow these detailed steps:

1.  **Prerequisites:**
    *   Ensure you have **Python 3.7 or a newer version** installed on your system. You also need `pip`, Python's standard package installer (usually included with modern Python installations). You can download Python from [python.org](https://www.python.org/downloads/).
    *   You must obtain necessary API keys: one for **Google Gemini** and one for **Firecrawl**. Refer to their respective documentation for how to sign up and get keys.

2.  **Clone the repository:**
    Open your terminal or command prompt and clone the project repository from GitHub using `git clone`. Then navigate into the project directory.
    ```bash
    git clone https://github.com/YourUsername/amazon-fake-review-detection.git
    cd amazon-fake-review-detection
    ```
    *(Replace `YourUsername/amazon-fake-review-detection.git` with the actual path to your repository on GitHub.)*

3.  **Create a Virtual Environment (Highly Recommended):**
    Using a virtual environment is considered best practice for Python projects. It isolates the project's dependencies, preventing conflicts with other projects or your system's Python installation.
    ```bash
    # On macOS/Linux:
    python3 -m venv venv   # Creates a virtual environment named 'venv'
    source venv/bin/activate # Activates the virtual environment

    # On Windows:
    python -m venv venv   # Creates a virtual environment named 'venv'
    venv\Scripts\activate # Activates the virtual environment
    ```
    *(After activation, your terminal prompt will typically show the name of the virtual environment, e.g., `(venv)`. You will need to activate the virtual environment each time you open a new terminal session to work on the project.)*

4.  **Install Dependencies:**
    With your virtual environment successfully activated, install all the required Python packages listed in the `requirements.txt` file using `pip`.
    ```bash
    pip install -r requirements.txt
    ```
    This command reads `requirements.txt` and installs all the specified libraries (like Flask, google-generative-ai, firecrawl-python, python-dotenv, beautifulsoup4, requests) into your isolated virtual environment.

5.  **Configuration (Environment Variables):**
    This project requires sensitive API keys to access the Google Gemini and Firecrawl services. For security, these keys must be loaded from environment variables and stored locally in a `.env` file, which is excluded from version control.
    
    *   Locate the `.env.example` file in the root directory of the project (the same directory as `app.py` and `requirements.txt`).
    *   **Copy** this file and rename the copy to `.env`.
        ```bash
        # On macOS/Linux:
        cp .env.example .env

        # On Windows:
        copy .env.example .env
        ```
    *   Open the newly created `.env` file in a text editor.
    *   You will find lines defining variables with placeholder values (e.g., `GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE`). **Replace** the entire placeholder value (the text immediately following the `=` sign) with your actual, obtained API key for each corresponding variable.

    *   **Example of your `.env` file *after* you have edited it with your actual keys:**
        ```
        # Environment variables needed for the Amazon Fake Review Detection project

        GOOGLE_API_KEY=[Your Actual Google API Key Goes Here]
        FIRECRAWL_API_KEY=[Your Actual Firecrawl API Key Goes Here]

        # Add other required variables here if any...
        # DATABASE_URL=...
        # FLASK_ENV=development # Example for Flask environment setting
        ```
        *(Note: Ensure there are no spaces immediately before or after the `=` sign unless they are part of the key itself. Keys should generally not be enclosed in quotes unless they contain special characters or spaces, which is uncommon for API keys).*

    *   Save the `.env` file.
    *   **Security Note:** Your `.env` file contains highly sensitive information (your personal API keys). For your security, the project's `.gitignore` file is specifically configured to prevent this file from being committed to the repository. **Ensure you never manually add or attempt to commit your `.env` file.** Treat your `.env` file as private and local to your development environment.

## Usage

Once you have completed the setup steps and your virtual environment is active, you can run the application and interact with it.

1.  **Activate Virtual Environment** (if not already active):
    Open your terminal or command prompt, navigate to the project directory, and activate your virtual environment:
    ```bash
    # On macOS/Linux:
    source venv/bin/activate

    # On Windows:
    venv\Scripts\activate
    ```

2.  **Run the Flask application:**
    Execute the main application file using the Python interpreter from your active virtual environment:
    ```bash
    python app.py
    ```
    Flask will start a local development server. You should see output in your terminal indicating the server is running, including the local address and port.
    ```
     * Serving Flask app 'app'
     * Debug mode: off # Or 'on' if configured
     WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

3.  **Access the Web Interface:**
    Open your web browser and navigate to the local address displayed in your terminal (usually `http://127.0.0.1:5000/`). You should see the project's homepage with an input field where you can paste an Amazon product URL (preferably from Amazon.in, as noted below) for analysis. Submit the URL and the page should display the results.

4.  **Using the API Endpoint:**
    The application provides a RESTful API endpoint (`/analyze_reviews`) that you can use programmatically to submit URLs and retrieve analysis results. This is useful for integrating the functionality into other scripts, applications, or testing.

    *   **Endpoint URL:** `http://127.0.0.1:5000/analyze_reviews` (When running locally)
    *   **HTTP Method:** `POST`
    *   **Request Body (JSON):** The request body must be a JSON object containing a single key, `"url"`, whose value is the Amazon product URL string you want to analyze.
        ```json
        {
          "url": "https://www.amazon.in/dp/YOUR_PRODUCT_ASIN_HERE/"
        }
        ```
    *   **Response (JSON):** The endpoint will return a JSON response containing the analysis results. The exact structure depends on the backend implementation but typically includes the product title and a list of analyzed reviews, each with its original text and a `"classification"` property (e.g., `"REAL"` or `"FAKE"`).
        ```json
        {
          "product_title": "Example Product Name Extracted",
          "product_price": "₹1,234.56", # Price format may vary
          "reviews": [
            {
              "text": "This is the full text of the first review.",
              "classification": "REAL"
            },
            {
              "text": "Text of the second review...",
              "classification": "FAKE"
            },
            // ... potentially more analyzed reviews ...
          ],
          "message": "Analysis complete" # Optional status message
        }
        ```

## Notes and Limitations

*   **Amazon.in Specific:** The current implementation is primarily tested and configured to reliably work with **Amazon India (.in)** URLs. The parsing and scraping logic may need adjustments to function correctly with other Amazon domains (.com, .co.uk, .de, etc.) due to differences in website structure and HTML class names.
*   **Gemini Model Version:** The application currently utilizes the `gemini-1.5-flash-latest` model for its AI classification. The accuracy and performance of the fake review detection are directly dependent on this specific AI model's capabilities and any updates Google makes to it.
*   **Review Processing Limit:** To manage API costs, processing time, and response size, the application may process a limited number of reviews per product URL. A common limit, for example, is sending a maximum of 50 reviews to Gemini for classification per request. This limit is adjustable in the backend code.
*   **AI Accuracy and Nature:** Detecting fake reviews is an inherently complex and challenging task. The AI's classification ('REAL' or 'FAKE') is an automated analysis based on learned patterns and statistical probabilities. It should be considered an indicator to aid human judgment rather than a definitive, infallible truth about a review's authenticity.
*   **Scraping Reliability:** Web scraping, by its nature, can be fragile. Amazon periodically updates its website's layout and HTML structure. While using the Firecrawl API provides better resilience, significant site changes could potentially impact the scraper's ability to extract data correctly, requiring updates to the parsing logic.
*   **API Key Dependency:** The application is non-functional without valid API keys for both Google Gemini and Firecrawl.

## Contributing

Contributions to this project are welcome! Whether it's fixing bugs, adding new features, improving documentation, or enhancing the UI, your help is appreciated. Please follow these steps to contribute:

1.  **Fork the repository** on GitHub. This creates your own copy of the project under your GitHub account.
2.  **Clone your forked repository** to your local machine.
    ```bash
    git clone https://github.com/YourGitHubUsername/amazon-fake-review-detection.git
    cd amazon-fake-review-detection
    ```
3.  **Create a new branch** for your contribution. Give it a descriptive name related to the feature or bug fix you're working on.
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/issue-number
    ```
4.  **Implement your changes.** Write your code, ensuring it follows standard Python practices and includes necessary comments or docstrings.
5.  **Test your changes** thoroughly to ensure they work as expected and don't introduce new issues.
6.  **Commit your changes** with clear, concise, and descriptive commit messages.
    ```bash
    git add .
    git commit -m "feat: Add functionality to analyze product images" # Example commit message
    ```
7.  **Push your new branch** to your forked repository on GitHub.
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request (PR)** on GitHub. Go to your forked repository's page, click "Compare & pull request" to compare your branch with the main branch of the original repository. Write a clear description of your changes and why they should be merged.

We will review your PR and work with you to get it merged if it aligns with the project's goals.

## License

This project is distributed under the **MIT License**. This is a permissive free software license, meaning you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided you include the original copyright and license notice. You can find the full text of the license in the `LICENSE` file at the root of the repository.

---

*(This README provides comprehensive documentation for the project based on the provided files and discussed architecture, including `app.py`, `requirements.txt`, `templates/index.html`, `.env.example`, `.env` [ignored], and `rough.py` [utility]).*
