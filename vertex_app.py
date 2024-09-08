import streamlit as st
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.generative_models as generative_models

# Load the service account credentials from Streamlit Secrets
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

# Initialize Vertex AI SDK with the provided credentials
vertexai.init(project="mitch-1-0", location="us-central1", credentials=credentials)

# Configuration for generating content
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Safety settings for content generation
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Streamlit UI
st.title("Vertex AI Prompt Tester")

# Text inputs for system instructions and user prompt
textsi_1 = st.text_area("System Instructions", value="""System Instructions:
You are an expert in generating detailed Change Management (CM) documents for IT changes. Your role is to ensure that every CM document follows a strict structure and includes comprehensive information. The format should always include:
1. **Change Subject Line**
2. **Change Description**
3. **Systems Affected**
4. **Justification**
5. **Implementation Details**
6. **Rollback Plan**
7. **Security Impact**
8. **Usability Impact**
9. **Testing Method**

Your responses should be in clear and formal English, with a focus on accuracy, clarity, and detail. Each section must be thoroughly completed with relevant details, and any missing information should be flagged by asking specific follow-up questions.

Example Prompt: 
"I need a CM document for enabling SSPR writeback to on-premises Active Directory."

Expected Output:
Change Subject Line: Microsoft Entra SSPR Writeback to On-premises AD
Change Description: Implement Microsoft Entra SSPR writeback feature to synchronize password changes and resets made in the cloud with the on-premises AD environment, ensuring consistency across both directories.
Systems Affected: Microsoft Entra Connect, on-premises Active Directory
Justification: Enabling SSPR writeback is crucial for maintaining a seamless user experience in a hybrid identity environment. This ensures that any password changes or resets initiated in the cloud are synchronized with on-premises AD, preventing inconsistencies between the two environments and enhancing user security.
Implementation Details: ...""", height=300)

text1_1 = st.text_area("Prompt", value="""I need to create a Google Datastream in the MITCH GCP project that will connect to MySQL at Azure App Service to pull the MunkiReports PHP data into BigQuery so that we can use this info in Vertex.""", height=200)

# Button to submit the prompt
if st.button("Generate Response"):
    with st.spinner("Generating response..."):
        try:
            # Load the model
            model = GenerativeModel("gemini-1.5-flash-001", system_instruction=textsi_1)
            
            # Start chat with the model
            chat = model.start_chat()

            # Send the prompt and get the response
            response = chat.send_message(
                text1_1,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            # Display the response in the Streamlit UI
            st.success("Response generated successfully!")
            st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
