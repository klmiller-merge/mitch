import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.generative_models as generative_models

# Initialize Vertex AI SDK
project_id = "mitch-1-0"  # replace with your project ID
location = "us-central1"
vertexai.init(project=project_id, location=location)

# Configuration for the model
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Streamlit interface
st.title("Vertex AI Prompt Tester")

# Text areas for system instructions and prompt
textsi_1 = st.text_area("System Instructions", value="""System Instructions: You are an expert in generating detailed Change Management (CM) documents for IT changes...""")
text1_1 = st.text_area("Prompt", value="""I need to create a Google Datastream in the MITCH GCP project that will connect to MySQL at Azure App Service...""")

# Button to submit the prompt
if st.button("Submit"):
    with st.spinner("Generating response..."):
        try:
            # Generate response from Vertex AI
            model = GenerativeModel("gemini-1.5-flash-001", system_instruction=textsi_1)
            chat = model.start_chat()

            response = chat.send_message(text1_1, generation_config=generation_config, safety_settings=safety_settings)

            st.success("Response generated successfully!")
            st.write("Response:", response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

