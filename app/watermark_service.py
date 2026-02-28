from sqlalchemy.orm import Session
from .models import Watermark
from datetime import datetime, timezone

class WatermarkService:
    @staticmethod
    def get_last_timestamp(db: Session, consumer_id: str) -> datetime:
        watermark = db.query(Watermark).filter(Watermark.consumer_id == consumer_id).first()
        if watermark:
            return watermark.last_exported_at
        return datetime.fromtimestamp(0, tz=timezone.utc)

    @staticmethod
    def update_timestamp(db: Session, consumer_id: str, new_timestamp: datetime):
        watermark = db.query(Watermark).filter(Watermark.consumer_id == consumer_id).first()
        if not watermark:
            watermark = Watermark(
                consumer_id=consumer_id,
                last_exported_at=new_timestamp,
                updated_at=datetime.now(timezone.utc)
            )
            db.add(watermark)
        else:
            watermark.last_exported_at = new_timestamp
            watermark.updated_at = datetime.now(timezone.utc)
        db.commit()