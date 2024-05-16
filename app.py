from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
## how gemini pro is suppose to behave like is the prompt
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def get_interview_questions(pdf_content, input):
  """Generates interview questions based on resume and job description using gemini-pro."""
  model = genai.GenerativeModel('gemini-pro')
  prompt = input_prompt4.format(resume_content=pdf_content, job_description=input)
  response = model.generate_content([prompt])
  return response.text.split("\n")

def input_pdf_setup(uploaded_file):
    ## convert pdf to images
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        ##convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
       raise FileNotFoundError("No file uploaded")


##Streamlit app
st.set_page_config(page_title="RESUME EXPERT")
st.header("Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file is not None:
    st.write("Pdf uploaded successfully")



submit1 = st.button("Feedback on my resume")

submit2 = st.button("Required keywords in my resume")

submit3 = st.button("Percentage Match")

submit4 = st.button("Take my interview")

input_prompt1 = """ You are an experienced Technical Human Resource Manage experienced in the field of any one job role among data science,full stack web development,Big data 
Engineering,DEVOPS,Data analyst,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""

input_prompt2 = """Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%",    "MissingKeywords:[]"   ,"Profile Summary":""}}"""

input_prompt3 = """ You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role among data science,full stack web development,big data engineering,
DEVOPS,Data analyst and ATS functionality, your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts. """

input_prompt4 = """You are an AI interview coach with expertise in various technical fields. Based on the provided resume and 
job description, generate a list of potential interview questions that assess the candidate's qualifications for the role. Focus on a
 mix of technical skills, soft skills, and experience-based questions relevant to the specific job requirements.

Resume: {resume_content}
Job Description: {job_description}
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf file")

if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf file")       

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")


if submit4:
  if uploaded_file is not None:
    resume_text = input_pdf_setup(uploaded_file)
  else:
    resume_text = input_text
  interview_questions = get_interview_questions(resume_text, input_text)

  if len(interview_questions) > 0:
    st.subheader("Interview Questions:")
    for question in interview_questions:
      st.write(question)
  else:
    st.write("No interview questions generated. Please try revising your resume or job description.")

