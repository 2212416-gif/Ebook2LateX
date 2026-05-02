import json
import uuid
from app.database import SessionLocal
from app.models import FormulaEntry, Document

def seed_from_json():
    db = SessionLocal()
    try:
        print("Đang đọc dữ liệu từ data.json...")
        with open("data.json", "r", encoding="utf-8") as f:
            formulas_data = json.load(f)
            
        # Lấy một document_id ngẫu nhiên có sẵn trong database để gán công thức vào
        first_doc = db.query(Document).first()
        if not first_doc:
            print("Không có tài liệu nào trong database để gán công thức.")
            return

        for i, item in enumerate(formulas_data):
            formula = FormulaEntry(
                id=uuid.uuid4(),
                document_id=first_doc.id,
                latex_content=item["latex"],
                order_index=i+1
            )
            db.add(formula)
            
        db.commit()
        print(f"Đã chèn {len(formulas_data)} công thức từ JSON vào Database thành công!")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_from_json()
