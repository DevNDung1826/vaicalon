#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ Di chuyển Chi tiết Ảnh
Một ứng dụng Python tương tác cho phép chọn và di chuyển các phần nhỏ trong ảnh
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import io
from typing import Optional, List, Tuple

class Layer:
    """Lớp đại diện cho một phần ảnh có thể di chuyển"""
    
    def __init__(self, image: Image.Image, x: int, y: int, rotation: float = 0):
        self.image = image
        self.x = x
        self.y = y
        self.width = image.width
        self.height = image.height
        self.rotation = rotation
        self.selected = False
        self.original_image = image.copy()
    
    def contains(self, x: int, y: int) -> bool:
        """Kiểm tra xem điểm (x, y) có nằm trong layer này không"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def rotate(self, angle: float):
        """Xoay layer theo góc cho trước"""
        self.rotation += angle
        self.image = self.original_image.rotate(self.rotation, expand=True)
        self.width = self.image.width
        self.height = self.image.height
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Lấy tọa độ bounds của layer"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


class ImageEditor:
    """Ứng dụng chỉnh sửa ảnh chính"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Công cụ Di chuyển Chi tiết Ảnh")
        self.root.geometry("1200x800")
        
        # State management
        self.original_image: Optional[Image.Image] = None
        self.display_image: Optional[ImageTk.PhotoImage] = None
        self.canvas_image = None
        self.layers: List[Layer] = []
        self.selected_layer: Optional[Layer] = None
        
        # Selection state
        self.select_mode = False
        self.is_selecting = False
        self.selection_start = None
        self.selection_rect = None
        
        # Dragging state
        self.is_dragging = False
        self.drag_start = None
        
        # Zoom
        self.zoom_level = 1.0
        
        # Setup UI
        self.setup_ui()
        
        # Keyboard bindings
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Escape>', lambda e: self.cancel_selection())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-o>', lambda e: self.load_image())
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        
        # Top frame - Title
        title_frame = tk.Frame(self.root, bg='#667eea', pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="🎨 Công cụ Di chuyển Chi tiết Ảnh",
            font=('Arial', 20, 'bold'),
            bg='#667eea',
            fg='white'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Tải ảnh lên và di chuyển các phần tử một cách dễ dàng",
            font=('Arial', 10),
            bg='#667eea',
            fg='white'
        )
        subtitle_label.pack()
        
        # Control frame
        control_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        control_frame.pack(fill=tk.X)
        
        # Buttons
        btn_style = {'font': ('Arial', 10, 'bold'), 'padx': 15, 'pady': 8}
        
        self.load_btn = tk.Button(
            control_frame,
            text="📁 Tải ảnh lên",
            command=self.load_image,
            bg='#667eea',
            fg='white',
            **btn_style
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.select_btn = tk.Button(
            control_frame,
            text="✂️ Chế độ chọn vùng",
            command=self.toggle_select_mode,
            bg='#f0f0f0',
            **btn_style
        )
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(
            control_frame,
            text="🗑️ Xóa vùng",
            command=self.delete_selected,
            bg='#ff6b6b',
            fg='white',
            state=tk.DISABLED,
            **btn_style
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(
            control_frame,
            text="🔄 Đặt lại",
            command=self.reset_canvas,
            bg='#f0f0f0',
            **btn_style
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(
            control_frame,
            text="💾 Lưu ảnh",
            command=self.save_image,
            bg='#51cf66',
            fg='white',
            **btn_style
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Toolbar frame
        toolbar_frame = tk.Frame(self.root, bg='#f8f9fa', pady=8)
        toolbar_frame.pack(fill=tk.X)
        
        # Zoom controls
        tk.Label(toolbar_frame, text="Độ phóng:", bg='#f8f9fa', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar_frame,
            text="-",
            command=lambda: self.zoom(0.9),
            width=3,
            **btn_style
        ).pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = tk.Label(toolbar_frame, text="100%", bg='#f8f9fa', font=('Arial', 9, 'bold'), width=8)
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar_frame,
            text="+",
            command=lambda: self.zoom(1.1),
            width=3,
            **btn_style
        ).pack(side=tk.LEFT, padx=2)
        
        # Rotation controls
        tk.Label(toolbar_frame, text="Xoay:", bg='#f8f9fa', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(20, 5))
        
        tk.Button(
            toolbar_frame,
            text="↺ -15°",
            command=lambda: self.rotate_selection(-15),
            **btn_style
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar_frame,
            text="↻ +15°",
            command=lambda: self.rotate_selection(15),
            **btn_style
        ).pack(side=tk.LEFT, padx=2)
        
        # Canvas frame
        canvas_frame = tk.Frame(self.root, bg='#e0e0e0')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            cursor='cross',
            highlightthickness=2,
            highlightbackground='#667eea'
        )
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack canvas and scrollbars
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas bindings
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.canvas.bind('<Motion>', self.on_mouse_motion)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg='#f8f9fa', pady=10)
        info_frame.pack(fill=tk.X)
        
        self.info_labels = {}
        
        info_items = [
            ('Vị trí chuột:', 'mouse_pos', '-'),
            ('Chế độ:', 'mode', 'Di chuyển'),
            ('Vùng đã chọn:', 'selection', 'Không có')
        ]
        
        for i, (label, key, default) in enumerate(info_items):
            frame = tk.Frame(info_frame, bg='#f8f9fa')
            frame.pack(side=tk.LEFT, padx=20)
            
            tk.Label(frame, text=label, bg='#f8f9fa', font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
            self.info_labels[key] = tk.Label(
                frame, 
                text=default, 
                bg='#f8f9fa', 
                fg='#667eea',
                font=('Arial', 9, 'bold')
            )
            self.info_labels[key].pack(side=tk.LEFT, padx=5)
        
        # Instructions frame
        instr_frame = tk.LabelFrame(
            self.root,
            text="📖 Hướng dẫn sử dụng",
            bg='#e7f5ff',
            font=('Arial', 10, 'bold'),
            fg='#1971c2'
        )
        instr_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        instructions = [
            "▸ Tải ảnh: Nhấp 'Tải ảnh lên' hoặc Ctrl+O",
            "▸ Chọn vùng: Kích hoạt chế độ chọn, sau đó kéo chuột trên ảnh",
            "▸ Di chuyển: Click và kéo vùng đã chọn đến vị trí mới",
            "▸ Xoay: Chọn vùng, sau đó dùng nút xoay (↺/↻)",
            "▸ Xóa: Chọn vùng và nhấn Delete hoặc nút 'Xóa vùng'",
            "▸ Lưu: Nhấn 'Lưu ảnh' hoặc Ctrl+S"
        ]
        
        instr_text = tk.Label(
            instr_frame,
            text='\n'.join(instructions),
            bg='#e7f5ff',
            fg='#495057',
            font=('Arial', 9),
            justify=tk.LEFT,
            anchor='w'
        )
        instr_text.pack(padx=10, pady=5, fill=tk.X)
    
    def load_image(self):
        """Tải ảnh từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[
                ("Tất cả ảnh", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("GIF", "*.gif"),
                ("BMP", "*.bmp")
            ]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert('RGBA')
                self.reset_canvas()
                self.display_image_on_canvas()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
    
    def display_image_on_canvas(self):
        """Hiển thị ảnh lên canvas"""
        if not self.original_image:
            return
        
        # Calculate display size
        display_img = self.render_composite()
        
        self.display_image = ImageTk.PhotoImage(display_img)
        
        # Update canvas
        self.canvas.delete('all')
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        
        # Update scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def render_composite(self) -> Image.Image:
        """Tạo ảnh tổng hợp từ ảnh gốc và các layers"""
        if not self.original_image:
            return Image.new('RGBA', (100, 100), 'white')
        
        # Create composite
        composite = self.original_image.copy()
        
        # Draw layers
        for layer in self.layers:
            composite.paste(layer.image, (layer.x, layer.y), layer.image)
            
            # Draw selection border if selected
            if layer.selected:
                draw = ImageDraw.Draw(composite)
                bounds = layer.get_bounds()
                draw.rectangle(bounds, outline='blue', width=3)
        
        return composite
    
    def toggle_select_mode(self):
        """Bật/tắt chế độ chọn vùng"""
        self.select_mode = not self.select_mode
        
        if self.select_mode:
            self.select_btn.configure(bg='#667eea', fg='white')
            self.canvas.configure(cursor='cross')
            self.info_labels['mode'].configure(text='Chọn vùng')
        else:
            self.select_btn.configure(bg='#f0f0f0', fg='black')
            self.canvas.configure(cursor='hand2')
            self.info_labels['mode'].configure(text='Di chuyển')
    
    def on_mouse_down(self, event):
        """Xử lý sự kiện nhấn chuột"""
        if not self.original_image:
            return
        
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if self.select_mode:
            # Start selection
            self.is_selecting = True
            self.selection_start = (int(x), int(y))
        else:
            # Check if clicking on a layer
            self.selected_layer = None
            for layer in reversed(self.layers):
                if layer.contains(x, y):
                    # Deselect all
                    for l in self.layers:
                        l.selected = False
                    
                    layer.selected = True
                    self.selected_layer = layer
                    self.is_dragging = True
                    self.drag_start = (int(x) - layer.x, int(y) - layer.y)
                    break
            
            self.display_image_on_canvas()
            self.update_info()
    
    def on_mouse_move(self, event):
        """Xử lý sự kiện di chuyển chuột khi đang giữ nút"""
        if not self.original_image:
            return
        
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if self.is_selecting and self.selection_start:
            # Draw selection rectangle
            self.display_image_on_canvas()
            
            x1, y1 = self.selection_start
            x2, y2 = int(x), int(y)
            
            self.selection_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='blue',
                width=2,
                dash=(5, 5)
            )
        
        elif self.is_dragging and self.selected_layer:
            # Move layer
            dx, dy = self.drag_start
            self.selected_layer.x = int(x) - dx
            self.selected_layer.y = int(y) - dy
            self.display_image_on_canvas()
    
    def on_mouse_up(self, event):
        """Xử lý sự kiện thả chuột"""
        if self.is_selecting and self.selection_start:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            self.create_layer_from_selection(self.selection_start[0], self.selection_start[1], int(x), int(y))
            self.is_selecting = False
            self.selection_start = None
        
        self.is_dragging = False
        self.drag_start = None
    
    def on_mouse_motion(self, event):
        """Cập nhật vị trí chuột"""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.info_labels['mouse_pos'].configure(text=f'X: {int(x)}, Y: {int(y)}')
    
    def create_layer_from_selection(self, x1: int, y1: int, x2: int, y2: int):
        """Tạo layer mới từ vùng đã chọn"""
        if not self.original_image:
            return
        
        # Normalize coordinates
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        if width < 5 or height < 5:
            self.display_image_on_canvas()
            return
        
        # Ensure within bounds
        x = max(0, min(x, self.original_image.width))
        y = max(0, min(y, self.original_image.height))
        width = min(width, self.original_image.width - x)
        height = min(height, self.original_image.height - y)
        
        # Extract region
        region = self.original_image.crop((x, y, x + width, y + height))
        
        # Create layer
        layer = Layer(region, x, y)
        layer.selected = True
        
        # Deselect all other layers
        for l in self.layers:
            l.selected = False
        
        self.layers.append(layer)
        self.selected_layer = layer
        
        # Clear the region from original image
        # (We'll keep original intact and just cover it with layers)
        
        self.display_image_on_canvas()
        self.update_info()
        self.delete_btn.configure(state=tk.NORMAL)
    
    def delete_selected(self):
        """Xóa layer đang được chọn"""
        if self.selected_layer and self.selected_layer in self.layers:
            self.layers.remove(self.selected_layer)
            self.selected_layer = None
            self.display_image_on_canvas()
            self.update_info()
            
            if not self.layers:
                self.delete_btn.configure(state=tk.DISABLED)
    
    def rotate_selection(self, angle: float):
        """Xoay layer đang được chọn"""
        if self.selected_layer:
            self.selected_layer.rotate(angle)
            self.display_image_on_canvas()
    
    def zoom(self, factor: float):
        """Phóng to/thu nhỏ canvas"""
        self.zoom_level *= factor
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))
        self.zoom_label.configure(text=f'{int(self.zoom_level * 100)}%')
        
        # Note: Real zoom implementation would require scaling the image
        # For simplicity, just update the label
        messagebox.showinfo("Thông báo", "Chức năng zoom đang được cập nhật!")
    
    def reset_canvas(self):
        """Đặt lại canvas về trạng thái ban đầu"""
        self.layers.clear()
        self.selected_layer = None
        self.zoom_level = 1.0
        self.zoom_label.configure(text='100%')
        self.delete_btn.configure(state=tk.DISABLED)
        
        if self.original_image:
            self.display_image_on_canvas()
        
        self.update_info()
    
    def save_image(self):
        """Lưu ảnh đã chỉnh sửa"""
        if not self.original_image:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải ảnh lên trước!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Lưu ảnh",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                composite = self.render_composite()
                # Convert RGBA to RGB if saving as JPEG
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    rgb_image = Image.new('RGB', composite.size, 'white')
                    rgb_image.paste(composite, mask=composite.split()[3])
                    rgb_image.save(file_path, quality=95)
                else:
                    composite.save(file_path)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh tại:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")
    
    def cancel_selection(self):
        """Hủy selection hiện tại"""
        if self.selected_layer:
            self.selected_layer.selected = False
            self.selected_layer = None
            self.display_image_on_canvas()
        
        if self.select_mode:
            self.toggle_select_mode()
        
        self.update_info()
    
    def update_info(self):
        """Cập nhật thông tin hiển thị"""
        if self.selected_layer:
            self.info_labels['selection'].configure(
                text=f'{self.selected_layer.width}x{self.selected_layer.height} px'
            )
        elif self.layers:
            self.info_labels['selection'].configure(text=f'{len(self.layers)} vùng đã tạo')
        else:
            self.info_labels['selection'].configure(text='Không có')


def main():
    """Chạy ứng dụng"""
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
