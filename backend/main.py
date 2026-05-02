# Goi thu vien FastAPI
from fastapi import FastAPI

# Tao doi tuong app tu class FastAPI
app = FastAPI()

# Tao decorator cho app.get("/") 
@app.get("/")
# khi nguoi dung truy cap vao web root, goi ham sau
def read_root():
    return {"message": "Chao mung ban den voi Ebook2LateX!"}

# --- BÀI TẬP 10a ---
# Nhận một số từ thanh địa chỉ (Path parameter), nhân với 10 và trả về
@app.get("/multiply/{number}")
def multiply_number(number: int):
    result = number * 10
    return {"original": number, "result": result}

# --- BÀI TẬP 10b ---
# Nhận nhãn hiệu (brand) và kích thước (size) từ thanh địa chỉ, trả về chuỗi xác nhận
@app.get("/shoes/{brand}/{size}")
def buy_shoes(brand: str, size: int):
    return {"message": f"Bạn muốn mua giày {brand} kích thước {size} đúng không?"}
