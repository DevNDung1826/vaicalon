#!/usr/bin/env python3
"""
Script test headless để kiểm tra ứng dụng thao tác ảnh
"""

import sys
import os

def test_imports():
    """Test import các thư viện cần thiết"""
    try:
        import tkinter as tk
        from PIL import Image, ImageTk
        import numpy as np
        print("✓ Tất cả thư viện đã được import thành công")
        return True
    except ImportError as e:
        print(f"✗ Lỗi import: {e}")
        return False

def test_pil_functionality():
    """Test chức năng PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFilter
        import numpy as np
        
        # Tạo ảnh test
        img = Image.new('RGB', (100, 100), color='red')
        
        # Test resize với LANCZOS
        resized = img.resize((50, 50), Image.Resampling.LANCZOS)
        
        # Test rotate
        rotated = img.rotate(45, expand=True)
        
        # Test flip
        flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
        
        print("✓ PIL hoạt động bình thường")
        return True
    except Exception as e:
        print(f"✗ Lỗi PIL: {e}")
        return False

def test_code_syntax():
    """Test syntax của code chính"""
    try:
        # Đọc và compile code
        with open('image_manipulation_tool.py', 'r') as f:
            code = f.read()
        
        compile(code, 'image_manipulation_tool.py', 'exec')
        print("✓ Code syntax hợp lệ")
        return True
    except SyntaxError as e:
        print(f"✗ Lỗi syntax: {e}")
        return False
    except Exception as e:
        print(f"✗ Lỗi khác: {e}")
        return False

def main():
    print("=== KIỂM TRA ỨNG DỤNG THAO TÁC ẢNH (HEADLESS) ===\n")
    
    # Test imports
    print("1. Kiểm tra thư viện...")
    if not test_imports():
        sys.exit(1)
    
    # Test PIL functionality
    print("\n2. Kiểm tra chức năng PIL...")
    if not test_pil_functionality():
        sys.exit(1)
    
    # Test code syntax
    print("\n3. Kiểm tra syntax code...")
    if not test_code_syntax():
        sys.exit(1)
    
    print("\n✓ Tất cả kiểm tra đều thành công!")
    print("\nỨng dụng đã sẵn sàng sử dụng!")
    print("\nĐể chạy ứng dụng (cần môi trường có GUI), sử dụng lệnh:")
    print("python3 image_manipulation_tool.py")

if __name__ == "__main__":
    main()