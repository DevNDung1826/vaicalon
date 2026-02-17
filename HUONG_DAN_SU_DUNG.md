# HƯỚNG DẪN SỬ DỤNG CHI TIẾT

## 🎯 Tổng quan
Công cụ thao tác ảnh chi tiết là một ứng dụng Python với GUI cho phép:
- Xoay và lật ảnh
- Cắt ảnh thành các chi tiết
- Di chuyển các chi tiết một cách tự do
- Giữ nguyên chất lượng ảnh

## 🚀 Cách chạy ứng dụng

### Phương pháp 1: Sử dụng script launcher
```bash
./run_app.sh
```

### Phương pháp 2: Chạy trực tiếp
```bash
python3 image_manipulation_tool.py
```

## 📋 Các tính năng chi tiết

### 1. Load ảnh
- **Nút "Chọn ảnh"**: Mở dialog để chọn file ảnh
- **Hỗ trợ định dạng**: JPG, JPEG, PNG, BMP, GIF, TIFF
- **Hiển thị**: Ảnh được hiển thị tự động fit vào cửa sổ

### 2. Xoay ảnh
- **Thanh trượt "Góc xoay"**: Xoay ảnh từ 0° đến 360°
- **Hiển thị góc**: Label hiển thị góc hiện tại
- **Cập nhật real-time**: Ảnh được cập nhật ngay khi thay đổi

### 3. Lật ảnh
- **Lật ngang**: Đảo ảnh theo chiều ngang (trái ↔ phải)
- **Lật dọc**: Đảo ảnh theo chiều dọc (trên ↔ dưới)
- **Lật trái**: Xoay ảnh 90° ngược chiều kim đồng hồ
- **Lật phải**: Xoay ảnh 90° theo chiều kim đồng hồ

### 4. Cắt ảnh
- **Thêm đường cắt ngang**: Thêm đường cắt ngang ở giữa ảnh
- **Thêm đường cắt dọc**: Thêm đường cắt dọc ở giữa ảnh
- **Xóa tất cả đường cắt**: Xóa tất cả đường cắt đã thêm
- **Cắt ảnh**: Thực hiện việc cắt ảnh theo các đường đã vẽ

### 5. Di chuyển chi tiết
- **Click và kéo**: Click vào một phần đã cắt và kéo để di chuyển
- **Reset vị trí**: Đưa tất cả chi tiết về vị trí ban đầu
- **Không biến dạng**: Các chi tiết giữ nguyên kích thước và chất lượng

## 🎨 Giao diện

### Panel điều khiển (bên trái)
- **Chọn ảnh**: Nút load ảnh
- **Xoay ảnh**: Thanh trượt và label hiển thị góc
- **Lật ảnh**: 4 nút lật khác nhau
- **Cắt ảnh**: Các nút thêm/xóa đường cắt và cắt ảnh
- **Di chuyển chi tiết**: Hướng dẫn và nút reset

### Canvas hiển thị (bên phải)
- **Hiển thị ảnh**: Ảnh được scale để fit cửa sổ
- **Đường cắt**: Hiển thị bằng đường đỏ
- **Chi tiết**: Các phần đã cắt có thể di chuyển

## 🔧 Cài đặt và yêu cầu

### Yêu cầu hệ thống
- Python 3.7+
- Hệ điều hành có hỗ trợ GUI (Windows, macOS, Linux với X11)

### Cài đặt thư viện
```bash
pip3 install -r requirements.txt
```

### Cài đặt tkinter (Linux)
```bash
sudo apt-get install python3-tk
```

## 📁 Cấu trúc file

```
├── image_manipulation_tool.py    # File chính
├── requirements.txt              # Danh sách thư viện
├── run_app.sh                   # Script launcher
├── create_test_image.py         # Tạo ảnh test
├── test_headless.py            # Test không cần GUI
├── test_image.png              # Ảnh test mẫu
└── README.md                   # Hướng dẫn cơ bản
```

## 🎯 Workflow sử dụng

1. **Khởi động**: Chạy `./run_app.sh` hoặc `python3 image_manipulation_tool.py`
2. **Load ảnh**: Click "Chọn ảnh" và chọn file ảnh
3. **Thao tác cơ bản**: Xoay, lật ảnh theo ý muốn
4. **Cắt ảnh**: Thêm đường cắt và click "Cắt ảnh"
5. **Di chuyển**: Click và kéo các chi tiết để sắp xếp lại
6. **Reset**: Click "Reset vị trí" nếu muốn quay lại ban đầu

## ⚠️ Lưu ý quan trọng

- **Chất lượng ảnh**: Ảnh được xử lý với thuật toán LANCZOS để giữ nguyên chất lượng
- **Không biến dạng**: Các chi tiết giữ nguyên tỷ lệ khi di chuyển
- **Real-time**: Mọi thay đổi được hiển thị ngay lập tức
- **Memory**: Ảnh lớn có thể tốn nhiều RAM, nên resize trước nếu cần

## 🐛 Xử lý lỗi thường gặp

### Lỗi "No module named 'tkinter'"
```bash
sudo apt-get install python3-tk
```

### Lỗi "No display name"
- Chạy trong môi trường có GUI
- Hoặc sử dụng X11 forwarding nếu SSH

### Ảnh không hiển thị
- Kiểm tra định dạng file có được hỗ trợ không
- Thử với ảnh khác

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python version >= 3.7
2. Đã cài đặt đầy đủ thư viện
3. Môi trường có hỗ trợ GUI
4. File ảnh hợp lệ