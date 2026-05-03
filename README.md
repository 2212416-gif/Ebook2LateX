# EBOOK2LATEX - TỔNG HỢP KIẾN THỨC VÀ GHI CHÚ BÀI HỌC

Tài liệu này tổng hợp các ghi chú, bài học kinh nghiệm (lessons learned) và giải đáp lý thuyết chi tiết cho từng bài học trong dự án Ebook2LateX (từ Bài 4 đến Bài 10).

---

## Bài 4: Khởi tạo dự án
- **Công cụ:** Git, Github.
- **Ghi chú quan trọng:**
  - `git init`: Khởi tạo kho chứa mã nguồn cục bộ.
  - Tệp `.gitignore`: Rất quan trọng để chặn Git theo dõi các thư mục rác, thư viện (như `venv`, `node_modules`) hoặc tệp nhạy cảm (như `.env` chứa mật khẩu). Có thể tạo tự động thông qua các trang web hỗ trợ như gitignore.io.
  - Lệnh `git push -u origin main`: Tham số `-u` giúp thiết lập liên kết luồng theo dõi mặc định giữa nhánh cục bộ và nhánh trên Github cho lần đẩy đầu tiên.

## Bài 5: Cài đặt hệ quản trị cơ sở dữ liệu
- **Công cụ:** PostgreSQL, pgAdmin 4.
- **Ghi chú quan trọng:**
  - Dữ liệu thực tế của PostgreSQL được hệ quản trị tự động quản lý tách biệt hoàn toàn với thư mục mã nguồn dự án.
  - Dự án sẽ giao tiếp với cơ sở dữ liệu thông qua chuỗi kết nối an toàn. Tuyệt đối không hard-code mà phải lưu ở tệp môi trường `.env`.
  - Định dạng chuỗi kết nối: `postgresql://[user]:[password]@[host]:[port]/[database_name]`

## Bài 6: Phân tích và thiết kế các bảng
- **Kiến trúc CSDL:** Dự án xoay quanh 4 bảng chính:
  1. `Documents`: Lưu thông tin file PDF người dùng tải lên (ID, Tên file, Đường dẫn URL, Thời gian, Trạng thái xử lý).
  2. `FormulaEntries`: Lưu nội dung công thức (Lưu ảnh vùng cắt, Mã LaTeX trích xuất, Thứ tự, Khóa ngoại tham chiếu về Document).
  3. `Users`: Quản lý tài khoản (Mật khẩu mã hóa, Quyền truy cập).
  4. `Logs`: Lưu lịch sử, theo dõi hiệu suất OCR của mô hình AI (Thời gian dịch, Độ tin cậy, Thông báo lỗi).
- **Ràng buộc (CASCADE):** Cần thiết lập để đảm bảo tính toàn vẹn. Ví dụ: Khi người dùng xoá một tài liệu (`Document`), tất cả công thức (`FormulaEntries`) và lỗi (`Logs`) liên đới tới nó cũng sẽ tự động bị xoá sạch, giúp Database không sinh ra dữ liệu rác.

## Bài 7: Tạo các bảng (ORM & Database Migration)
- **Công cụ:** SQLAlchemy, Alembic.
- **Ghi chú quan trọng:**
  - **Môi trường ảo (venv):** Luôn cô lập thư viện của dự án để tránh xung đột. Sử dụng `pip freeze > requirements.txt` để xuất và sao lưu danh sách thư viện.
  - **ORM (SQLAlchemy):** Viết code bằng Python dưới dạng Lớp (Class) kế thừa từ `Base = declarative_base()` để mô tả cấu trúc bảng thay vì viết lệnh SQL thô.
  - **Di chuyển CSDL (Alembic):** Công cụ quản lý phiên bản thay đổi (version control) của Database.
    - Cấu hình bắt buộc: Trong `migrations/env.py`, cần thiết lập `target_metadata = Base.metadata` để Alembic có thể "đọc hiểu" được cấu trúc bạn đã định nghĩa trong Python. Trong `alembic.ini`, mật khẩu chứa chữ `@` phải được đổi thành `%40`.
    - `alembic revision --autogenerate -m "..."`: Tự động so sánh code Python và Database thực tế để sinh ra tập tin kịch bản cập nhật.
    - `alembic upgrade head`: Áp dụng kịch bản cập nhật xuống PostgreSQL.

## Bài 8: Nhập dữ liệu tự động (Seeding)
- **Khái niệm:** Quá trình "gieo" dữ liệu mô phỏng, tự động nạp số lượng lớn bản ghi vào các bảng.
- **Mục đích:**
  - Tối ưu thời gian thay vì nhập thủ công từng dòng trên pgAdmin.
  - Dùng để kiểm thử giao diện (UI/UX) (ví dụ text dài có bị vỡ bố cục không) và đánh giá logic phân trang, tìm kiếm.
  - Xác thực các ràng buộc khóa ngoại hoạt động chính xác.
- **Thực hành:** 
  - Mở một `SessionLocal` để tương tác với Database.
  - Ứng dụng thư viện `Faker` để tự động sinh ra hàng chục người dùng với thông tin (Tên, Email) ngẫu nhiên.
  - Đọc dữ liệu công thức mẫu từ một file `data.json` và chèn vào bảng.

## Bài 9: Web services
- **Khái niệm:** Dịch vụ web là những đoạn phần mềm có khả năng giao tiếp và trao đổi dữ liệu với các ứng dụng khác qua môi trường mạng (Internet, HTTP). Định dạng trả về thường là dữ liệu thô `JSON` thay vì trang web HTML dành cho con người đọc.
- **Khung làm việc (FastAPI):**
  - Framework hiện đại, mạnh mẽ của Python hỗ trợ bất đồng bộ và tự kiểm tra kiểu dữ liệu (Validation) thông qua Pydantic.
  - **Uvicorn:** Là phần mềm web server ASGI dùng để khởi chạy và hứng Request cho FastAPI. Cú pháp chạy: `uvicorn main:app --reload`.
  - Khi cài đặt, mã nguồn của framework FastAPI sẽ nằm sâu bên trong thư mục cô lập của dự án: `venv\Lib\site-packages\fastapi`.

## Bài 10: Lập trình Web services
- **Mô hình Client-Server:** Web Services hoạt động theo chu trình: Trình duyệt (Client) gửi yêu cầu (HTTP Request) qua URL -> Web Server (Uvicorn) nhận yêu cầu -> Backend (FastAPI) xử lý (nhân 10, ghép chuỗi) -> Gửi trả kết quả về (HTTP Response) dưới dạng JSON.
- **Truyền dữ liệu (Path Parameters):** Bạn có thể gán các tham số thẳng vào thanh địa chỉ để FastAPI thu thập. Ví dụ: `@app.get("/shoes/{brand}/{size}")` sẽ hứng "Nike" và "42" từ đường dẫn URL.
- **Tài liệu tự động (Swagger UI):** Một tính năng tuyệt vời của FastAPI là việc tự sinh trang giao diện tài liệu tại endpoint `/docs`, giúp đội nhóm dễ dàng đọc hiểu và thử nghiệm các API.
