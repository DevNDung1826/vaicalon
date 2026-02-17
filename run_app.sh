#!/bin/bash

echo "=== CÔNG CỤ THAO TÁC ẢNH CHI TIẾT ==="
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy. Vui lòng cài đặt Python3."
    exit 1
fi

# Kiểm tra thư viện
echo "🔍 Kiểm tra thư viện..."
python3 -c "import tkinter, PIL, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Thiếu thư viện. Đang cài đặt..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Không thể cài đặt thư viện."
        exit 1
    fi
fi

echo "✅ Thư viện đã sẵn sàng"
echo ""

# Tạo ảnh test nếu chưa có
if [ ! -f "test_image.png" ]; then
    echo "🖼️  Tạo ảnh test..."
    python3 create_test_image.py
fi

echo "🚀 Khởi động ứng dụng..."
echo ""
echo "Hướng dẫn sử dụng:"
echo "1. Click 'Chọn ảnh' để load ảnh"
echo "2. Sử dụng thanh trượt để xoay ảnh"
echo "3. Click các nút lật để lật ảnh"
echo "4. Thêm đường cắt và click 'Cắt ảnh'"
echo "5. Click và kéo để di chuyển các phần đã cắt"
echo ""

# Chạy ứng dụng
python3 image_manipulation_tool.py