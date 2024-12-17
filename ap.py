import streamlit as st
from PIL import Image
import pyttsx3
import pytesseract
from gtts import gTTS
from io import BytesIO
from langchain_google_genai import GoogleGenerativeAI

# Set the Tesseract OCR path
# Adjust the path according to your operating system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load API Key for Google Generative AI
try:
    with open('key.txt', 'r') as f:
        GOOGLE_API_KEY = f.read().strip()
except FileNotFoundError:
    st.error("API key file 'key.txt' not found. Please upload or set the correct path.")
    GOOGLE_API_KEY = None

# Initialize Google Generative AI (ensure API key is valid)
if GOOGLE_API_KEY:
    llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GOOGLE_API_KEY)

# Add Custom CSS for Styling
st.markdown(
    """
    <style>
        body { background-color: #f7f9fc; }
        .main-title { font-size: 42px; font-weight: 600; text-align: center; color: #4A90E2; margin-bottom: 10px; }
        .subtitle { font-size: 18px; text-align: center; color: #666; margin-bottom: 30px; }
        .section-title { font-size: 22px; font-weight: 600; margin-top: 30px; margin-bottom: 15px; color: #333; }
        button { background-color: #4A90E2 !important; color: white !important; border-radius: 5px !important; }
        footer { text-align: center; margin-top: 50px; color: #777; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Application Title
st.title(":blue[AI VIJAY ASSIST]")

# Function Definitions
def extract_text(image):
    """Extract text from an image using Tesseract OCR."""
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise RuntimeError(f"Error during OCR: {e}")

def text_to_speech(text):
    """Convert text to speech using gTTS and play in Streamlit."""
    try:
        tts = gTTS(text=text, lang='en')
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)
        st.audio(audio, format="audio/mp3")
    except Exception as e:
        st.error(f"Error during Text-to-Speech: {e}")

def generate_scene_description(prompt):
    """Generate a scene description using Google Generative AI."""
    try:
        response = llm.predict(prompt)
        return response
    except Exception as e:
        raise RuntimeError(f"Error generating scene description: {e}")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. A list of detected items and their purposes.
2. An overall description of the image.
3. Current status and past status of that images.
4. Make future predictions based on image analysis.
5. Suggestions or precautions for visually impaired users.
"""

# Image Upload Section
st.markdown('<div class="section-title">📤 Upload an Image</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open and resize the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Features Section
st.markdown('<div class="section-title">⚙️ Features</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")
audio_scene_button = col4.button("🎤 Describe Scene in Audio")

# Process User Actions
if uploaded_file:
    # Describe Scene
    if scene_button:
        with st.spinner("Generating scene description..."):
            try:
                description = generate_scene_description(input_prompt)
                st.markdown('<div class="section-title">🔍 Scene Description</div>', unsafe_allow_html=True)
                st.write(description)
            except Exception as e:
                st.error(e)

    # Extract Text
    if ocr_button:
        with st.spinner("Extracting text..."):
            try:
                extracted_text = extract_text(image)
                st.markdown('<div class="section-title">📝 Extracted Text</div>', unsafe_allow_html=True)
                st.text_area("Extracted Text", extracted_text, height=200)
            except Exception as e:
                st.error(e)

    # Text-to-Speech
    if tts_button:
        with st.spinner("Converting text to speech..."):
            try:
                extracted_text = extract_text(image)
                if extracted_text.strip():
                    text_to_speech(extracted_text)
                    st.success("✅ Text-to-Speech completed!")
                else:
                    st.warning("No text found in the image.")
            except Exception as e:
                st.error(e)

    # Describe Scene in Audio
    if audio_scene_button:
        with st.spinner("Generating scene description and audio..."):
            try:
                description = generate_scene_description(input_prompt)
                st.markdown('<div class="section-title">🔍 Scene Description</div>', unsafe_allow_html=True)
                st.write(description)
                text_to_speech(description)
                st.success("✅ Scene description has been spoken!")
            except Exception as e:
                st.error(f"Error generating or narrating scene description: {e}")
