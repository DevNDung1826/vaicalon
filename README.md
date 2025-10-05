# 🎨 Công cụ Di chuyển Chi tiết Ảnh

Một ứng dụng Python desktop tương tác cho phép bạn chọn và di chuyển các phần nhỏ trong ảnh một cách dễ dàng.

## ✨ Tính năng

- 📁 **Tải ảnh lên**: Hỗ trợ các định dạng ảnh phổ biến (PNG, JPG, JPEG, GIF, BMP)
- ✂️ **Chọn vùng**: Vẽ hình chữ nhật để chọn bất kỳ phần nào của ảnh
- 🎯 **Tự động co vùng**: Khi chọn xong, vùng sẽ TỰ ĐỘNG co lại chỉ bao quanh chi tiết thực sự (loại bỏ phần trong suốt/trống)
- 🖱️ **Kéo thả**: Di chuyển các vùng đã chọn đến bất kỳ vị trí nào
- 🔄 **Xoay**: Xoay các phần tử đã chọn theo góc ±15°
- 🔍 **Phóng to/thu nhỏ**: Điều chỉnh kích thước hiển thị
- 🗑️ **Xóa**: Xóa các phần không mong muốn
- 💾 **Lưu**: Tải xuống ảnh đã chỉnh sửa (PNG hoặc JPEG)

## 🚀 Cài đặt và Chạy

### Yêu cầu hệ thống:
- Python 3.7 trở lên
- pip (Python package manager)

### Bước 1: Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
```

Hoặc cài đặt trực tiếp:

```bash
pip install Pillow
```

### Bước 2: Chạy ứng dụng

```bash
python image_editor.py
```

Hoặc trên Linux/Mac:

```bash
python3 image_editor.py
```

hoặc làm cho file thực thi được:

```bash
chmod +x image_editor.py
./image_editor.py
```

## 📖 Hướng dẫn sử dụng

### 1. Tải ảnh lên
- Click nút **"📁 Tải ảnh lên"** hoặc nhấn `Ctrl + O`
- Chọn file ảnh từ máy tính của bạn
- Ảnh sẽ hiển thị trên canvas

### 2. Chọn vùng muốn di chuyển
- Click nút **"✂️ Chế độ chọn vùng"** (nút sẽ chuyển màu xanh tím)
- Nhấn giữ chuột trái và kéo để vẽ hình chữ nhật xung quanh chi tiết muốn di chuyển
- Thả chuột để hoàn thành việc chọn
- **✨ MAGIC**: Vùng sẽ TỰ ĐỘNG co lại để chỉ bao quanh phần chi tiết thực sự, loại bỏ các pixel trong suốt/trống xung quanh!
- Vùng đã chọn sẽ có viền xanh dương

### 3. Di chuyển chi tiết
- Tắt chế độ chọn vùng (click lại nút nếu đang bật)
- Click vào vùng đã chọn và kéo đến vị trí mới
- Thả chuột để đặt vùng đó xuống

### 4. Co vùng thủ công (nếu cần)
- Nếu bạn muốn co lại vùng đã chọn sau khi di chuyển hoặc xoay
- Chọn vùng đó (click vào để có viền xanh)
- Click nút **"🎯 Co vùng chọn"**
- Vùng sẽ tự động loại bỏ các pixel trong suốt và co lại vừa khít với chi tiết

### 5. Xoay chi tiết
- Chọn vùng muốn xoay (click vào nó để có viền xanh)
- Click nút **"↺ -15°"** để xoay ngược chiều kim đồng hồ
- Click nút **"↻ +15°"** để xoay cùng chiều kim đồng hồ
- Có thể click nhiều lần để xoay nhiều góc hơn

### 6. Xóa chi tiết
- Chọn vùng muốn xóa
- Click nút **"🗑️ Xóa vùng"** hoặc nhấn phím `Delete`

### 7. Lưu ảnh
- Click nút **"💾 Lưu ảnh"** hoặc nhấn `Ctrl + S`
- Chọn vị trí và tên file
- Chọn định dạng (PNG hoặc JPEG)

### 8. Đặt lại
- Click nút **"🔄 Đặt lại"** để xóa tất cả các vùng đã chọn và quay về ảnh gốc

## ⌨️ Phím tắt

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + O` | Tải ảnh lên |
| `Ctrl + S` | Lưu ảnh |
| `Delete` | Xóa vùng đang chọn |
| `Escape` | Hủy chọn / Thoát chế độ chọn vùng |

## 🎯 Mẹo sử dụng

1. **Tự động co vùng thông minh**: Không cần chọn chính xác! Chỉ cần vẽ vùng chọn xung quanh chi tiết (có thể to hơn), vùng sẽ TỰ ĐỘNG co lại vừa khít
2. **Chọn thoải mái**: Với tính năng auto-trim, bạn có thể chọn vùng rộng hơn, không cần chính xác 100%
3. **Tạo nhiều vùng**: Bạn có thể tạo nhiều vùng khác nhau từ cùng một ảnh và di chuyển chúng độc lập
4. **Sắp xếp lại**: Các vùng được tạo sau sẽ nằm trên các vùng trước đó
5. **Co lại bất cứ lúc nào**: Nếu sau khi xoay vùng bị to ra, dùng nút "🎯 Co vùng chọn" để co lại
6. **Lưu thường xuyên**: Nên lưu lại tiến độ thường xuyên để tránh mất dữ liệu

## 🛠️ Công nghệ sử dụng

- **Python 3**: Ngôn ngữ lập trình chính
- **Tkinter**: Thư viện GUI có sẵn trong Python
- **Pillow (PIL)**: Thư viện xử lý ảnh mạnh mẽ

## 📝 Cấu trúc file

```
image_editor.py     # File Python duy nhất chứa toàn bộ ứng dụng
requirements.txt    # Danh sách thư viện cần cài đặt
README.md          # Hướng dẫn sử dụng (file này)
```

## 🌟 Ví dụ sử dụng

Công cụ này rất hữu ích cho:
- ✅ Chỉnh sửa sprite sheet cho game
- ✅ Sắp xếp lại các phần tử trong ảnh
- ✅ Tạo composition ảnh mới từ các chi tiết
- ✅ Thiết kế nhân vật hoặc đồ họa
- ✅ Tách và sắp xếp lại các đối tượng trong ảnh

## ⚠️ Lưu ý

- Ảnh của bạn không được tải lên server nào, tất cả xử lý đều cục bộ
- Với ảnh kích thước lớn, việc xử lý có thể mất thời gian
- Nên lưu ảnh định dạng PNG để giữ chất lượng tốt nhất
- Chế độ xoay có thể làm tăng kích thước vùng đã chọn

## 🐛 Xử lý sự cố

### Lỗi "No module named 'PIL'"
```bash
pip install --upgrade Pillow
```

### Lỗi "tkinter not found" (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Ứng dụng chạy chậm với ảnh lớn
- Thử giảm kích thước ảnh trước khi tải lên
- Đóng các ứng dụng khác đang chạy

## 📧 Hỗ trợ

Nếu gặp vấn đề:
1. Đảm bảo đã cài đặt đúng Python 3.7+
2. Kiểm tra đã cài đặt Pillow chưa: `pip list | grep -i pillow`
3. Thử chạy với quyền admin/sudo nếu gặp lỗi quyền truy cập

---

**Phiên bản:** 1.0  
**Ngôn ngữ:** Python 3  
**Giấy phép:** MIT  

Chúc bạn sử dụng vui vẻ! 🎉
