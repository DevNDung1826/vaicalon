// Canvas and context
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const canvasContainer = document.getElementById('canvasContainer');

// State management
let originalImage = null;
let currentScale = 1;
let layers = [];
let selectedLayer = null;
let isDragging = false;
let isSelecting = false;
let selectMode = false;
let dragStartX = 0;
let dragStartY = 0;
let selectionStart = { x: 0, y: 0 };
let selectionEnd = { x: 0, y: 0 };
let currentSelection = null;

// Layer class to manage moveable elements
class Layer {
    constructor(imageData, x, y, width, height, rotation = 0) {
        this.imageData = imageData;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.rotation = rotation;
        this.selected = false;
    }

    contains(x, y) {
        // Simple bounding box check (not accounting for rotation)
        return x >= this.x && x <= this.x + this.width &&
               y >= this.y && y <= this.y + this.height;
    }

    draw(context) {
        context.save();
        context.translate(this.x + this.width / 2, this.y + this.height / 2);
        context.rotate(this.rotation * Math.PI / 180);
        context.translate(-this.width / 2, -this.height / 2);
        
        // Create temporary canvas for the layer
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = this.width;
        tempCanvas.height = this.height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.putImageData(this.imageData, 0, 0);
        
        context.drawImage(tempCanvas, 0, 0);
        
        // Draw selection outline if selected
        if (this.selected) {
            context.strokeStyle = '#667eea';
            context.lineWidth = 3;
            context.setLineDash([5, 5]);
            context.strokeRect(0, 0, this.width, this.height);
            context.setLineDash([]);
        }
        
        context.restore();
    }
}

// File input handler
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                originalImage = img;
                initCanvas(img);
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Initialize canvas with image
function initCanvas(img) {
    // Set canvas size to image size
    canvas.width = img.width;
    canvas.height = img.height;
    
    // Clear layers
    layers = [];
    selectedLayer = null;
    currentSelection = null;
    
    // Draw image
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    
    updateInfo();
}

// Toggle select mode
function toggleSelectMode() {
    selectMode = !selectMode;
    const btn = document.getElementById('selectModeBtn');
    const modeInfo = document.getElementById('modeInfo');
    
    if (selectMode) {
        btn.style.background = '#667eea';
        btn.style.color = 'white';
        canvas.style.cursor = 'crosshair';
        modeInfo.textContent = 'Chọn vùng';
    } else {
        btn.style.background = '#f0f0f0';
        btn.style.color = '#333';
        canvas.style.cursor = 'move';
        modeInfo.textContent = 'Di chuyển';
    }
}

// Get mouse position relative to canvas
function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
    };
}

// Mouse down event
canvas.addEventListener('mousedown', function(e) {
    const pos = getMousePos(e);
    
    if (selectMode) {
        // Start selection
        isSelecting = true;
        selectionStart = pos;
        selectionEnd = pos;
    } else {
        // Check if clicking on a layer
        selectedLayer = null;
        for (let i = layers.length - 1; i >= 0; i--) {
            if (layers[i].contains(pos.x, pos.y)) {
                selectedLayer = layers[i];
                layers[i].selected = true;
                isDragging = true;
                dragStartX = pos.x - layers[i].x;
                dragStartY = pos.y - layers[i].y;
                break;
            } else {
                layers[i].selected = false;
            }
        }
        redraw();
    }
});

// Mouse move event
canvas.addEventListener('mousemove', function(e) {
    const pos = getMousePos(e);
    
    // Update mouse position display
    document.getElementById('mousePos').textContent = `X: ${Math.round(pos.x)}, Y: ${Math.round(pos.y)}`;
    
    if (isSelecting) {
        selectionEnd = pos;
        drawSelection();
    } else if (isDragging && selectedLayer) {
        selectedLayer.x = pos.x - dragStartX;
        selectedLayer.y = pos.y - dragStartY;
        redraw();
    }
});

// Mouse up event
canvas.addEventListener('mouseup', function(e) {
    if (isSelecting) {
        isSelecting = false;
        createLayerFromSelection();
    }
    isDragging = false;
});

// Mouse leave event
canvas.addEventListener('mouseleave', function() {
    isSelecting = false;
    isDragging = false;
});

// Create layer from selection
function createLayerFromSelection() {
    if (!originalImage) return;
    
    const x = Math.min(selectionStart.x, selectionEnd.x);
    const y = Math.min(selectionStart.y, selectionEnd.y);
    const width = Math.abs(selectionEnd.x - selectionStart.x);
    const height = Math.abs(selectionEnd.y - selectionStart.y);
    
    if (width < 5 || height < 5) {
        redraw();
        return;
    }
    
    // Get image data from selection
    const imageData = ctx.getImageData(x, y, width, height);
    
    // Clear the selected area
    ctx.clearRect(x, y, width, height);
    
    // Redraw the base image
    ctx.drawImage(originalImage, 0, 0);
    
    // Redraw existing layers
    for (let layer of layers) {
        layer.draw(ctx);
    }
    
    // Create new layer
    const layer = new Layer(imageData, x, y, width, height);
    layer.selected = true;
    layers.push(layer);
    
    // Deselect other layers
    for (let i = 0; i < layers.length - 1; i++) {
        layers[i].selected = false;
    }
    
    selectedLayer = layer;
    currentSelection = { x, y, width, height };
    
    redraw();
    updateInfo();
    
    // Show delete button
    document.getElementById('deleteBtn').style.display = 'inline-flex';
}

// Draw selection rectangle
function drawSelection() {
    redraw();
    
    const x = Math.min(selectionStart.x, selectionEnd.x);
    const y = Math.min(selectionStart.y, selectionEnd.y);
    const width = Math.abs(selectionEnd.x - selectionStart.x);
    const height = Math.abs(selectionEnd.y - selectionStart.y);
    
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(x, y, width, height);
    ctx.fillStyle = 'rgba(102, 126, 234, 0.1)';
    ctx.fillRect(x, y, width, height);
    ctx.setLineDash([]);
}

// Redraw canvas
function redraw() {
    if (!originalImage) return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(originalImage, 0, 0);
    
    for (let layer of layers) {
        layer.draw(ctx);
    }
}

// Delete selected layer
function deleteSelected() {
    if (selectedLayer) {
        const index = layers.indexOf(selectedLayer);
        if (index > -1) {
            layers.splice(index, 1);
        }
        selectedLayer = null;
        currentSelection = null;
        redraw();
        updateInfo();
        
        if (layers.length === 0) {
            document.getElementById('deleteBtn').style.display = 'none';
        }
    }
}

// Zoom functionality
function zoom(factor) {
    currentScale *= factor;
    currentScale = Math.max(0.1, Math.min(5, currentScale));
    
    canvas.style.transform = `scale(${currentScale})`;
    canvas.style.transformOrigin = 'top left';
    
    document.getElementById('zoomLevel').textContent = Math.round(currentScale * 100) + '%';
}

// Rotate selection
function rotateSelection(angle) {
    if (selectedLayer) {
        selectedLayer.rotation += angle;
        redraw();
    }
}

// Reset canvas
function resetCanvas() {
    if (originalImage) {
        initCanvas(originalImage);
        currentScale = 1;
        canvas.style.transform = 'scale(1)';
        document.getElementById('zoomLevel').textContent = '100%';
        document.getElementById('deleteBtn').style.display = 'none';
    }
}

// Save image
function saveImage() {
    if (!originalImage) {
        alert('Vui lòng tải ảnh lên trước!');
        return;
    }
    
    // Create a temporary canvas with final composition
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Draw everything
    tempCtx.drawImage(originalImage, 0, 0);
    for (let layer of layers) {
        layer.draw(tempCtx);
    }
    
    // Download
    tempCanvas.toBlob(function(blob) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'edited-image-' + Date.now() + '.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
}

// Update info panel
function updateInfo() {
    const selectionInfo = document.getElementById('selectionInfo');
    
    if (selectedLayer) {
        selectionInfo.textContent = `${Math.round(selectedLayer.width)}x${Math.round(selectedLayer.height)} px`;
    } else if (layers.length > 0) {
        selectionInfo.textContent = `${layers.length} vùng đã tạo`;
    } else {
        selectionInfo.textContent = 'Không có';
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === 'Delete' && selectedLayer) {
        deleteSelected();
    } else if (e.key === 'Escape') {
        if (selectMode) {
            toggleSelectMode();
        }
        if (selectedLayer) {
            selectedLayer.selected = false;
            selectedLayer = null;
            redraw();
        }
    } else if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveImage();
    }
});

// Initialize
console.log('Image manipulation tool loaded!');
console.log('Shortcuts: Delete (xóa), Escape (hủy), Ctrl+S (lưu)');
