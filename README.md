# TỔNG HỢP KIẾN THỨC VÀ BÀI TẬP LÝ THUYẾT - DỰ ÁN EBOOK2LATEX
*(Từ Bài 4 đến Bài 10)*

---

## I. GHI CHÚ QUAN TRỌNG TRONG QUÁ TRÌNH THỰC HIỆN (LESSONS LEARNED)

### 1. Quản lý mã nguồn (Git)
- Việc đầu tiên khi khởi tạo dự án là luôn dùng `git init` và tạo ngay tệp `.gitignore` (để chặn Git theo dõi các thư mục rác hoặc file chứa mật khẩu như `venv`, `.env`).
- Lệnh `git push -u origin main` có tham số `-u` để tự động thiết lập liên kết luồng theo dõi giữa máy cá nhân và GitHub cho lần đẩy code đầu tiên.

### 2. Môi trường làm việc (Virtual Environment)
- Khi code Python, luôn tạo môi trường ảo (`python -m venv venv`) và kích hoạt (`venv\Scripts\activate`) để cô lập thư viện, tránh xung đột phiên bản với hệ thống.
- Cần chạy lệnh `pip freeze > requirements.txt` để sao lưu toàn bộ danh sách thư viện và phiên bản, giúp thành viên khác hoặc Docker dễ dàng tái lập lại đúng môi trường.

### 3. Bảo mật thông tin (Environment Variables)
- **Tuyệt đối không** viết trực tiếp mật khẩu Database hay các mã API bí mật vào trong code (hard-code).
- Luôn sử dụng tệp ẩn `.env` và thư viện `python-dotenv` để gọi thông tin thông qua biến môi trường `os.getenv()`.
- **Lưu ý nhỏ:** Khi ghi mật khẩu vào biến `DATABASE_URL` trong `.env` để dùng cho SQLAlchemy, nếu có ký tự `@`, hãy đổi nó thành `%40` (URL Encode) để tránh việc SQLAlchemy đọc nhầm cấu trúc `user:pass@host`.

---

## II. GIẢI ĐÁP CÁC BÀI TẬP LÝ THUYẾT

### BÀI 6a: Phân tích Thiết kế các Bảng (Database Schema)
- **Kiến trúc dữ liệu:** Dự án tuân theo chuẩn thiết kế CSDL quan hệ với 4 bảng.
- **Khóa ngoại (Foreign Key) và Ràng buộc (CASCADE):** Bảng `FormulaEntries` phụ thuộc trực tiếp vào `Documents`. Khi một file tài liệu bị xoá, toàn bộ công thức và các lỗi nhận diện hình ảnh (Logs) liên đới tới nó cũng sẽ tự động bị xoá sạch nhờ có ràng buộc `cascade="all, delete-orphan"`, giúp database không có "dữ liệu rác".

### BÀI 7b: Tổng hợp các Lệnh và Bước Quan trọng của SQLAlchemy & Alembic
**Về ORM (SQLAlchemy):**
- Giúp thao tác với Database như đang gọi các Đối tượng (Class) của Python mà không cần viết lệnh truy vấn SQL phức tạp.
- Sử dụng `Base = declarative_base()` để tạo lớp mẹ, sau đó các bảng khác (User, Document...) sẽ kế thừa lớp mẹ này.

**Về Database Migration (Alembic):**
- **Mục đích:** Là công cụ version control cho Database (giống như Git của mã nguồn).
- **Khởi tạo:** `alembic init migrations`
- **Kết nối "bản thiết kế":** Trong `migrations/env.py`, bắt buộc phải gán `target_metadata = Base.metadata` để Alembic biết được cấu trúc code Python đang viết gì mà đem so sánh với PostgreSQL.
- **Lệnh tạo bản thảo cập nhật:** `alembic revision --autogenerate -m "tên bản cập nhật"`
- **Lệnh thực thi chạy cập nhật bảng xuống PostgreSQL:** `alembic upgrade head`

### BÀI 8a: Mục đích của Nhập liệu Tự động (Seeding)
- **Thay vì nhập tay mất thời gian:** Seeding giúp gieo dữ liệu giả định với số lượng lớn trong vài giây (ví dụ dùng thư viện `Faker`).
- **Lợi ích:** Mô phỏng giao diện người dùng thực tế, phát hiện sớm các lỗi tràn màn hình, test khả năng phân trang, test truy vấn lấy dữ liệu và giúp cả nhóm phát triển có cùng một bộ dữ liệu giống nhau.

### BÀI 9b: Mã nguồn của framework FastAPI nằm ở đâu sau khi cài?
- **Trả lời:** Sau khi chạy `pip install fastapi`, mã nguồn gốc của hệ thống FastAPI sẽ không nằm lẫn vào code của dự án, mà được cất giấu an toàn bên trong thư mục môi trường ảo. 
- **Đường dẫn cụ thể:** `Ebook2LateX/venv/Lib/site-packages/fastapi/`. Bạn có thể mở ra để xem cấu trúc nền tảng của framework này.

### BÀI 10: Mô hình Client-Server và Web Services
- **Client (Khách):** Bắt đầu cuộc hội thoại bằng cách gửi Yêu cầu (`Request`) qua HTTP.
- **Server (Chủ):** Lắng nghe ở cổng `8000` (bằng `uvicorn`). Nhận URL (VD: `/shoes/Nike/42`), trích xuất thông tin, tính toán trong backend, rồi đóng gói vào định dạng JSON gửi trả lại (`Response`).
- Ứng dụng Backend không vẽ giao diện mà làm ra các **API Web Services**, trả về dữ liệu thô (JSON), sau này phần Frontend (ReactJS/Vue) sẽ gọi API và hiển thị lên cho người dùng dễ nhìn.
