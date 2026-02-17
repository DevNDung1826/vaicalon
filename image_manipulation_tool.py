import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import math
import numpy as np

class ImageManipulationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ thao tác ảnh chi tiết")
        self.root.geometry("1200x800")
        
        # Biến lưu trữ
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_tk = None
        self.rotation_angle = 0
        self.flip_horizontal = False
        self.flip_vertical = False
        
        # Hệ thống cắt ảnh
        self.cut_lines = []  # [{'x': x, 'y': y, 'type': 'horizontal'/'vertical'}]
        self.image_segments = []  # Các phần ảnh đã cắt
        self.selected_segment = None
        self.drag_start = None
        self.segment_positions = {}  # Vị trí của các segment
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame điều khiển
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Nút load ảnh
        ttk.Button(control_frame, text="Chọn ảnh", command=self.load_image).pack(pady=5, fill=tk.X)
        
        # Frame xoay ảnh
        rotation_frame = ttk.LabelFrame(control_frame, text="Xoay ảnh")
        rotation_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(rotation_frame, text="Góc xoay (độ):").pack()
        self.rotation_var = tk.IntVar()
        self.rotation_scale = ttk.Scale(rotation_frame, from_=0, to=360, 
                                       variable=self.rotation_var, 
                                       command=self.on_rotation_change)
        self.rotation_scale.pack(fill=tk.X, padx=5)
        
        self.rotation_label = ttk.Label(rotation_frame, text="0°")
        self.rotation_label.pack()
        
        # Frame lật ảnh
        flip_frame = ttk.LabelFrame(control_frame, text="Lật ảnh")
        flip_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(flip_frame, text="Lật ngang", command=self.flip_horizontal_image).pack(fill=tk.X, pady=2)
        ttk.Button(flip_frame, text="Lật dọc", command=self.flip_vertical_image).pack(fill=tk.X, pady=2)
        ttk.Button(flip_frame, text="Lật trái", command=self.flip_left).pack(fill=tk.X, pady=2)
        ttk.Button(flip_frame, text="Lật phải", command=self.flip_right).pack(fill=tk.X, pady=2)
        
        # Frame cắt ảnh
        cut_frame = ttk.LabelFrame(control_frame, text="Cắt ảnh")
        cut_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(cut_frame, text="Thêm đường cắt ngang", command=self.add_horizontal_cut).pack(fill=tk.X, pady=2)
        ttk.Button(cut_frame, text="Thêm đường cắt dọc", command=self.add_vertical_cut).pack(fill=tk.X, pady=2)
        ttk.Button(cut_frame, text="Xóa tất cả đường cắt", command=self.clear_cuts).pack(fill=tk.X, pady=2)
        ttk.Button(cut_frame, text="Cắt ảnh", command=self.cut_image).pack(fill=tk.X, pady=2)
        
        # Frame di chuyển chi tiết
        move_frame = ttk.LabelFrame(control_frame, text="Di chuyển chi tiết")
        move_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(move_frame, text="Click và kéo để di chuyển").pack()
        ttk.Button(move_frame, text="Reset vị trí", command=self.reset_positions).pack(fill=tk.X, pady=2)
        
        # Frame hiển thị ảnh
        self.image_frame = ttk.Frame(main_frame)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas để hiển thị ảnh
        self.canvas = tk.Canvas(self.image_frame, bg='white', cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image = self.current_image.copy()
                self.update_display()
                self.clear_cuts()
                messagebox.showinfo("Thành công", "Ảnh đã được tải thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
    
    def update_display(self):
        if self.display_image is None:
            return
            
        # Tính toán kích thước hiển thị
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.update_display)
            return
        
        # Tính tỷ lệ để fit ảnh vào canvas
        img_width, img_height = self.display_image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y) * 0.9  # 90% để có margin
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize ảnh với chất lượng cao
        resized_image = self.display_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Chuyển đổi sang PhotoImage
        self.image_tk = ImageTk.PhotoImage(resized_image)
        
        # Xóa canvas cũ và vẽ ảnh mới
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.image_tk, anchor=tk.CENTER)
        
        # Vẽ các đường cắt
        self.draw_cut_lines()
        
        # Vẽ các segment nếu có
        self.draw_segments()
    
    def on_rotation_change(self, value):
        self.rotation_angle = int(float(value))
        self.rotation_label.config(text=f"{self.rotation_angle}°")
        self.apply_transformations()
    
    def flip_horizontal_image(self):
        self.flip_horizontal = not self.flip_horizontal
        self.apply_transformations()
    
    def flip_vertical_image(self):
        self.flip_vertical = not self.flip_vertical
        self.apply_transformations()
    
    def flip_left(self):
        self.rotation_angle = (self.rotation_angle - 90) % 360
        self.rotation_var.set(self.rotation_angle)
        self.rotation_label.config(text=f"{self.rotation_angle}°")
        self.apply_transformations()
    
    def flip_right(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.rotation_var.set(self.rotation_angle)
        self.rotation_label.config(text=f"{self.rotation_angle}°")
        self.apply_transformations()
    
    def apply_transformations(self):
        if self.original_image is None:
            return
            
        # Bắt đầu từ ảnh gốc
        img = self.original_image.copy()
        
        # Áp dụng flip
        if self.flip_horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if self.flip_vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Áp dụng xoay
        if self.rotation_angle != 0:
            img = img.rotate(-self.rotation_angle, expand=True, fillcolor=(255, 255, 255))
        
        self.current_image = img
        self.display_image = img.copy()
        self.update_display()
    
    def add_horizontal_cut(self):
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
        
        # Thêm đường cắt ngang ở giữa ảnh
        img_height = self.current_image.size[1]
        cut_y = img_height // 2
        
        self.cut_lines.append({'x': 0, 'y': cut_y, 'type': 'horizontal'})
        self.update_display()
    
    def add_vertical_cut(self):
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
        
        # Thêm đường cắt dọc ở giữa ảnh
        img_width = self.current_image.size[0]
        cut_x = img_width // 2
        
        self.cut_lines.append({'x': cut_x, 'y': 0, 'type': 'vertical'})
        self.update_display()
    
    def clear_cuts(self):
        self.cut_lines.clear()
        self.image_segments.clear()
        self.segment_positions.clear()
        self.selected_segment = None
        self.update_display()
    
    def draw_cut_lines(self):
        if not self.cut_lines or self.current_image is None:
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.current_image.size
        
        # Tính tỷ lệ scale
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y) * 0.9
        
        for cut in self.cut_lines:
            if cut['type'] == 'horizontal':
                # Vẽ đường ngang
                y = canvas_height//2 + (cut['y'] - img_height//2) * scale
                self.canvas.create_line(0, y, canvas_width, y, fill='red', width=2, tags='cut_line')
            else:  # vertical
                # Vẽ đường dọc
                x = canvas_width//2 + (cut['x'] - img_width//2) * scale
                self.canvas.create_line(x, 0, x, canvas_height, fill='red', width=2, tags='cut_line')
    
    def cut_image(self):
        if self.current_image is None or not self.cut_lines:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh và thêm đường cắt!")
            return
        
        # Sắp xếp các đường cắt
        horizontal_cuts = sorted([cut['y'] for cut in self.cut_lines if cut['type'] == 'horizontal'])
        vertical_cuts = sorted([cut['x'] for cut in self.cut_lines if cut['type'] == 'vertical'])
        
        # Thêm biên ảnh
        img_width, img_height = self.current_image.size
        horizontal_cuts = [0] + horizontal_cuts + [img_height]
        vertical_cuts = [0] + vertical_cuts + [img_width]
        
        # Cắt ảnh thành các segment
        self.image_segments.clear()
        self.segment_positions.clear()
        
        for i in range(len(horizontal_cuts) - 1):
            for j in range(len(vertical_cuts) - 1):
                left = vertical_cuts[j]
                top = horizontal_cuts[i]
                right = vertical_cuts[j + 1]
                bottom = horizontal_cuts[i + 1]
                
                if right > left and bottom > top:
                    segment = self.current_image.crop((left, top, right, bottom))
                    segment_id = f"segment_{i}_{j}"
                    self.image_segments.append({
                        'id': segment_id,
                        'image': segment,
                        'original_bounds': (left, top, right, bottom),
                        'current_position': (left, top)
                    })
                    self.segment_positions[segment_id] = (left, top)
        
        self.update_display()
        messagebox.showinfo("Thành công", f"Đã cắt ảnh thành {len(self.image_segments)} phần!")
    
    def draw_segments(self):
        if not self.image_segments or self.current_image is None:
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.current_image.size
        
        # Tính tỷ lệ scale
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y) * 0.9
        
        for segment in self.image_segments:
            # Tính vị trí hiển thị
            pos = self.segment_positions.get(segment['id'], segment['current_position'])
            x, y = pos
            
            # Chuyển đổi tọa độ ảnh sang tọa độ canvas
            canvas_x = canvas_width//2 + (x - img_width//2) * scale
            canvas_y = canvas_height//2 + (y - img_height//2) * scale
            
            # Resize segment để hiển thị
            segment_width = int(segment['image'].size[0] * scale)
            segment_height = int(segment['image'].size[1] * scale)
            
            if segment_width > 0 and segment_height > 0:
                resized_segment = segment['image'].resize((segment_width, segment_height), Image.Resampling.LANCZOS)
                segment_tk = ImageTk.PhotoImage(resized_segment)
                
                # Lưu reference để tránh garbage collection
                segment['tk_image'] = segment_tk
                
                # Vẽ segment
                self.canvas.create_image(canvas_x, canvas_y, image=segment_tk, 
                                       anchor=tk.NW, tags=f"segment_{segment['id']}")
    
    def on_canvas_click(self, event):
        if not self.image_segments:
            return
        
        # Tìm segment được click
        clicked_items = self.canvas.find_closest(event.x, event.y)
        if clicked_items:
            item = clicked_items[0]
            tags = self.canvas.gettags(item)
            
            for tag in tags:
                if tag.startswith('segment_'):
                    segment_id = tag.replace('segment_', '')
                    self.selected_segment = segment_id
                    self.drag_start = (event.x, event.y)
                    break
    
    def on_canvas_drag(self, event):
        if self.selected_segment and self.drag_start:
            # Tính toán offset
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            
            # Cập nhật vị trí segment
            if self.selected_segment in self.segment_positions:
                old_x, old_y = self.segment_positions[self.selected_segment]
                
                # Chuyển đổi từ tọa độ canvas sang tọa độ ảnh
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                img_width, img_height = self.current_image.size
                
                scale_x = canvas_width / img_width
                scale_y = canvas_height / img_height
                scale = min(scale_x, scale_y) * 0.9
                
                new_x = old_x + dx / scale
                new_y = old_y + dy / scale
                
                self.segment_positions[self.selected_segment] = (new_x, new_y)
                
                # Cập nhật hiển thị
                self.update_display()
                
                # Cập nhật drag_start cho lần drag tiếp theo
                self.drag_start = (event.x, event.y)
    
    def on_canvas_release(self, event):
        self.selected_segment = None
        self.drag_start = None
    
    def reset_positions(self):
        if self.image_segments:
            for segment in self.image_segments:
                self.segment_positions[segment['id']] = segment['current_position']
            self.update_display()
            messagebox.showinfo("Thành công", "Đã reset vị trí các chi tiết!")

def main():
    root = tk.Tk()
    app = ImageManipulationTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()