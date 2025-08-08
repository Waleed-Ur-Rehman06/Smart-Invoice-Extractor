import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import io
import base64 

# Load environment variables from .env
load_dotenv()

# Custom CSS for a beautiful UI 
st.markdown("""
<style>
    /* General Page Styling */
    .main {
        background-color: #F0F2F6; 
        padding: 20px;
        box-sizing: border-box;
    }
    .stApp {
        background-color: #F0F2F6;
    }

    /* Header Styling */
    h1 {
        color: #2C3E50; 
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Input & File Uploader Containers */
    .stTextInput>div>div>input, .stFileUploader>div>button {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 10px 15px;
        transition: all 0.2s ease-in-out;
    }
    .stTextInput>div>div>input:focus, .stFileUploader>div>button:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
    }
    .stTextInput label, .stFileUploader label {
        font-weight: 600;
        color: #333333;
        margin-bottom: 8px;
        display: block;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #4CAF50; 
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 25px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: block;
        margin: 25px auto 0 auto; 
    }
    .stButton>button:hover {
        background-color: #45a049; 
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        background-color: #3e8e41;
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Image Display Styling */
    .stImage {
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 5px;
        background-color: white;
        margin-top: 20px;
    }
    .stImage img {
        border-radius: 5px; 
    }

    /* Response Section */
    .stMarkdown h2 {
        color: #2C3E50;
        margin-top: 30px;
        margin-bottom: 15px;
        text-align: center;
    }
    .response-container {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-top: 20px;
        position: relative;
    }
    .response-container p {
        font-size: 16px;
        line-height: 1.6;
        color: #333333;
        white-space: pre-wrap; 
        word-wrap: break-word; 
    }

    /* Copy to Clipboard Button */
    .copy-button {
        background-color: #6C757D; 
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 15px;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        position: absolute;
        top: 10px;
        right: 10px;
    }
    .copy-button:hover {
        background-color: #5A6268;
    }

    /* Alert Messages (Success, Error, Warning) */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 20px;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    div[data-testid="stAlert"] .stMarkdown {
        padding: 0; 
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #2C3E50;
        font-size: 20px;
        margin-bottom: 20px;
    }

    /* Spinner Customization */
    .stSpinner > div > div {
        border-top-color: #4CAF50 !important;
    }

</style>
""", unsafe_allow_html=True)


# Configure model
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"Configuration Error: Please ensure GOOGLE_API_KEY is set in your .env file. Details: {e}")
    st.stop() # Stop the app if API key is not configured


# Load model
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Failed to load gemini-2.0-flash model. Check API key and network. Details: {e}")
    st.stop()


def get_gemini_response(input_text, image_parts, user_prompt):
    """
    Sends the input, image, and user prompt to the gemini-2.0-flash model
    and returns the generated text response.
    """
    try:
        # The input_text goes first as context, then the image, then the specific user query
        response = model.generate_content([input_text, image_parts[0], user_prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating content from Gemini: {e}")
        return None 

def input_image_details(uploaded_file):
    """
    Processes an uploaded file into the format expected by gemini-2.0-flash API.
    """
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        # This case should ideally be caught by frontend validation
        # but included for robustness
        raise FileNotFoundError("No file uploaded. Please choose an image.")

# Copy to clipboard functionality
def copy_to_clipboard_js(text):
    """Generates JavaScript to copy text to clipboard."""
    js_code = f"""
    <script>
    function copyTextToClipboard(text) {{
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";  // Avoid scrolling to bottom
        textArea.style.left = "-9999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {{
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Copying text command was ' + msg);
            // Optional: Show a temporary success message in Streamlit
            Streamlit.setComponentValue("copied"); // This needs a custom component to work fully
            alert("Text copied to clipboard!"); // Simple alert for direct feedback
        }} catch (err) {{
            console.error('Oops, unable to copy', err);
        }}
        document.body.removeChild(textArea);
    }}
    copyTextToClipboard("{base64.b64encode(text.encode('utf-8')).decode('utf-8')}");
    </script>
    """
    # Use base64 encoding to safely pass potentially complex text through JS string literal
    st.components.v1.html(js_code, height=0, width=0)


# Streamlit UI Layout 
st.set_page_config(page_title="Smart Invoice Extractor", layout="centered")

st.markdown("<h1>💰 Smart Invoice Extractor</h1>", unsafe_allow_html=True)
st.markdown("---") # Visual separator

# Main content area
col1, col2 = st.columns([1, 1]) # Use columns for input and image side-by-side initially

with col1:
    input_prompt_text = st.text_area(
        "**Your Question about the Invoice:**",
        value="Extract all key details like total amount, invoice number, date, vendor name, and line items.",
        height=100,
        placeholder="e.g., 'What is the total amount due?' or 'List all line items and their prices.'"
    )

    uploaded_file = st.file_uploader(
        "**Upload an image of the invoice...**",
        type=["jpg", "jpeg", "png"],
        key="file_uploader",
        help="Supported formats: JPG, JPEG, PNG"
    )

with col2:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice Image", use_container_width=True)
    else:
        st.info("Upload an invoice image to get started!")
        # Placeholder for attractive empty image area
        st.markdown(
            """
            <div style="height: 250px; border: 2px dashed #D1D5DB; border-radius: 8px;
                        display: flex; justify-content: center; align-items: center;
                        color: #6B7280; font-size: 18px; text-align: center;">
                No image uploaded yet.
            </div>
            """, unsafe_allow_html=True
        )

# Submit button centered at the bottom of the input section
submit_button = st.button("Analyze Invoice", key="submit_button")

# This prompt guides the AI on its role
gemini_role_prompt = """
You are an expert in understanding and extracting information from invoices.
Your task is to meticulously analyze the uploaded invoice image and answer any questions
based solely on the content of the invoice. If a piece of information is not present
on the invoice, state that clearly.
Be precise, accurate, and structured in your responses.
"""

# Main Logic on Submit
if submit_button:
    if uploaded_file is None:
        st.error("Please upload an invoice image before clicking 'Analyze Invoice'.")
    elif not input_prompt_text.strip():
        st.error("Please enter a question or prompt about the invoice.")
    else:
        with st.spinner("Analyzing your invoice... This may take a few moments."):
            try:
                # Prepare image 
                image_data = input_image_details(uploaded_file)

                # Get response 
                response_text = get_gemini_response(gemini_role_prompt, image_data, input_prompt_text)

                if response_text:
                    st.markdown("---") # Visual separator before response
                    st.markdown("<h2>Analysis Result </h2>", unsafe_allow_html=True)

                    st.markdown(f'<div class="response-container">', unsafe_allow_html=True)
                    st.markdown(f'<p>{response_text}</p>', unsafe_allow_html=True)

                    # Copy to clipboard button
                    if st.button("Copy to Clipboard", key="copy_button", help="Click to copy the extracted text."):
                        copy_to_clipboard_js(response_text)
                        st.toast("Copied to clipboard!", icon="✅") # Streamlit's built-in toast notification
                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.warning("⚠️ Could not get a response from the AI. Please try again or check your input.")

            except FileNotFoundError as fnf_err:
                st.error(f"File Error: {fnf_err}")
            except Exception as ex:
                st.error(f"An unexpected error occurred: {ex}. Please try again.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6B7280; font-size: 14px; margin-top: 30px;">
        AI-powered Extraction Engine
    </div>
    """, unsafe_allow_html=True
)



