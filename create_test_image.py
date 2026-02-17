#!/usr/bin/env python3
"""
Script tạo ảnh test để demo ứng dụng
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Tạo ảnh test với các phần khác nhau"""
    # Tạo ảnh 400x300
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ các hình chữ nhật màu khác nhau
    colors = [
        ('red', (0, 0, 100, 100)),
        ('blue', (100, 0, 200, 100)),
        ('green', (200, 0, 300, 100)),
        ('yellow', (300, 0, 400, 100)),
        ('purple', (0, 100, 100, 200)),
        ('orange', (100, 100, 200, 200)),
        ('cyan', (200, 100, 300, 200)),
        ('pink', (300, 100, 400, 200)),
        ('brown', (0, 200, 100, 300)),
        ('gray', (100, 200, 200, 300)),
        ('lime', (200, 200, 300, 300)),
        ('navy', (300, 200, 400, 300))
    ]
    
    for color, (x1, y1, x2, y2) in colors:
        draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)
    
    # Thêm text
    try:
        # Thử sử dụng font mặc định
        font = ImageFont.load_default()
    except:
        font = None
    
    # Vẽ text trên các phần
    text_positions = [
        ("A", 50, 50),
        ("B", 150, 50),
        ("C", 250, 50),
        ("D", 350, 50),
        ("E", 50, 150),
        ("F", 150, 150),
        ("G", 250, 150),
        ("H", 350, 150),
        ("I", 50, 250),
        ("J", 150, 250),
        ("K", 250, 250),
        ("L", 350, 250)
    ]
    
    for text, x, y in text_positions:
        if font:
            draw.text((x-5, y-5), text, fill='white', font=font)
        else:
            draw.text((x-5, y-5), text, fill='white')
    
    # Lưu ảnh
    img.save('test_image.png')
    print("✓ Đã tạo ảnh test: test_image.png")
    
    return 'test_image.png'

def main():
    print("=== TẠO ẢNH TEST ===\n")
    
    # Tạo ảnh test
    image_path = create_test_image()
    
    print(f"\nẢnh test đã được tạo: {image_path}")
    print("Bạn có thể sử dụng ảnh này để test ứng dụng thao tác ảnh.")
    print("\nCác phần trong ảnh:")
    print("- 12 hình chữ nhật màu khác nhau")
    print("- Mỗi phần có kích thước 100x100 pixels")
    print("- Có thể cắt và di chuyển các phần này")

if __name__ == "__main__":
    main()