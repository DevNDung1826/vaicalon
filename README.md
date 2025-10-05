# Image Segment Tool - Công cụ chia và di chuyển chi tiết ảnh

Công cụ Python với giao diện đồ họa để xử lý, chia nhỏ và di chuyển các phần của ảnh mà không làm biến dạng.

## Tính năng

### 1. Xử lý ảnh cơ bản
- **Tải ảnh**: Hỗ trợ các định dạng phổ biến (JPG, PNG, BMP, GIF, TIFF)
- **Lật ảnh**: Lật ngang và lật dọc
- **Xoay ảnh**: Xoay từ 0-360 độ với độ nét cao
- **Reset**: Khôi phục ảnh về trạng thái ban đầu

### 2. Chia ảnh thành các chi tiết
- **Thêm đường cắt**: Thêm đường dọc và đường ngang để chia ảnh
- **Điều chỉnh đường cắt**: Kéo các đường cắt để thay đổi vị trí
- **Cập nhật chi tiết**: Chia ảnh thành các chi tiết dựa trên đường cắt
- **Xóa đường**: Xóa tất cả đường cắt

### 3. Di chuyển chi tiết
- **Chọn chi tiết**: Click vào chi tiết để chọn
- **Kéo thả**: Kéo chi tiết đến vị trí mới
- **Không biến dạng**: Các chi tiết giữ nguyên kích thước và độ nét
- **Cập nhật trực tiếp**: Xem kết quả ngay lập tức khi thao tác

### 4. Lưu kết quả
- **Lưu ảnh**: Lưu ảnh đã xử lý ra file PNG hoặc JPG
- **Giữ chất lượng**: Duy trì độ nét và chất lượng ảnh gốc

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Hệ điều hành: Windows, Linux, hoặc macOS

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:

```bash
pip install Pillow numpy opencv-python
```

## Sử dụng

### Chạy chương trình

```bash
python image_tool.py
```

### Hướng dẫn chi tiết

#### Bước 1: Tải ảnh
1. Click nút "📁 Tải ảnh"
2. Chọn file ảnh từ máy tính
3. Ảnh sẽ được hiển thị với đường cắt mặc định (chia 3x3)

#### Bước 2: Xử lý ảnh (tùy chọn)
- **Lật ngang**: Click "↔ Ngang"
- **Lật dọc**: Click "↕ Dọc"
- **Xoay**: Nhập góc xoay (0-360) và click "↻ Quay"

#### Bước 3: Điều chỉnh đường cắt
1. **Thêm đường mới**:
   - Click "➕ Dọc" để thêm đường cắt dọc
   - Click "➕ Ngang" để thêm đường cắt ngang

2. **Di chuyển đường cắt**:
   - Click và kéo đường cắt màu đỏ đến vị trí mong muốn

3. **Cập nhật chi tiết**:
   - Click "🔄 Cập nhật" để chia ảnh thành các chi tiết theo đường cắt

#### Bước 4: Di chuyển chi tiết
1. Sau khi cập nhật chi tiết, các phần ảnh sẽ được viền màu xanh
2. Click vào chi tiết muốn di chuyển
3. Kéo thả chi tiết đến vị trí mới
4. Thả chuột để đặt chi tiết

#### Bước 5: Lưu kết quả
1. Click "💾 Lưu"
2. Chọn vị trí và tên file
3. Chọn định dạng (PNG hoặc JPG)
4. Click "Save"

## Lưu ý quan trọng

1. **Giữ nguyên độ nét**: 
   - Sử dụng thuật toán LANCZOS để resize
   - Lưu với quality=95 cho JPEG
   - Không làm mất chất lượng ảnh

2. **Không biến dạng**:
   - Các chi tiết giữ nguyên tỷ lệ khung hình
   - Không bị kéo giãn hay co lại

3. **Cập nhật trực tiếp**:
   - Mọi thao tác đều hiển thị ngay lập tức
   - Không cần reload hay refresh

4. **Reset an toàn**:
   - Click "↺ Reset" để quay về ảnh gốc bất cứ lúc nào
   - Không làm mất ảnh gốc

## Xử lý lỗi

### Không tải được ảnh
- Kiểm tra định dạng file có được hỗ trợ
- Đảm bảo file không bị hỏng

### Chương trình chạy chậm
- Giảm kích thước ảnh đầu vào
- Giảm số lượng chi tiết

### Lỗi cài đặt thư viện
```bash
# Nếu gặp lỗi với opencv-python, thử:
pip install opencv-python-headless

# Hoặc cập nhật pip:
python -m pip install --upgrade pip
```

## Phím tắt

- **Ctrl+O**: Tải ảnh (nếu thêm vào code)
- **Ctrl+S**: Lưu ảnh (nếu thêm vào code)
- **Escape**: Hủy thao tác hiện tại (nếu thêm vào code)

## Liên hệ và hỗ trợ

Nếu gặp vấn đề hoặc có câu hỏi, vui lòng báo cáo lỗi hoặc yêu cầu tính năng mới.

## License

MIT License - Tự do sử dụng và chỉnh sửa.

---

**Chúc bạn sử dụng công cụ hiệu quả!** 🎨✨
