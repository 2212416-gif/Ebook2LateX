import uuid
import random
from faker import Faker
from app.database import SessionLocal
from app.models import User, Document

def seed_faker_data():
    fake = Faker('vi_VN')
    db = SessionLocal()
    
    try:
        print("Đang tạo 50 người dùng ngẫu nhiên và tài liệu...")
        for _ in range(50):
            # Tạo User
            user = User(
                user_id=uuid.uuid4(),
                username_email=fake.unique.email(),
                password_hash="hashed_password",
                full_name=fake.name(),
                role=random.choice(["Admin", "Editor", "Viewer"])
            )
            db.add(user)
            db.flush() # Để có user_id
            
            # Tạo 2-5 Documents cho User này
            num_docs = random.randint(2, 5)
            for _ in range(num_docs):
                doc = Document(
                    id=uuid.uuid4(),
                    user_id=user.user_id,
                    file_name=fake.file_name(extension="pdf"),
                    file_path_url=f"/uploads/{fake.file_name(extension='pdf')}",
                    status=random.choice(["Pending", "Processed", "Error"]),
                    version=1
                )
                db.add(doc)
                
        db.commit()
        print("Đã tạo xong dữ liệu ngẫu nhiên bằng Faker!")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_faker_data()
