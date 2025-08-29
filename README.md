# Team-Aetherion - UOWD Aerospace Machine Vision System

Advanced computer vision system for object detection, shape recognition, color analysis, and real-time tracking.

## Features

### Core Capabilities
- **Real-time Object Detection** with live camera feed
- **Shape Recognition** - Detects: Circle, Square, Rectangle, Triangle, Pentagon, Hexagon, Oval, Star, Complex shapes
- **Color Detection** - Recognizes: Red, Green, Blue, Yellow, Orange, Purple, Cyan, Pink, White, Black
- **Hex Color Values** - Displays precise hex codes for detected colors
- **Object Quantification** - Real-time counting of detected objects
- **Edge Detection** - Multiple algorithms (Canny, Sobel, Laplacian)
- **Object Circling** - Automatic contour detection and highlighting
- **Bounding Boxes** - Precise object localization

### Advanced Features
- **Object Tracking** - Assigns unique IDs to objects across frames
- **Statistical Analysis** - Area, perimeter, circularity measurements
- **FPS Counter** - Real-time performance monitoring
- **Data Export** - Save detection results to JSON files
- **Multi-level Edge Detection** - Switchable edge detection methods
- **Enhanced Color Analysis** - Statistical color detection with median values

## Installation

1. **Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Required Libraries:**
- OpenCV (cv2) - Computer vision processing
- NumPy - Numerical operations
- Pillow - Image processing support

## Usage

### Basic Machine Vision System
```bash
python machine_vision.py
```

### Advanced Machine Vision System
```bash
python advanced_machine_vision.py
```

## Controls

### Basic Version
- **'q'** - Quit application
- **'s'** - Save screenshot

### Advanced Version
- **'q'** - Quit application
- **'s'** - Save screenshot with timestamp
- **'d'** - Save detection data to JSON file
- **'1'** - Show Canny edge detection
- **'2'** - Show Sobel edge detection
- **'3'** - Show Laplacian edge detection
- **'4'** - Show combined edge detection
- **'0'** - Hide edge detection windows

## System Requirements

- **Camera**: USB webcam or built-in camera
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM recommended
- **Processor**: Multi-core processor recommended for real-time processing

## Output Information Panel

The system displays a comprehensive information panel showing:

### Real-time Statistics
- Total object count
- FPS (Frames Per Second)
- Object counts by type (color + shape)

### Individual Object Details
- Object ID (in advanced version)
- Shape classification
- Color identification
- Hex color value with visual swatch
- Area measurement
- Circularity index
- Center coordinates

## Object Detection Capabilities

### Shape Detection
- **Triangle** - 3-sided polygons
- **Square** - 4-sided with equal aspect ratio
- **Rectangle** - 4-sided with different aspect ratio
- **Pentagon** - 5-sided polygons
- **Hexagon** - 6-sided polygons
- **Circle** - High circularity objects
- **Oval** - Medium circularity objects
- **Star** - High solidity complex shapes
- **Complex** - Multi-sided irregular shapes

### Color Detection
Detects colors in HSV color space for better accuracy:
- **Primary Colors**: Red, Green, Blue
- **Secondary Colors**: Yellow, Orange, Purple, Cyan
- **Neutral Colors**: White, Black, Pink
- **Custom Ranges**: Adjustable HSV ranges for each color

### Edge Detection Methods
1. **Canny Edge Detection** - Optimal edge detection with hysteresis
2. **Sobel Edge Detection** - Gradient-based edge detection
3. **Laplacian Edge Detection** - Second derivative edge detection
4. **Combined Detection** - Fusion of all methods

## Technical Specifications

### Detection Parameters
- **Minimum Object Area**: 300 pixels (adjustable)
- **Maximum Object Area**: 50,000 pixels (adjustable)
- **Color Detection Threshold**: 100 pixels minimum
- **Edge Detection**: Multi-method approach
- **Tracking Distance**: 50 pixels maximum for ID matching

### Performance Optimization
- **Adaptive Thresholding** for varying lighting conditions
- **Morphological Operations** for noise reduction
- **Contour Approximation** for shape simplification
- **Statistical Color Analysis** using median values

## Data Export Format

Detection data is exported as JSON with the following structure:
```json
[
  {
    "id": 1,
    "shape": "Circle",
    "color": "Red",
    "hex": "#ff0000",
    "area": 1250,
    "center": [320, 240],
    "bbox": [300, 220, 40, 40],
    "circularity": 0.85,
    "age": 15,
    "timestamp": 1693420800
  }
]
```

## Troubleshooting

### Camera Issues
- Ensure camera is not in use by another application
- Check camera permissions in system settings
- Try different camera indices (0, 1, 2, etc.)

### Performance Issues
- Close unnecessary applications
- Reduce camera resolution if needed
- Adjust minimum object area to filter small objects

### Detection Accuracy
- Ensure good lighting conditions
- Use contrasting backgrounds
- Clean camera lens
- Adjust color ranges if needed

## Customization

### Adjusting Color Ranges
Modify the `color_ranges` dictionary in the code to fine-tune color detection:
```python
self.color_ranges = {
    'CustomColor': [[(H_min, S_min, V_min), (H_max, S_max, V_max)]]
}
```

### Changing Detection Parameters
Adjust these variables for different detection sensitivity:
```python
self.min_area = 300  # Minimum object size
self.max_area = 50000  # Maximum object size
```

## Applications

This machine vision system can be used for:
- **Quality Control** in manufacturing
- **Object Sorting** and classification
- **Educational Demonstrations** of computer vision
- **Research Projects** in aerospace and engineering
- **Inventory Management** with visual counting
- **Robotics Applications** for object recognition

## Development Team

UOWD Aerospace Engineering Department
Advanced Machine Vision Laboratory

---

For technical support or feature requests, please refer to the documentation or contact the development team.
