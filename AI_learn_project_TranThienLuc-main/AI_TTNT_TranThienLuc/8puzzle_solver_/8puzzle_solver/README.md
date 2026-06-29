# GIẢI QUYẾT BÀI TOÁN 8 PUZZLE BẰNG CÁC GIẢI THUẬT TÌM KIẾM

Dự án này tập trung triển khai và mô phỏng trực quan các thuật toán tìm kiếm cơ bản trong Trí tuệ nhân tạo (AI) ứng dụng trên trò chơi ô số 8-Puzzle.

## 🛠 Môi trường và Điều kiện chuẩn bị

- Ngôn ngữ: **Python 3.x**
- Bộ thư viện đồ họa tích hợp sẵn: `tkinter`
- **Không yêu cầu** cài đặt thêm bất kỳ thư viện bên thứ ba nào (No external dependencies).

## 🚀 Hướng dẫn khởi chạy ứng dụng

Vui lòng mở terminal/cmd tại thư mục gốc của đồ án và thực thi chuỗi lệnh sau:

```bash
cd 8puzzle_solver
python main.py

📁 8puzzle_solver/
│
├── 📄 main.py               # Module điều khiển giao diện người dùng chính (Tkinter UI)
│
├── 📂 algorithms/           # Thư mục lưu trữ logic các giải thuật tìm kiếm
│   ├── 📄 __init__.py       # Khai báo gói (package initialization)
│   ├── 📄 utils.py          # Hệ thống hàm bổ trợ tính toán toán học & heuristic
│   ├── 📄 bfs.py            # Giải thuật tìm kiếm theo chiều rộng
│   ├── 📄 dfs.py            # Giải thuật tìm kiếm theo chiều sâu
│   ├── 📄 dls.py            # Giải thuật tìm kiếm giới hạn độ sâu
│   ├── 📄 ids.py            # Giải thuật tìm kiếm sâu dần
│   └── 📄 ucs.py            # Giải thuật chi phí đồng nhất
│
└── 📄 README.md             # Tài liệu đặc tả kỹ thuật và hướng dẫn sử dụng đồ án