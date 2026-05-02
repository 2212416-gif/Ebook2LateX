from app.database import SessionLocal
from app.models import User, Document, FormulaEntry
from sqlalchemy import func

def report_users_documents(db):
    print("--- BÁO CÁO NGƯỜI DÙNG VÀ SỐ LƯỢNG TÀI LIỆU ---")
    results = db.query(
        User.full_name,
        func.count(Document.id).label('doc_count')
    ).outerjoin(Document, User.user_id == Document.user_id)\
     .group_by(User.user_id).all()
    
    for name, count in results:
        print(f"Người dùng: {name} - Số tài liệu: {count}")
    print("-" * 50)

def search_formulas(db, keyword: str):
    print(f"--- TÌM KIẾM CÔNG THỨC VỚI TỪ KHÓA '{keyword}' ---")
    results = db.query(FormulaEntry).filter(FormulaEntry.latex_content.ilike(f"%{keyword}%")).all()
    
    if not results:
        print("Không tìm thấy công thức nào.")
    for entry in results:
        print(f"ID: {entry.id} | LaTeX: {entry.latex_content}")
    print("-" * 50)

if __name__ == "__main__":
    db = SessionLocal()
    try:
        report_users_documents(db)
        search_formulas(db, "sqrt")
    finally:
        db.close()
