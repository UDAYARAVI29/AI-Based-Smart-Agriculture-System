from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from src.services.disease_service import predict_disease
from src.services import db_service

router = APIRouter(prefix="/predict/disease", tags=["Disease Prediction"])

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def predict_leaf_disease(file: UploadFile = File(...)):
    """
    Predict crop disease from an uploaded leaf image.
    Saves result to MongoDB.
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Upload JPG or PNG.")

    # Save temporary image
    file_id = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(UPLOAD_DIR, file_id)

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = predict_disease(temp_path)

        # Store in DB
        db_doc = {
            "image_name": file_id,
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "meta": {"original_filename": file.filename}
        }
        inserted_id = await db_service.insert_disease_prediction(db_doc)
        result["db_id"] = inserted_id

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)

    return result
