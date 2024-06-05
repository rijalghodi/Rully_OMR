# main.py
from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import cv2
import numpy as np
from utils import preprocess_bubble
from bubble_classifier import bubble_classifier
from recognize_bubble_sheet import recognize_bubble_sheet as recognize_bubble_sheet_util
from typing import Annotated
import json

app = FastAPI()
router = APIRouter(prefix="/bubble", tags=["Bubble"])


html_content = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Rully API : AI-Powered Universal Bubble Sheet Grader</title>
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Rully : AI-Powered Universal Bubble Sheet Grader</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Created by <a href="https://zalcode.my.id" target="_blank">ZalCode</a></p>
        </div>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_content


class GradeRequest(BaseModel):
    image: UploadFile 
    correct_answers: List[List[int]]

image_types = ["image/png", "image/jpg", "image/jpeg"]

# bubble_labels = ['crossed', 'default', 'filled', 'invalid']

@router.post("/", name="Classify Bubble Answer")
async def classify_bubble_answer(file: UploadFile = File(...)):
    try:
        if file.content_type not in image_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Read the uploaded image file as bytes
        image_bytes = await file.read()


        # Convert bytes to a openCV image
        
        # Convert bytes to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode the image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
   
          # Preprocess the image
        img = preprocess_bubble(img)

        # Ensure the input data type matches the model's expectation (float32)
        img = img.astype(np.float32)

        # Classify Bubble
        result = bubble_classifier(img)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sheet", name="Recognize Bubble Sheet")
async def recognize_bubble_sheet(file: UploadFile = File(...)):
    try:
        if file.content_type not in image_types:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Read and decode the uploaded image
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Recognize bubble sheet
        result = recognize_bubble_sheet_util(img)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/grade-sheet", name="Grade Bubble Sheet")
async def grade_bubble_sheet(
    file: Annotated[UploadFile, File()],
    correct_marks: Annotated[str, Form()],
):
    try:
        correct_marks = json.loads(correct_marks)

        if file.content_type not in image_types:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Read and decode the uploaded image
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Recognize bubble sheet
        result = recognize_bubble_sheet_util(img)

        # Compare with correct marks
        score = sum(1 for a, b in zip(correct_marks, result["marks"]) if a == b)

        return {"score": score, **result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_app() -> FastAPI:
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)