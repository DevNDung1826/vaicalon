# Image Segment Tool - Công cụ phát hiện và di chuyển chi tiết ảnh

Công cụ Python với giao diện đồ họa để **TỰ ĐỘNG PHÁT HIỆN** các chi tiết trong ảnh, sau đó có thể kéo thả các chi tiết đến **BẤT KỲ VỊ TRÍ NÀO** mà không làm biến dạng.

## ✨ Tính năng nổi bật

### 🤖 Phát hiện tự động
- **Computer Vision**: Sử dụng OpenCV để tự động phát hiện các đối tượng/chi tiết trong ảnh
- **Cài đặt linh hoạt**: Điều chỉnh ngưỡng và kích thước tối thiểu để phát hiện chính xác
- **Không cần đường cắt**: Tool tự động nhận diện các vùng khác nhau

### 🎯 Chi tiết độc lập
- **Đối tượng rời**: Mỗi chi tiết là đối tượng độc lập, không gắn với ảnh gốc
- **Kéo tự do**: Di chuyển chi tiết đến bất kỳ vị trí nào trong workspace
- **Ra ngoài khung**: Chi tiết có thể kéo ra ngoài vùng ảnh gốc
- **Workspace lớn**: Không gian làm việc 3000x3000 pixels với scrollbar

### 🎨 Xử lý ảnh
- **Tải ảnh**: Hỗ trợ JPG, PNG, BMP, GIF, TIFF
- **Lật**: Lật ngang và lật dọc
- **Xoay**: Xoay 0-360 độ với chất lượng cao
- **Reset**: Khôi phục về trạng thái ban đầu

### 💎 Chất lượng cao
- **Không biến dạng**: Chi tiết giữ nguyên kích thước và tỷ lệ
- **Giữ độ nét**: Sử dụng LANCZOS resampling
- **Cập nhật trực tiếp**: Xem kết quả ngay lập tức

## 📦 Cài đặt

### Yêu cầu
- Python 3.8+
- Windows, Linux, hoặc macOS

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
pip install Pillow numpy opencv-python
```

## 🚀 Sử dụng

### Chạy chương trình

```bash
python image_tool.py
```

## 📖 Hướng dẫn chi tiết

### Bước 1: Tải và chuẩn bị ảnh

1. **Tải ảnh**: Click "📁 Tải ảnh" và chọn file
2. **Xử lý (tùy chọn)**:
   - Lật ngang/dọc nếu cần
   - Xoay ảnh đến góc mong muốn

### Bước 2: Phát hiện chi tiết tự động

1. **Click "🔍 Tự động"**: Tool sẽ tự động phát hiện các chi tiết
2. **Điều chỉnh (nếu cần)**:
   - Click "⚙️ Cài đặt" để mở cửa sổ cài đặt
   - **Ngưỡng phát hiện (0-255)**: 
     - Giá trị thấp: Phát hiện nhiều chi tiết hơn
     - Giá trị cao: Chỉ phát hiện vùng tương phản mạnh
     - Mặc định: 127
   - **Kích thước tối thiểu**: 
     - Bỏ qua các vùng nhỏ hơn giá trị này
     - Mặc định: 100 pixels
   - Click "Áp dụng" để phát hiện lại

### Bước 3: Di chuyển chi tiết

#### Di chuyển:
1. **Click vào chi tiết** để chọn (viền chuyển màu xanh lá)
2. **Kéo thả** chi tiết đến vị trí bất kỳ
3. **Có thể kéo ra ngoài** vùng ảnh gốc
4. **Thả chuột** để đặt chi tiết

#### Xóa chi tiết:
- **Cách 1**: Click chuột phải vào chi tiết muốn xóa
- **Cách 2**: Click "🗑 Xóa chi tiết" để xóa tất cả

#### Lưu ý workspace:
- Workspace có kích thước 3000x3000 pixels
- Sử dụng thanh scroll để di chuyển xung quanh
- Lưới màu xám giúp định vị (mỗi ô 100 pixels)

### Bước 4: Lưu kết quả

1. **Click "💾 Lưu"**
2. **Chọn định dạng**:
   - PNG: Nền trong suốt, chất lượng cao
   - JPG: Nền trắng, dung lượng nhỏ
3. **Click "Save"**

## 🎯 Ví dụ sử dụng

### Ví dụ 1: Tách các đối tượng trong ảnh
```
1. Tải ảnh có nhiều đối tượng riêng biệt
2. Click "Tự động" - tool sẽ phát hiện từng đối tượng
3. Kéo từng đối tượng ra vị trí riêng
4. Lưu kết quả với nền trong suốt (PNG)
```

### Ví dụ 2: Tạo collage sáng tạo
```
1. Tải ảnh đầu tiên, phát hiện chi tiết
2. Sắp xếp các chi tiết theo ý muốn
3. Chi tiết có thể xếp chồng lên nhau
4. Lưu tác phẩm nghệ thuật
```

### Ví dụ 3: Phân tích ảnh kỹ thuật
```
1. Tải ảnh kỹ thuật (bản vẽ, sơ đồ)
2. Điều chỉnh ngưỡng để phát hiện đúng các phần
3. Tách các phần ra để nghiên cứu riêng
4. Lưu từng phần riêng biệt
```

## ⚙️ Tham số phát hiện

### Ngưỡng (Threshold)
- **Chức năng**: Quyết định mức độ khác biệt để tách vùng
- **Giá trị thấp (0-100)**: 
  - ✅ Phát hiện nhiều chi tiết
  - ❌ Có thể phát hiện cả nhiễu
- **Giá trị trung bình (100-150)**: 
  - ✅ Cân bằng
  - ✅ Phù hợp đa số ảnh
- **Giá trị cao (150-255)**:
  - ✅ Chỉ phát hiện vùng rõ ràng
  - ❌ Có thể bỏ sót chi tiết nhỏ

### Kích thước tối thiểu
- **Chức năng**: Lọc bỏ vùng quá nhỏ
- **50-200**: Giữ lại chi tiết nhỏ
- **200-1000**: Chỉ giữ vùng trung bình
- **1000+**: Chỉ giữ các đối tượng lớn

## 🎮 Thao tác chuột

| Thao tác | Chức năng |
|----------|-----------|
| **Click trái** | Chọn chi tiết |
| **Kéo thả** | Di chuyển chi tiết |
| **Click chuột phải** | Xóa chi tiết |
| **Scroll** | Di chuyển workspace |

## 💡 Mẹo và thủ thuật

### Mẹo 1: Ảnh nền đơn giản
- Ảnh có nền trắng hoặc nền đơn sắc sẽ phát hiện tốt hơn
- Tương phản cao giữa đối tượng và nền cho kết quả tốt nhất

### Mẹo 2: Điều chỉnh trước khi phát hiện
- Xoay và lật ảnh về đúng hướng trước
- Sau khi phát hiện, các chi tiết sẽ giữ nguyên hướng này

### Mẹo 3: Thử nghiệm tham số
- Nếu phát hiện không đúng, thử điều chỉnh ngưỡng
- Click "Áp dụng" ngay để xem kết quả mới

### Mẹo 4: Sắp xếp nhiều lớp
- Chi tiết được vẽ theo thứ tự (mới nhất ở trên)
- Click vào chi tiết để "kéo lên trên"

### Mẹo 5: Lưu với nền trong suốt
- Chọn PNG để giữ nền trong suốt
- Tiện cho việc ghép với ảnh khác sau này

## 🐛 Xử lý lỗi

### Không phát hiện được chi tiết
**Nguyên nhân**: Ngưỡng không phù hợp
**Giải pháp**: 
- Mở "Cài đặt" và thử giảm ngưỡng xuống 80-100
- Giảm kích thước tối thiểu xuống 50

### Phát hiện quá nhiều vùng lỗi
**Nguyên nhân**: Ngưỡng quá thấp
**Giải pháp**:
- Tăng ngưỡng lên 150-180
- Tăng kích thước tối thiểu lên 200-500

### Chi tiết bị mất sau khi transform
**Lưu ý**: Đây là tính năng, không phải lỗi
- Khi xoay/lật ảnh, tool sẽ xóa chi tiết cũ
- Nhấn "Tự động" lại để phát hiện lại trên ảnh mới

### Không tải được ảnh
- Kiểm tra định dạng file
- Thử chuyển sang PNG hoặc JPG

## 🔧 Yêu cầu kỹ thuật

### Phần cứng đề xuất
- **RAM**: 4GB+ (8GB khuyến nghị)
- **CPU**: Dual-core trở lên
- **Màn hình**: 1366x768 trở lên

### Kích thước ảnh
- **Khuyến nghị**: Dưới 4000x4000 pixels
- **Tối đa**: Phụ thuộc vào RAM
- Ảnh lớn có thể chậm khi phát hiện

## 📝 Lưu ý quan trọng

✅ **Giữ nguyên chất lượng**: Không làm mất độ nét  
✅ **Không biến dạng**: Chi tiết giữ nguyên tỷ lệ  
✅ **Tự do di chuyển**: Kéo đến bất kỳ đâu  
✅ **Cập nhật trực tiếp**: Xem ngay kết quả  
✅ **An toàn**: Không làm mất ảnh gốc  

## 🆘 Hỗ trợ

Nếu gặp vấn đề:
1. Thử reset và tải lại ảnh
2. Kiểm tra phiên bản thư viện
3. Thử với ảnh đơn giản hơn

## 📜 License

MIT License - Tự do sử dụng và chỉnh sửa

---

**Chúc bạn sử dụng công cụ hiệu quả!** 🎨✨🚀
