import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .export_service import ExportService
from datetime import datetime

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CDC Export API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/export/{consumer_id}")
def trigger_export(consumer_id: str, db: Session = Depends(get_db)):
    output_dir = "/app/output"
    
    # Ensure directory exists inside container
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        file_generated = ExportService.export_incremental(db, consumer_id, output_dir)
        
        if not file_generated:
            return {"message": "No new data to export", "consumer_id": consumer_id}

        return {
            "status": "success",
            "consumer_id": consumer_id,
            "file": file_generated,
            "path": f"{output_dir}/{file_generated}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))