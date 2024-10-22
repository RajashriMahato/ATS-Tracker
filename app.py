'''import streamlit as st
import google.generativeai as genai
import os
import json
import PyPDF2 as pdf
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Function to get response from Google's generative AI model
def get_gemini_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()  # Extract text from the current page
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Prompt Template for the API
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
the best assistance for improving resumes. Assign the percentage Matching based 
on the JD and the missing keywords with high accuracy.
resume: {resume}
description: {jd}

I want the response in one single string having the structure as json only:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app interface
st.title("Smart ATS")
st.text("Improve Your Resume for ATS")

# Input for job description
jd = st.text_area("Paste the Job Description")

# File uploader for resume in PDF format
uploaded_file = st.file_uploader("Upload Your Resume (PDF format)", type="pdf", help="Please upload the resume in PDF format", accept_multiple_files=True)

# Submit button
submit = st.button("Submit")

# Logic when the submit button is pressed
if submit:
    if uploaded_file is not None and jd:
        # Extract text from the uploaded PDF
        resume_text = input_pdf_text(uploaded_file)
        
        # Prepare the prompt by formatting the template with resume and JD
        input_prompt = input_prompt_template.format(resume=resume_text, jd=jd)
        
        # Get the response from the API
        response = get_gemini_response(input_prompt)
        
        # Display the response in Streamlit
        st.subheader("ATS Evaluation Result")
        response = response.replace('```json','')
        response = response.replace('```','')
        response = response.strip()
        st.json(json.loads(response)) 
    else:
        st.warning("Please upload a PDF and provide a job description.")'''

import streamlit as st
import google.generativeai as genai
import os
import json
import PyPDF2 as pdf
import pandas as pd
from dotenv import load_dotenv
from io import StringIO

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Function to get response from Google's generative AI model
def get_gemini_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()  # Extract text from the current page
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Prompt Template for the API
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
the best assistance for improving resumes. Assign the percentage Matching based 
on the JD and the missing keywords with high accuracy.
resume: {resume}
description: {jd}

I want the response in one single string having the structure as json only:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app interface
st.title("Smart ATS")
st.text("Improve Your Resume for ATS")

# Input for job description
jd = st.text_area("Paste the Job Description")

# File uploader for resumes in PDF format
uploaded_files = st.file_uploader("Upload Your Resumes (PDF format)", type="pdf", 
                                  help="Please upload the resumes in PDF format", 
                                  accept_multiple_files=True)

# Submit button
submit = st.button("Submit")

# Logic when the submit button is pressed
if submit:
    if uploaded_files and jd:
        # Initialize a list to hold results
        results = []

        # Loop through each uploaded resume file
        for uploaded_file in uploaded_files:
            # Extract text from the uploaded PDF
            resume_text = input_pdf_text(uploaded_file)
            
            # Prepare the prompt by formatting the template with resume and JD
            input_prompt = input_prompt_template.format(resume=resume_text, jd=jd)
            
            # Get the response from the API
            response = get_gemini_response(input_prompt)
            
            # Clean the response
            response = response.replace('```json', '').replace('```', '').strip()
            
            # Convert the response to JSON format
            try:
                response_json = json.loads(response)
            except json.JSONDecodeError:
                response_json = {"JD Match": "Error", "MissingKeywords": [], "Profile Summary": "Error parsing response"}
            
            # Append the response to results
            results.append({
                "Resume File": uploaded_file.name,
                "JD Match": response_json.get("JD Match"),
                "Missing Keywords": ", ".join(response_json.get("MissingKeywords", [])),
                "Profile Summary": response_json.get("Profile Summary")
            })

        # Create a DataFrame to hold the results
        df_results = pd.DataFrame(results)

        # Display the DataFrame in Streamlit
        st.subheader("ATS Evaluation Results")
        st.dataframe(df_results)

        # Convert DataFrame to CSV format and provide a download link
        csv_data = df_results.to_csv(index=False)
        st.download_button("Download CSV", data=csv_data, file_name="ATS_Results.csv", mime="text/csv")
    
    else:
        st.warning("Please upload at least one PDF and provide a job description.")
