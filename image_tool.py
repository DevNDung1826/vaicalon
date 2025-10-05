import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2

class ImageSegmentTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Segment Tool - Công cụ chia và di chuyển chi tiết ảnh")
        self.root.geometry("1400x900")
        
        # Image data
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_path = None
        
        # Transformation parameters
        self.rotation_angle = 0
        self.flip_horizontal = False
        self.flip_vertical = False
        
        # Segmentation data
        self.vertical_lines = []
        self.horizontal_lines = []
        self.segments = []
        self.segment_positions = []
        
        # Canvas scale
        self.canvas_scale = 1.0
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0
        
        # Interaction state
        self.selected_segment = None
        self.dragging_segment = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging_line = None
        self.line_type = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Load image button
        ttk.Button(control_frame, text="📁 Tải ảnh", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Flip buttons
        ttk.Label(control_frame, text="Lật:").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="↔ Ngang", command=self.flip_horizontal_action).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="↕ Dọc", command=self.flip_vertical_action).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Rotation
        ttk.Label(control_frame, text="Xoay (độ):").pack(side=tk.LEFT, padx=5)
        self.rotation_var = tk.StringVar(value="0")
        rotation_spinbox = ttk.Spinbox(control_frame, from_=0, to=360, textvariable=self.rotation_var, 
                                       width=8, command=self.rotate_image)
        rotation_spinbox.pack(side=tk.LEFT, padx=2)
        rotation_spinbox.bind('<Return>', lambda e: self.rotate_image())
        
        ttk.Button(control_frame, text="↻ Quay", command=self.rotate_image).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Segmentation controls
        ttk.Label(control_frame, text="Chia ảnh:").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="➕ Dọc", command=self.add_vertical_line).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="➕ Ngang", command=self.add_horizontal_line).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔄 Cập nhật", command=self.update_segments).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🗑 Xóa đường", command=self.clear_lines).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Reset and Save
        ttk.Button(control_frame, text="↺ Reset", command=self.reset_transformations).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Lưu", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Main canvas
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#2b2b2b', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        
        # Status bar
        self.status_var = tk.StringVar(value="Sẵn sàng. Vui lòng tải ảnh.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                
                # Reset transformations
                self.rotation_angle = 0
                self.flip_horizontal = False
                self.flip_vertical = False
                self.rotation_var.set("0")
                
                # Initialize segmentation with 2x2 grid
                self.vertical_lines = [self.current_image.width // 3, 2 * self.current_image.width // 3]
                self.horizontal_lines = [self.current_image.height // 3, 2 * self.current_image.height // 3]
                
                self.update_segments()
                self.display_canvas()
                
                self.status_var.set(f"Đã tải: {file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
    
    def flip_horizontal_action(self):
        if self.current_image:
            self.flip_horizontal = not self.flip_horizontal
            self.apply_transformations()
            self.status_var.set("Đã lật ngang")
    
    def flip_vertical_action(self):
        if self.current_image:
            self.flip_vertical = not self.flip_vertical
            self.apply_transformations()
            self.status_var.set("Đã lật dọc")
    
    def rotate_image(self):
        if self.current_image:
            try:
                self.rotation_angle = float(self.rotation_var.get()) % 360
                self.apply_transformations()
                self.status_var.set(f"Đã xoay {self.rotation_angle}°")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập góc xoay hợp lệ")
    
    def apply_transformations(self):
        if self.original_image:
            img = self.original_image.copy()
            
            # Apply flips
            if self.flip_horizontal:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            if self.flip_vertical:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            
            # Apply rotation (high quality)
            if self.rotation_angle != 0:
                img = img.rotate(-self.rotation_angle, resample=Image.BICUBIC, expand=True)
            
            self.current_image = img
            self.update_segments()
            self.display_canvas()
    
    def add_vertical_line(self):
        if self.current_image:
            # Add line at center if no lines, otherwise add between existing
            if not self.vertical_lines:
                pos = self.current_image.width // 2
            else:
                pos = sum(self.vertical_lines) // len(self.vertical_lines)
            
            self.vertical_lines.append(pos)
            self.vertical_lines.sort()
            self.display_canvas()
            self.status_var.set("Đã thêm đường dọc. Kéo để di chuyển, nhấn 'Cập nhật' để chia ảnh.")
    
    def add_horizontal_line(self):
        if self.current_image:
            if not self.horizontal_lines:
                pos = self.current_image.height // 2
            else:
                pos = sum(self.horizontal_lines) // len(self.horizontal_lines)
            
            self.horizontal_lines.append(pos)
            self.horizontal_lines.sort()
            self.display_canvas()
            self.status_var.set("Đã thêm đường ngang. Kéo để di chuyển, nhấn 'Cập nhật' để chia ảnh.")
    
    def clear_lines(self):
        self.vertical_lines = []
        self.horizontal_lines = []
        self.segments = []
        self.segment_positions = []
        self.display_canvas()
        self.status_var.set("Đã xóa tất cả đường chia")
    
    def update_segments(self):
        if not self.current_image:
            return
        
        # Create segments based on lines
        x_positions = [0] + sorted(self.vertical_lines) + [self.current_image.width]
        y_positions = [0] + sorted(self.horizontal_lines) + [self.current_image.height]
        
        self.segments = []
        self.segment_positions = []
        
        for i in range(len(y_positions) - 1):
            for j in range(len(x_positions) - 1):
                x1, x2 = x_positions[j], x_positions[j + 1]
                y1, y2 = y_positions[i], y_positions[i + 1]
                
                # Extract segment (no deformation)
                segment = self.current_image.crop((x1, y1, x2, y2))
                self.segments.append(segment)
                self.segment_positions.append([x1, y1, x2, y2])
        
        self.display_canvas()
        self.status_var.set(f"Đã tạo {len(self.segments)} chi tiết")
    
    def reset_transformations(self):
        if self.original_image:
            self.rotation_angle = 0
            self.flip_horizontal = False
            self.flip_vertical = False
            self.rotation_var.set("0")
            self.current_image = self.original_image.copy()
            self.vertical_lines = []
            self.horizontal_lines = []
            self.segments = []
            self.segment_positions = []
            self.display_canvas()
            self.status_var.set("Đã reset về trạng thái ban đầu")
    
    def display_canvas(self):
        if not self.current_image:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate scaling
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 1200
            canvas_height = 700
        
        if self.segments:
            # Calculate bounding box of all segments
            max_x = max(pos[2] for pos in self.segment_positions)
            max_y = max(pos[3] for pos in self.segment_positions)
            img_width, img_height = max_x, max_y
        else:
            img_width = self.current_image.width
            img_height = self.current_image.height
        
        scale_x = (canvas_width - 40) / img_width
        scale_y = (canvas_height - 40) / img_height
        self.canvas_scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        self.canvas_offset_x = (canvas_width - img_width * self.canvas_scale) / 2
        self.canvas_offset_y = (canvas_height - img_height * self.canvas_scale) / 2
        
        # Draw segments or full image
        if self.segments:
            for idx, (segment, pos) in enumerate(zip(self.segments, self.segment_positions)):
                x1, y1, x2, y2 = pos
                
                # Scale segment for display
                display_width = int((x2 - x1) * self.canvas_scale)
                display_height = int((y2 - y1) * self.canvas_scale)
                
                if display_width > 0 and display_height > 0:
                    segment_resized = segment.resize((display_width, display_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(segment_resized)
                    
                    canvas_x = self.canvas_offset_x + x1 * self.canvas_scale
                    canvas_y = self.canvas_offset_y + y1 * self.canvas_scale
                    
                    self.canvas.create_image(canvas_x, canvas_y, anchor=tk.NW, image=photo, tags=f"segment_{idx}")
                    self.canvas.image_refs = getattr(self.canvas, 'image_refs', [])
                    self.canvas.image_refs.append(photo)
                    
                    # Draw border around segment
                    border_x1 = canvas_x
                    border_y1 = canvas_y
                    border_x2 = canvas_x + display_width
                    border_y2 = canvas_y + display_height
                    self.canvas.create_rectangle(border_x1, border_y1, border_x2, border_y2, 
                                                outline='#00ff00', width=2, tags=f"border_{idx}")
        else:
            # Display full image with cutting lines
            display_width = int(self.current_image.width * self.canvas_scale)
            display_height = int(self.current_image.height * self.canvas_scale)
            
            if display_width > 0 and display_height > 0:
                img_resized = self.current_image.resize((display_width, display_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img_resized)
                
                self.canvas.create_image(self.canvas_offset_x, self.canvas_offset_y, 
                                        anchor=tk.NW, image=photo, tags="main_image")
                self.canvas.image_photo = photo
                
                # Draw cutting lines
                for x in self.vertical_lines:
                    canvas_x = self.canvas_offset_x + x * self.canvas_scale
                    self.canvas.create_line(canvas_x, self.canvas_offset_y,
                                          canvas_x, self.canvas_offset_y + display_height,
                                          fill='red', width=2, tags=f"vline_{x}")
                
                for y in self.horizontal_lines:
                    canvas_y = self.canvas_offset_y + y * self.canvas_scale
                    self.canvas.create_line(self.canvas_offset_x, canvas_y,
                                          self.canvas_offset_x + display_width, canvas_y,
                                          fill='red', width=2, tags=f"hline_{y}")
    
    def on_canvas_click(self, event):
        if not self.current_image:
            return
        
        # Check if clicking on a cutting line
        if not self.segments:
            for idx, x in enumerate(self.vertical_lines):
                canvas_x = self.canvas_offset_x + x * self.canvas_scale
                if abs(event.x - canvas_x) < 10:
                    self.dragging_line = idx
                    self.line_type = 'vertical'
                    return
            
            for idx, y in enumerate(self.horizontal_lines):
                canvas_y = self.canvas_offset_y + y * self.canvas_scale
                if abs(event.y - canvas_y) < 10:
                    self.dragging_line = idx
                    self.line_type = 'horizontal'
                    return
        
        # Check if clicking on a segment
        if self.segments:
            for idx, pos in enumerate(self.segment_positions):
                x1, y1, x2, y2 = pos
                canvas_x1 = self.canvas_offset_x + x1 * self.canvas_scale
                canvas_y1 = self.canvas_offset_y + y1 * self.canvas_scale
                canvas_x2 = self.canvas_offset_x + x2 * self.canvas_scale
                canvas_y2 = self.canvas_offset_y + y2 * self.canvas_scale
                
                if canvas_x1 <= event.x <= canvas_x2 and canvas_y1 <= event.y <= canvas_y2:
                    self.selected_segment = idx
                    self.dragging_segment = True
                    self.drag_start_x = event.x
                    self.drag_start_y = event.y
                    self.status_var.set(f"Đang kéo chi tiết {idx + 1}")
                    break
    
    def on_canvas_drag(self, event):
        if self.dragging_line is not None:
            if self.line_type == 'vertical':
                new_x = (event.x - self.canvas_offset_x) / self.canvas_scale
                new_x = max(1, min(new_x, self.current_image.width - 1))
                self.vertical_lines[self.dragging_line] = int(new_x)
            elif self.line_type == 'horizontal':
                new_y = (event.y - self.canvas_offset_y) / self.canvas_scale
                new_y = max(1, min(new_y, self.current_image.height - 1))
                self.horizontal_lines[self.dragging_line] = int(new_y)
            
            self.display_canvas()
        
        elif self.dragging_segment and self.selected_segment is not None:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            # Update segment position
            pos = self.segment_positions[self.selected_segment]
            dx_img = dx / self.canvas_scale
            dy_img = dy / self.canvas_scale
            
            pos[0] += dx_img
            pos[1] += dy_img
            pos[2] += dx_img
            pos[3] += dy_img
            
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
            self.display_canvas()
    
    def on_canvas_release(self, event):
        if self.dragging_line is not None:
            self.dragging_line = None
            self.line_type = None
            self.status_var.set("Di chuyển đường thành công. Nhấn 'Cập nhật' để chia lại ảnh.")
        
        if self.dragging_segment:
            self.dragging_segment = False
            self.status_var.set(f"Đã di chuyển chi tiết {self.selected_segment + 1}")
    
    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để lưu")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Lưu ảnh",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if self.segments:
                    # Create composite image from segments
                    max_x = int(max(pos[2] for pos in self.segment_positions))
                    max_y = int(max(pos[3] for pos in self.segment_positions))
                    
                    # Create transparent canvas
                    composite = Image.new('RGBA', (max_x + 100, max_y + 100), (0, 0, 0, 0))
                    
                    for segment, pos in zip(self.segments, self.segment_positions):
                        x1, y1 = int(pos[0]), int(pos[1])
                        composite.paste(segment, (x1, y1))
                    
                    # Convert to RGB for saving as JPEG
                    if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                        rgb_composite = Image.new('RGB', composite.size, (255, 255, 255))
                        rgb_composite.paste(composite, mask=composite.split()[3] if composite.mode == 'RGBA' else None)
                        rgb_composite.save(file_path, quality=95)
                    else:
                        composite.save(file_path)
                else:
                    self.current_image.save(file_path, quality=95)
                
                self.status_var.set(f"Đã lưu: {file_path}")
                messagebox.showinfo("Thành công", "Đã lưu ảnh thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageSegmentTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
