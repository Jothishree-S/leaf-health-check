from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import base64, uuid, os, io
from PIL import Image
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MODELS ----------
class DiagnoseRequest(BaseModel):
    image_base64: str
    mime_type: str

class DiagnosisResult(BaseModel):
    plant_species: str
    disease_name: str
    description: str
    severity: str
    confidence: str
    rescue_tips: List[str]

# ---------- ROUTE ----------
@app.post("/api/diagnose")
async def diagnose(req: DiagnoseRequest):

    # decode image
    try:
        image_data = base64.b64decode(req.image_base64)
        Image.open(io.BytesIO(image_data))
    except:
        raise HTTPException(400, "Invalid image")

    # 🔥 SIMULATED AI (works without API)
    return {
        "plant_species": "Unknown Plant",
        "disease_name": "Possible Leaf Spot",
        "description": "The plant shows signs of infection or stress. Spots or discoloration detected.",
        "severity": "Moderate",
        "confidence": "Medium",
        "rescue_tips": [
            "Remove infected leaves",
            "Avoid overwatering",
            "Apply organic fungicide"
        ]
    }

# ---------- PDF ----------
@app.post("/api/pdf")
async def pdf(data: DiagnosisResult):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph("Plant Diagnosis Report", styles["Title"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"Plant: {data.plant_species}", styles["Normal"]))
    story.append(Paragraph(f"Disease: {data.disease_name}", styles["Normal"]))
    story.append(Paragraph(f"Description: {data.description}", styles["Normal"]))
    story.append(Paragraph(f"Severity: {data.severity}", styles["Normal"]))

    for tip in data.rescue_tips:
        story.append(Paragraph(f"- {tip}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()
