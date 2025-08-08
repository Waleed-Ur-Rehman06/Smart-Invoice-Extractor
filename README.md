# Smart Invoice Extractor

# Overview
This is an intelligent web application designed to simplify the process of extracting key information from invoices. Simply upload an image of an invoice, and the AI-powered engine will analyze the document and provide you with the most important details, such as the total amount, invoice number, and line items. This project is perfect for quickly digitizing and organizing your invoice data.

# Features 
Effortless Data Extraction: Upload an invoice image (JPG, JPEG, PNG) and get key details in seconds.
Intuitive UI: A clean, modern, and easy-to-use interface built with Streamlit.
Intelligent Analysis: Powered by an AI-powered extraction engine for highly accurate data extraction.
Interactive Response: Receive the extracted information in a clean, readable format with a one-click copy-to-clipboard button.
Customizable Prompts: Ask the model specific questions about your invoice, like "What is the total amount due?" or "List all the products."


# How to Run the App 

# Prerequisites
make sure you have the following installed:
Python 3.10 or a newer version.
Google API Key for the gemini 2.0 flash model.

# Installation
1.Clone the repository:
    ```bash
    git clone [https://github.com/Waleed-Ur-Rehman06/Smart-Invoice-Extractor.git]
    cd Smart-Invoice-Extractor
    ```

2. Create a virtual environment(recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

# Configuration
1.  Create a .env file in the root directory of your project.
2.  Add your Google API key to this file:
    ```bash
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

# Launch the Application

Run the app from your terminal using Streamlit:
```bash
streamlit run app.py