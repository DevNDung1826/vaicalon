import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2

class ImageSegmentTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Segment Tool - Công cụ phát hiện và di chuyển chi tiết ảnh")
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
        
        # Segmentation data - now segments are independent objects
        self.segments = []  # List of segment images
        self.segment_positions = []  # Absolute positions [x, y, width, height]
        self.segment_contours = []  # Store contour info
        
        # Canvas properties - expandable workspace
        self.canvas_scale = 1.0
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0
        self.workspace_width = 3000  # Large workspace
        self.workspace_height = 3000
        
        # Interaction state
        self.selected_segment = None
        self.dragging_segment = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Detection parameters
        self.threshold_value = tk.IntVar(value=127)
        self.min_area = tk.IntVar(value=100)
        
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
        
        # Auto detection controls
        ttk.Label(control_frame, text="Phát hiện:").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔍 Tự động", command=self.auto_detect_segments).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⚙️ Cài đặt", command=self.show_detection_settings).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Reset and Save
        ttk.Button(control_frame, text="↺ Reset", command=self.reset_transformations).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑 Xóa chi tiết", command=self.clear_segments).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="💾 Lưu", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Main canvas with scrollbars
        canvas_container = ttk.Frame(self.root)
        canvas_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas with large scrollable area
        self.canvas = tk.Canvas(canvas_container, bg='#2b2b2b', highlightthickness=0,
                               scrollregion=(0, 0, self.workspace_width, self.workspace_height),
                               xscrollcommand=h_scrollbar.set,
                               yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.canvas.bind('<Button-3>', self.on_right_click)  # Right click for delete
        
        # Status bar
        self.status_var = tk.StringVar(value="Sẵn sàng. Vui lòng tải ảnh và nhấn 'Tự động' để phát hiện chi tiết.")
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
                
                # Clear segments
                self.segments = []
                self.segment_positions = []
                self.segment_contours = []
                
                # Center image in workspace
                self.canvas_offset_x = (self.workspace_width - self.current_image.width) // 2
                self.canvas_offset_y = (self.workspace_height - self.current_image.height) // 2
                
                self.display_canvas()
                
                self.status_var.set(f"Đã tải: {file_path} - Nhấn 'Tự động' để phát hiện chi tiết")
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
            
            # Clear segments after transformation
            self.segments = []
            self.segment_positions = []
            self.segment_contours = []
            
            self.display_canvas()
    
    def show_detection_settings(self):
        """Show dialog for detection parameters"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Cài đặt phát hiện")
        settings_window.geometry("400x250")
        settings_window.transient(self.root)
        
        frame = ttk.Frame(settings_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Threshold
        ttk.Label(frame, text="Ngưỡng phát hiện (0-255):").pack(anchor=tk.W, pady=5)
        threshold_scale = ttk.Scale(frame, from_=0, to=255, variable=self.threshold_value, 
                                   orient=tk.HORIZONTAL, length=300)
        threshold_scale.pack(pady=5)
        ttk.Label(frame, textvariable=self.threshold_value).pack()
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Min area
        ttk.Label(frame, text="Kích thước tối thiểu (pixels):").pack(anchor=tk.W, pady=5)
        area_scale = ttk.Scale(frame, from_=50, to=5000, variable=self.min_area, 
                              orient=tk.HORIZONTAL, length=300)
        area_scale.pack(pady=5)
        ttk.Label(frame, textvariable=self.min_area).pack()
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Áp dụng", command=lambda: [self.auto_detect_segments(), settings_window.destroy()]).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Đóng", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def auto_detect_segments(self):
        """Automatically detect segments using computer vision"""
        if not self.current_image:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải ảnh trước")
            return
        
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(self.current_image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, self.threshold_value.get(), 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Clear existing segments
            self.segments = []
            self.segment_positions = []
            self.segment_contours = []
            
            # Process each contour
            for contour in contours:
                area = cv2.contourArea(contour)
                
                if area < self.min_area.get():
                    continue
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Skip if too small
                if w < 10 or h < 10:
                    continue
                
                # Extract segment with some padding
                padding = 2
                x1 = max(0, x - padding)
                y1 = max(0, y - padding)
                x2 = min(self.current_image.width, x + w + padding)
                y2 = min(self.current_image.height, y + h + padding)
                
                # Crop segment
                segment = self.current_image.crop((x1, y1, x2, y2))
                
                # Store segment at original position in workspace
                abs_x = self.canvas_offset_x + x1
                abs_y = self.canvas_offset_y + y1
                
                self.segments.append(segment)
                self.segment_positions.append([abs_x, abs_y, segment.width, segment.height])
                self.segment_contours.append(contour)
            
            if len(self.segments) == 0:
                messagebox.showinfo("Thông báo", "Không phát hiện được chi tiết. Thử điều chỉnh cài đặt.")
            else:
                self.status_var.set(f"Đã phát hiện {len(self.segments)} chi tiết - Kéo thả để di chuyển")
            
            self.display_canvas()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi phát hiện chi tiết: {str(e)}")
    
    def clear_segments(self):
        """Clear all detected segments"""
        self.segments = []
        self.segment_positions = []
        self.segment_contours = []
        self.display_canvas()
        self.status_var.set("Đã xóa tất cả chi tiết")
    
    def reset_transformations(self):
        if self.original_image:
            self.rotation_angle = 0
            self.flip_horizontal = False
            self.flip_vertical = False
            self.rotation_var.set("0")
            self.current_image = self.original_image.copy()
            self.segments = []
            self.segment_positions = []
            self.segment_contours = []
            self.display_canvas()
            self.status_var.set("Đã reset về trạng thái ban đầu")
    
    def display_canvas(self):
        """Display current image and segments on canvas"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw grid for reference
        self.draw_grid()
        
        # Draw original image if no segments
        if self.current_image and not self.segments:
            img_width = self.current_image.width
            img_height = self.current_image.height
            
            # Create PhotoImage
            photo = ImageTk.PhotoImage(self.current_image)
            
            self.canvas.create_image(self.canvas_offset_x, self.canvas_offset_y, 
                                    anchor=tk.NW, image=photo, tags="original_image")
            self.canvas.image_photo = photo
            
            # Draw border
            self.canvas.create_rectangle(self.canvas_offset_x, self.canvas_offset_y,
                                        self.canvas_offset_x + img_width, 
                                        self.canvas_offset_y + img_height,
                                        outline='#555555', width=2, dash=(5, 5))
        
        # Draw all segments at their positions
        self.canvas.image_refs = []
        for idx, (segment, pos) in enumerate(zip(self.segments, self.segment_positions)):
            x, y, w, h = pos
            
            # Create PhotoImage
            photo = ImageTk.PhotoImage(segment)
            
            # Draw segment
            self.canvas.create_image(x, y, anchor=tk.NW, image=photo, tags=f"segment_{idx}")
            self.canvas.image_refs.append(photo)
            
            # Draw border
            border_color = '#00ff00' if idx == self.selected_segment else '#ffff00'
            border_width = 3 if idx == self.selected_segment else 2
            self.canvas.create_rectangle(x, y, x + w, y + h, 
                                        outline=border_color, width=border_width, 
                                        tags=f"border_{idx}")
            
            # Draw label
            self.canvas.create_text(x + 5, y + 5, text=f"#{idx+1}", 
                                  fill='white', font=('Arial', 10, 'bold'),
                                  anchor=tk.NW, tags=f"label_{idx}")
    
    def draw_grid(self):
        """Draw reference grid on canvas"""
        grid_spacing = 100
        grid_color = '#404040'
        
        # Vertical lines
        for x in range(0, self.workspace_width, grid_spacing):
            self.canvas.create_line(x, 0, x, self.workspace_height, 
                                  fill=grid_color, width=1, tags="grid")
        
        # Horizontal lines
        for y in range(0, self.workspace_height, grid_spacing):
            self.canvas.create_line(0, y, self.workspace_width, y, 
                                  fill=grid_color, width=1, tags="grid")
    
    def on_canvas_click(self, event):
        """Handle canvas click - select segment"""
        if not self.segments:
            return
        
        # Get canvas coordinates (accounting for scroll)
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Check if clicking on a segment (reverse order for top segments first)
        for idx in range(len(self.segment_positions) - 1, -1, -1):
            x, y, w, h = self.segment_positions[idx]
            
            if x <= canvas_x <= x + w and y <= canvas_y <= y + h:
                self.selected_segment = idx
                self.dragging_segment = True
                self.drag_start_x = canvas_x
                self.drag_start_y = canvas_y
                self.status_var.set(f"Đang kéo chi tiết #{idx + 1}")
                self.display_canvas()
                return
        
        # Clicked on empty space
        self.selected_segment = None
        self.display_canvas()
    
    def on_canvas_drag(self, event):
        """Handle dragging segment"""
        if not self.dragging_segment or self.selected_segment is None:
            return
        
        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Calculate movement
        dx = canvas_x - self.drag_start_x
        dy = canvas_y - self.drag_start_y
        
        # Update segment position (can go anywhere in workspace)
        pos = self.segment_positions[self.selected_segment]
        pos[0] += dx
        pos[1] += dy
        
        # Keep within workspace bounds (optional, remove if want unlimited)
        pos[0] = max(0, min(pos[0], self.workspace_width - pos[2]))
        pos[1] = max(0, min(pos[1], self.workspace_height - pos[3]))
        
        self.drag_start_x = canvas_x
        self.drag_start_y = canvas_y
        
        self.display_canvas()
    
    def on_canvas_release(self, event):
        """Handle mouse release"""
        if self.dragging_segment:
            self.dragging_segment = False
            if self.selected_segment is not None:
                pos = self.segment_positions[self.selected_segment]
                self.status_var.set(f"Chi tiết #{self.selected_segment + 1} tại vị trí ({int(pos[0])}, {int(pos[1])})")
    
    def on_right_click(self, event):
        """Handle right click - delete segment"""
        if not self.segments:
            return
        
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        for idx in range(len(self.segment_positions) - 1, -1, -1):
            x, y, w, h = self.segment_positions[idx]
            
            if x <= canvas_x <= x + w and y <= canvas_y <= y + h:
                # Delete this segment
                del self.segments[idx]
                del self.segment_positions[idx]
                del self.segment_contours[idx]
                
                if self.selected_segment == idx:
                    self.selected_segment = None
                elif self.selected_segment and self.selected_segment > idx:
                    self.selected_segment -= 1
                
                self.status_var.set(f"Đã xóa chi tiết #{idx + 1}")
                self.display_canvas()
                return
    
    def save_image(self):
        """Save the composition with segments at their positions"""
        if not self.current_image and not self.segments:
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
                    # Calculate bounding box of all segments
                    min_x = min(pos[0] for pos in self.segment_positions)
                    min_y = min(pos[1] for pos in self.segment_positions)
                    max_x = max(pos[0] + pos[2] for pos in self.segment_positions)
                    max_y = max(pos[1] + pos[3] for pos in self.segment_positions)
                    
                    # Add padding
                    padding = 50
                    min_x = max(0, int(min_x) - padding)
                    min_y = max(0, int(min_y) - padding)
                    max_x = int(max_x) + padding
                    max_y = int(max_y) + padding
                    
                    width = max_x - min_x
                    height = max_y - min_y
                    
                    # Create transparent canvas
                    composite = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    
                    # Paste all segments
                    for segment, pos in zip(self.segments, self.segment_positions):
                        x, y = int(pos[0]) - min_x, int(pos[1]) - min_y
                        
                        # Convert segment to RGBA if needed
                        if segment.mode != 'RGBA':
                            segment = segment.convert('RGBA')
                        
                        composite.paste(segment, (x, y), segment)
                    
                    # Save
                    if file_path.lower().endswith(('.jpg', '.jpeg')):
                        # Convert to RGB for JPEG
                        rgb_composite = Image.new('RGB', composite.size, (255, 255, 255))
                        rgb_composite.paste(composite, mask=composite.split()[3])
                        rgb_composite.save(file_path, quality=95)
                    else:
                        composite.save(file_path)
                else:
                    # Save current image
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
