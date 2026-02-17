# Công cụ thao tác ảnh chi tiết

Ứng dụng Python với GUI để thao tác ảnh với các tính năng:

## Tính năng chính

1. **Load và hiển thị ảnh**: Chọn và hiển thị ảnh từ máy tính
2. **Xoay ảnh**: Thanh trượt để xoay ảnh 360 độ
3. **Lật ảnh**: Các nút lật ngang, dọc, trái, phải
4. **Cắt ảnh**: Thêm đường cắt ngang/dọc để chia ảnh thành các chi tiết
5. **Di chuyển chi tiết**: Click và kéo để di chuyển các phần đã cắt
6. **Giữ nguyên chất lượng**: Ảnh không bị biến dạng, giữ nguyên độ nét
7. **Update real-time**: Thay đổi được hiển thị ngay lập tức

## Cài đặt

1. Cài đặt Python 3.7+
2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Chạy ứng dụng:
```bash
python image_manipulation_tool.py
```

2. **Chọn ảnh**: Click nút "Chọn ảnh" để load ảnh từ máy tính

3. **Xoay ảnh**: Sử dụng thanh trượt "Góc xoay" để xoay ảnh từ 0-360 độ

4. **Lật ảnh**: 
   - Lật ngang: Đảo ảnh theo chiều ngang
   - Lật dọc: Đảo ảnh theo chiều dọc  
   - Lật trái: Xoay ảnh 90 độ ngược chiều kim đồng hồ
   - Lật phải: Xoay ảnh 90 độ theo chiều kim đồng hồ

5. **Cắt ảnh**:
   - Click "Thêm đường cắt ngang" để thêm đường cắt ngang ở giữa
   - Click "Thêm đường cắt dọc" để thêm đường cắt dọc ở giữa
   - Click "Cắt ảnh" để thực hiện việc cắt
   - Click "Xóa tất cả đường cắt" để xóa các đường cắt

6. **Di chuyển chi tiết**:
   - Sau khi cắt ảnh, click và kéo các phần đã cắt để di chuyển
   - Click "Reset vị trí" để đưa các chi tiết về vị trí ban đầu

## Lưu ý

- Ảnh được xử lý với chất lượng cao, không bị biến dạng
- Tất cả thao tác được cập nhật ngay lập tức
- Hỗ trợ các định dạng ảnh: JPG, JPEG, PNG, BMP, GIF, TIFF
- Các chi tiết có thể di chuyển tự do mà không bị biến dạng