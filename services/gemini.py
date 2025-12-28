import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
from db.database import save_resume_data

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def extract_resume_data(file_path):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    
    sample_file = genai.upload_file(path=file_path, display_name="Resume_Analysis")
    
   
    prompt = """
    Act as a professional ATS (Applicant Tracking System) and Data Extractor.
    Analyze the attached resume and extract the data into a STRICT JSON format.

    JSON Structure:
    {
      "name": "Full Name",
      "email": "Email Address",
      "phone": "Phone Number",
      "skills": ["Skill 1", "Skill 2"],
      "experience": [{"company": "", "role": "", "duration": ""}],
      "education": [{"institution": "", "degree": "", "year": ""}],
      "ats": 0,
      "job_role": "Primary Job Title"
    }
    """
    
    try:
       
        response = model.generate_content([sample_file, prompt])
             
        content = response.text
        
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        
        

        if json_match:
           clean_json_str = json_match.group(0)
           data_dict = json.loads(clean_json_str)
    
           await save_resume_data(data_dict)
    
           if "_id" in data_dict:
             data_dict["_id"] = str(data_dict["_id"])

           return data_dict
        else:
            raise ValueError("No valid JSON found in AI response")

    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        
        return {
            "name": None, "email": None, "phone": None, "skills": [], 
            "experience": [], "education": [], "ats": 0, "job_role": "Unknown"
        }