import random
from datetime import datetime, timedelta, timezone
from faker import Faker
import psycopg2
import os

def seed_data():
    conn = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase"))
    cur = conn.cursor()

    # Clear old data to start fresh for the final audit
    cur.execute("TRUNCATE users, watermarks RESTART IDENTITY CASCADE;")
    
    fake = Faker()
    base_time = datetime.now(timezone.utc) - timedelta(days=30)
    
    print("Starting clean seed of 100,000 records with deleted flags...")
    
    batch_size = 10000
    for b in range(10):
        records = []
        for _ in range(batch_size):
            created = base_time + timedelta(seconds=random.randint(0, 2592000))
            updated = created + timedelta(seconds=random.randint(0, 86400))
            # 2% chance of being deleted
            is_deleted = random.random() < 0.02 
            records.append((fake.name(), fake.unique.email(), created, updated, is_deleted))
        
        args_str = ",".join(cur.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in records)
        cur.execute("INSERT INTO users (name, email, created_at, updated_at, is_deleted) VALUES " + args_str)
        print(f"Inserted {batch_size * (b+1)} records...")
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_data()