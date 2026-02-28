import csv
import os
from sqlalchemy.orm import Session
from .models import User
from .watermark_service import WatermarkService
from .logging_config import logger
from datetime import datetime

class ExportService:
    @staticmethod
    def export_incremental(db: Session, consumer_id: str, storage_path: str):
        last_sync = WatermarkService.get_last_timestamp(db, consumer_id)
        logger.info(f"Export started for {consumer_id}. Last sync point: {last_sync}")

        # Query only records updated AFTER the last watermark
        users = db.query(User).filter(User.updated_at > last_sync).order_by(User.updated_at.asc()).all()

        if not users:
            logger.info("No new changes detected.")
            return None

        # Create filename with timestamp
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{consumer_id}_{ts}.csv"
        full_path = os.path.join(storage_path, filename)

        with open(full_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'email', 'created_at', 'updated_at', 'is_deleted'])
            for u in users:
                writer.writerow([u.id, u.name, u.email, u.created_at.isoformat(), u.updated_at.isoformat(), u.is_deleted])

        # Update the watermark to the timestamp of the last record exported
        new_sync_point = users[-1].updated_at
        WatermarkService.update_timestamp(db, consumer_id, new_sync_point)
        
        logger.info(f"Successfully exported {len(users)} records to {filename}")
        return filename