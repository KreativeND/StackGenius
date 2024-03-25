import json
import streamlit as st
import google.generativeai as genai  # Import for Generative AI


def get_api_key():
    """Retrieves the API key from the text input, handling empty input gracefully."""
    api_key = st.text_input('API Key', placeholder='enter your google generativeai api key', key='api_key', label_visibility="collapsed")
    return api_key.strip() if api_key else None  # Remove leading/trailing whitespace and handle empty input

def get_project_description():
    """Retrieves the project description."""
    desc = st.text_area("Project Description", placeholder="Describe your project here...", key='project_description')
    return desc.strip() if desc else ""  # Return empty string if no text

def get_software_type():
    """Gets the selected software type from the dropdown menu."""
    software_type_options = ["Web App", "Hybrid App", "Android App", "iOS App", "Desktop App"]
    selected_type = st.selectbox("Software Type", options=software_type_options)
    return selected_type.lower().replace(" ", "_")  # Convert to lowercase and snake_case

def call_generative_ai_api(api_key, project_description, software_type):
    """Calls the Google Generative AI API to generate tech stack recommendations."""

    genai.configure(api_key=api_key)

    sample_output = """{ "front-end_languages": {
                    "languages": "suggested language or framework only one ",
                    "justification": "justification for selecting framework",
                    "docs": "link of docs if available or null"
                },
                "back-end_languages": {
                    "languages": "suggested language or framework only one ",
                    "justification": "justification for selecting framework",
                    "docs": "link of docs if available or null"
                },
                "database": {
                    "type": "database type",
                    "specific_database": "suggested database",
                    "justification": "justification for selecting database",
                    "docs": "link of docs if available or null"
                },
                "deployment_platform": {
                    "platform": "deployment platform",
                    "justification": "justification for selecting following platform",
                    "docs": "link of docs if available or null"
                } """
    prompt = f"Recommend a tech stack for a {software_type} with the following description: {project_description}. sample output :{sample_output}"

    response = genai.generate_text(prompt=prompt)

    result = response.result;
    if result != "":
        # Parse the tech stack recommendations from the response
        try:
            tech_stack_data = json.loads(result)  # Assuming JSON response
            return tech_stack_data;
        except ValueError:
            st.error("Invalid response format from Generative AI API.")
            return None
    else:
        st.error(f"API request failed with status code: {response.status_code}")
        return None

def display_tech_stack_details(section_name, section_data):
    """Displays details for a specific tech stack section (front-end, back-end, etc.)"""
    with st.expander(section_name):
        for key, value in section_data.items():
            st.write(f"{key.capitalize()}: {value}")

st.header('StackGenius', divider='rainbow')
st.caption('Empower Your Projects with StackGenius: Discover Your Ideal Tech Stack!')

api_key = get_api_key()
if api_key:
    project_description = get_project_description()
    software_type = get_software_type()

    # Display button as soon as text area value changes
    submit = st.button("Submit", type="primary", disabled=False)

    if submit:
        tech_stack_data = call_generative_ai_api(api_key, project_description, software_type)

        if tech_stack_data:
            st.header('Recommended Tech Stack')

            # Iterate through each section of the data and display in an expander
            for section_name, section_data in tech_stack_data.items():
                display_tech_stack_details(section_name.replace('_', ' '), section_data)
        else:
            st.error("Error fetching recommendations. Please check your API key or try again later.")