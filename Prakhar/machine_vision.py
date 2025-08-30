import cv2
import numpy as np
import threading
from collections import defaultdict
import time

class MachineVisionSystem:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.running = False
        self.object_counts = defaultdict(int)
        self.detected_objects = []
        
        # Color ranges for detection (HSV)
        self.color_ranges = {
            'Red': [(0, 50, 50), (10, 255, 255), (170, 50, 50), (180, 255, 255)],
            'Green': [(40, 50, 50), (80, 255, 255)],
            'Blue': [(100, 50, 50), (130, 255, 255)],
            'Yellow': [(20, 50, 50), (40, 255, 255)],
            'Orange': [(10, 50, 50), (25, 255, 255)],
            'Purple': [(130, 50, 50), (170, 255, 255)]
        }
        
        # Shape detection parameters
        self.shape_detector = ShapeDetector()
        
    def detect_color(self, hsv_frame, contour):
        """Detect the dominant color of a contour"""
        mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [contour], 255)
        
        for color_name, ranges in self.color_ranges.items():
            color_mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
            
            if len(ranges) == 4:  # Red has two ranges
                lower1, upper1, lower2, upper2 = ranges
                mask1 = cv2.inRange(hsv_frame, np.array(lower1), np.array(upper1))
                mask2 = cv2.inRange(hsv_frame, np.array(lower2), np.array(upper2))
                color_mask = cv2.bitwise_or(mask1, mask2)
            else:
                lower, upper = ranges
                color_mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
            
            # Check intersection with object mask
            intersection = cv2.bitwise_and(mask, color_mask)
            if cv2.countNonZero(intersection) > 50:  # Threshold for color detection
                return color_name
        
        return 'Unknown'
    
    def get_dominant_color_hex(self, frame, contour):
        """Get the hex value of the dominant color in the contour"""
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [contour], 255)
        
        # Get pixels within the contour
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        pixels = masked_frame[mask > 0]
        
        if len(pixels) > 0:
            # Calculate mean color
            mean_color = np.mean(pixels, axis=0)
            # Convert BGR to hex
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(mean_color[2]), int(mean_color[1]), int(mean_color[0])
            )
            return hex_color, mean_color
        
        return "#000000", [0, 0, 0]
    
    def detect_edges(self, frame):
        """Detect edges using Canny edge detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    def process_frame(self, frame):
        """Process a single frame for object detection"""
        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Edge detection
        edges = self.detect_edges(frame)
        
        # Find contours
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_objects = []
        object_counts = defaultdict(int)
        
        for contour in contours:
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < 500:
                continue
            
            # Get contour properties
            x, y, w, h = cv2.boundingRect(contour)
            center_x, center_y = x + w//2, y + h//2
            
            # Detect shape
            shape = self.shape_detector.detect(contour)
            
            # Detect color
            color = self.detect_color(hsv, contour)
            
            # Get hex color
            hex_color, mean_color = self.get_dominant_color_hex(frame, contour)
            
            # Circle the object
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Draw center point
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            
            # Store object info
            obj_info = {
                'shape': shape,
                'color': color,
                'hex': hex_color,
                'area': area,
                'center': (center_x, center_y),
                'bbox': (x, y, w, h),
                'contour': contour
            }
            detected_objects.append(obj_info)
            
            # Count objects by shape and color
            object_key = f"{color} {shape}"
            object_counts[object_key] += 1
        
        return frame, detected_objects, object_counts, edges
    
    def draw_info_panel(self, frame, detected_objects, object_counts):
        """Draw information panel on the side of the frame"""
        height, width = frame.shape[:2]
        
        # Create extended frame for info panel
        panel_width = 300
        extended_frame = np.zeros((height, width + panel_width, 3), dtype=np.uint8)
        extended_frame[:, :width] = frame
        
        # Draw info panel background
        cv2.rectangle(extended_frame, (width, 0), (width + panel_width, height), (50, 50, 50), -1)
        
        # Title
        cv2.putText(extended_frame, "Team-Aetherion - UOWD Aerospace", (width + 10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(extended_frame, "Machine Vision", (width + 10, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw line separator
        cv2.line(extended_frame, (width + 10, 70), (width + panel_width - 10, 70), (255, 255, 255), 1)
        
        y_offset = 90
        
        # Object counts
        cv2.putText(extended_frame, "Object Counts:", (width + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 25
        
        for obj_type, count in object_counts.items():
            cv2.putText(extended_frame, f"{obj_type}: {count}", (width + 10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
        
        y_offset += 20
        
        # Individual object details
        cv2.putText(extended_frame, "Object Details:", (width + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 25
        
        for i, obj in enumerate(detected_objects[:8]):  # Show first 8 objects
            # Object info
            cv2.putText(extended_frame, f"Obj {i+1}: {obj['color']} {obj['shape']}", 
                       (width + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 15
            
            # Hex color
            cv2.putText(extended_frame, f"Hex: {obj['hex']}", 
                       (width + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            
            # Color swatch
            color_bgr = [int(obj['hex'][5:7], 16), int(obj['hex'][3:5], 16), int(obj['hex'][1:3], 16)]
            cv2.rectangle(extended_frame, (width + 150, y_offset - 12), (width + 180, y_offset - 2), color_bgr, -1)
            cv2.rectangle(extended_frame, (width + 150, y_offset - 12), (width + 180, y_offset - 2), (255, 255, 255), 1)
            
            y_offset += 20
            
            # Area
            cv2.putText(extended_frame, f"Area: {int(obj['area'])}", 
                       (width + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            y_offset += 25
        
        return extended_frame
    
    def start_detection(self):
        """Start the real-time detection system"""
        self.running = True
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Process frame
            processed_frame, detected_objects, object_counts, edges = self.process_frame(frame.copy())
            
            # Draw info panel
            display_frame = self.draw_info_panel(processed_frame, detected_objects, object_counts)
            
            # Show edge detection in a separate window
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # Display frames
            cv2.imshow('Team-Aetherion - UOWD Aerospace Machine Vision System', display_frame)
            cv2.imshow('Edge Detection', edges_colored)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save screenshot
                timestamp = int(time.time())
                cv2.imwrite(f'screenshot_{timestamp}.jpg', display_frame)
                print(f"Screenshot saved as screenshot_{timestamp}.jpg")
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

class ShapeDetector:
    def __init__(self):
        pass
    
    def detect(self, contour):
        """Detect the shape of a contour"""
        # Calculate contour perimeter and approximate polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        
        # Get the number of vertices
        vertices = len(approx)
        
        # Classify based on vertices and other properties
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            # Check if it's a square or rectangle
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                return "Square"
            else:
                return "Rectangle"
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        else:
            # Check if it's a circle
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if circularity > 0.7:
                return "Circle"
            else:
                return "Complex"

def main():
    print("Team-Aetherion - UOWD Aerospace Machine Vision System")
    print("====================================")
    print("Features:")
    print("- Object Detection with Shape and Color Recognition")
    print("- Real-time Counting and Quantification")
    print("- Hex Color Value Display")
    print("- Edge Detection")
    print("- Object Circling and Bounding Boxes")
    print("\nControls:")
    print("- Press 'q' to quit")
    print("- Press 's' to save screenshot")
    print("\nStarting camera...")
    
    # Initialize and start the machine vision system
    vision_system = MachineVisionSystem()
    
    try:
        vision_system.start_detection()
    except KeyboardInterrupt:
        print("\nShutting down...")
        vision_system.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        vision_system.cleanup()

if __name__ == "__main__":
    main()
