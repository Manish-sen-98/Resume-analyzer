from fastapi import APIRouter, UploadFile, File, HTTPException,Depends
import shutil
import os
from services.cloudinary import upload_to_cloudinary
from services.gemini import extract_resume_data
from core.security import get_current_user

router = APIRouter(
    prefix="/api/upload",
    tags=["Resume Analysis"]
)

@router.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...),current_user: str = Depends(get_current_user)):
   
    temp_path = f"temp_{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        
        resume_url = upload_to_cloudinary(temp_path)
        parsed_json =await   extract_resume_data(temp_path)
        
        return {
            "status": "success",
            "cloudinary_url": resume_url,
            "data": parsed_json
        }

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)