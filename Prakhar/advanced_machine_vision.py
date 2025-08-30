import cv2
import numpy as np
import threading
from collections import defaultdict, deque
import time
import json
import os

class AdvancedMachineVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.running = False
        self.object_history = deque(maxlen=1000)
        self.tracking_objects = {}
        self.next_id = 0
        
        # Enhanced color ranges with more precise detection
        self.color_ranges = {
            'Red': [[(0, 100, 100), (10, 255, 255)], [(170, 100, 100), (180, 255, 255)]],
            'Green': [[(40, 100, 100), (80, 255, 255)]],
            'Blue': [[(100, 100, 100), (130, 255, 255)]],
            'Yellow': [[(20, 100, 100), (40, 255, 255)]],
            'Orange': [[(10, 100, 100), (25, 255, 255)]],
            'Purple': [[(130, 100, 100), (170, 255, 255)]],
            'Cyan': [[(80, 100, 100), (100, 255, 255)]],
            'Pink': [[(140, 50, 50), (170, 255, 255)]],
            'White': [[(0, 0, 200), (180, 30, 255)]],
            'Black': [[(0, 0, 0), (180, 255, 50)]]
        }
        
        # Initialize counters
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        
        # Detection parameters
        self.min_area = 300
        self.max_area = 50000
        
    def calculate_fps(self):
        """Calculate FPS"""
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time
    
    def enhanced_color_detection(self, hsv_frame, contour):
        """Enhanced color detection with better accuracy"""
        mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [contour], 255)
        
        best_color = 'Unknown'
        max_pixels = 0
        
        for color_name, ranges_list in self.color_ranges.items():
            total_pixels = 0
            
            for ranges in ranges_list:
                lower, upper = ranges
                color_mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
                intersection = cv2.bitwise_and(mask, color_mask)
                pixels = cv2.countNonZero(intersection)
                total_pixels += pixels
            
            if total_pixels > max_pixels and total_pixels > 100:
                max_pixels = total_pixels
                best_color = color_name
        
        return best_color
    
    def advanced_shape_detection(self, contour):
        """Advanced shape detection with better accuracy"""
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return "Unknown"
        
        # Approximate polygon
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)
        
        # Calculate additional properties
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0
        
        # Bounding rectangle properties
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h if h > 0 else 0
        extent = area / (w * h) if (w * h) > 0 else 0
        
        # Circularity
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Shape classification
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            if 0.95 <= aspect_ratio <= 1.05:
                return "Square"
            else:
                return "Rectangle"
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        elif circularity > 0.7:
            return "Circle"
        elif circularity > 0.5:
            return "Oval"
        elif vertices > 6:
            if solidity > 0.9:
                return "Star"
            else:
                return "Complex"
        else:
            return "Irregular"
    
    def get_precise_hex_color(self, frame, contour):
        """Get precise hex color with statistical analysis"""
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [contour], 255)
        
        # Get pixels within the contour
        pixels = frame[mask > 0]
        
        if len(pixels) == 0:
            return "#000000", [0, 0, 0]
        
        # Calculate median color (more robust than mean)
        median_color = np.median(pixels, axis=0)
        
        # Convert BGR to hex
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(median_color[2]), int(median_color[1]), int(median_color[0])
        )
        
        return hex_color, median_color
    
    def advanced_edge_detection(self, frame):
        """Advanced multi-level edge detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply different edge detection methods
        # Canny
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 50, 150)
        
        # Sobel
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.uint8(sobel / sobel.max() * 255)
        
        # Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        
        # Combine edge detection results
        combined = cv2.bitwise_or(canny, cv2.bitwise_or(sobel, laplacian))
        
        return canny, sobel, laplacian, combined
    
    def object_tracking(self, detected_objects):
        """Simple object tracking between frames"""
        current_objects = {}
        
        for obj in detected_objects:
            center = obj['center']
            matched_id = None
            min_distance = float('inf')
            
            # Find closest existing object
            for obj_id, tracked_obj in self.tracking_objects.items():
                distance = np.sqrt((center[0] - tracked_obj['center'][0])**2 + 
                                 (center[1] - tracked_obj['center'][1])**2)
                
                if distance < min_distance and distance < 50:  # Threshold for matching
                    min_distance = distance
                    matched_id = obj_id
            
            if matched_id is not None:
                # Update existing object
                obj['id'] = matched_id
                obj['age'] = self.tracking_objects[matched_id]['age'] + 1
                current_objects[matched_id] = obj
            else:
                # New object
                obj['id'] = self.next_id
                obj['age'] = 1
                current_objects[self.next_id] = obj
                self.next_id += 1
        
        self.tracking_objects = current_objects
        return list(current_objects.values())
    
    def process_frame_advanced(self, frame):
        """Advanced frame processing with multiple detection methods"""
        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Advanced edge detection
        canny, sobel, laplacian, combined_edges = self.advanced_edge_detection(frame)
        
        # Multiple preprocessing methods
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Adaptive thresholding
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                              cv2.THRESH_BINARY, 11, 2)
        
        # Method 2: Morphological operations
        kernel = np.ones((3,3), np.uint8)
        morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_objects = []
        object_counts = defaultdict(int)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < self.min_area or area > self.max_area:
                continue
            
            # Get contour properties
            x, y, w, h = cv2.boundingRect(contour)
            center_x, center_y = x + w//2, y + h//2
            
            # Advanced shape detection
            shape = self.advanced_shape_detection(contour)
            
            # Enhanced color detection
            color = self.enhanced_color_detection(hsv, contour)
            
            # Precise hex color
            hex_color, median_color = self.get_precise_hex_color(frame, contour)
            
            # Calculate additional properties
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # Draw enhanced visualization
            # Contour outline
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Center point
            cv2.circle(frame, (center_x, center_y), 7, (0, 0, 255), -1)
            cv2.circle(frame, (center_x, center_y), 3, (255, 255, 255), -1)
            
            # Store detailed object info
            obj_info = {
                'shape': shape,
                'color': color,
                'hex': hex_color,
                'area': area,
                'perimeter': perimeter,
                'circularity': circularity,
                'center': (center_x, center_y),
                'bbox': (x, y, w, h),
                'contour': contour,
                'median_color': median_color
            }
            detected_objects.append(obj_info)
            
            # Count objects
            object_key = f"{color} {shape}"
            object_counts[object_key] += 1
        
        # Object tracking
        tracked_objects = self.object_tracking(detected_objects)
        
        return frame, tracked_objects, object_counts, {
            'canny': canny,
            'sobel': sobel,
            'laplacian': laplacian,
            'combined': combined_edges
        }
    
    def draw_advanced_info_panel(self, frame, detected_objects, object_counts):
        """Draw advanced information panel with detailed stats"""
        height, width = frame.shape[:2]
        panel_width = 350
        
        # Create extended frame
        extended_frame = np.zeros((height, width + panel_width, 3), dtype=np.uint8)
        extended_frame[:, :width] = frame
        
        # Panel background with gradient
        for i in range(height):
            intensity = int(30 + (i / height) * 20)
            extended_frame[i, width:] = [intensity, intensity, intensity]
        
        # Header
        cv2.rectangle(extended_frame, (width, 0), (width + panel_width, 80), (0, 100, 200), -1)
        cv2.putText(extended_frame, "TEAM-AETHERION - UOWD AEROSPACE", (width + 10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(extended_frame, "Advanced Machine Vision", (width + 10, 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 255), 1)
        cv2.putText(extended_frame, f"FPS: {self.fps}", (width + 10, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        y_offset = 100
        
        # Summary statistics
        total_objects = len(detected_objects)
        cv2.putText(extended_frame, f"Total Objects: {total_objects}", (width + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 30
        
        # Object type counts
        cv2.putText(extended_frame, "Object Counts:", (width + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        y_offset += 20
        
        for obj_type, count in list(object_counts.items())[:6]:
            cv2.putText(extended_frame, f"  {obj_type}: {count}", (width + 15, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 18
        
        y_offset += 10
        
        # Individual object details
        cv2.putText(extended_frame, "Detailed Analysis:", (width + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        y_offset += 25
        
        for i, obj in enumerate(detected_objects[:6]):
            if 'id' in obj:
                cv2.putText(extended_frame, f"ID-{obj['id']}: {obj['color']} {obj['shape']}", 
                           (width + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            else:
                cv2.putText(extended_frame, f"Obj-{i+1}: {obj['color']} {obj['shape']}", 
                           (width + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 15
            
            # Properties
            cv2.putText(extended_frame, f"  Area: {int(obj['area'])}", 
                       (width + 15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
            y_offset += 12
            
            cv2.putText(extended_frame, f"  Hex: {obj['hex']}", 
                       (width + 15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
            
            # Color swatch
            try:
                color_bgr = [int(obj['hex'][5:7], 16), int(obj['hex'][3:5], 16), int(obj['hex'][1:3], 16)]
                cv2.rectangle(extended_frame, (width + 200, y_offset - 10), (width + 230, y_offset + 2), color_bgr, -1)
                cv2.rectangle(extended_frame, (width + 200, y_offset - 10), (width + 230, y_offset + 2), (255, 255, 255), 1)
            except:
                pass
            
            y_offset += 15
            
            if 'circularity' in obj:
                cv2.putText(extended_frame, f"  Circularity: {obj['circularity']:.2f}", 
                           (width + 15, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
                y_offset += 12
            
            y_offset += 8
        
        return extended_frame
    
    def save_detection_data(self, detected_objects, filename_prefix="detection"):
        """Save detection data to JSON file"""
        timestamp = int(time.time())
        filename = f"{filename_prefix}_{timestamp}.json"
        
        # Prepare data for JSON (remove non-serializable objects)
        data = []
        for obj in detected_objects:
            obj_data = {
                'shape': obj['shape'],
                'color': obj['color'],
                'hex': obj['hex'],
                'area': int(obj['area']),
                'center': obj['center'],
                'bbox': obj['bbox'],
                'timestamp': timestamp
            }
            if 'id' in obj:
                obj_data['id'] = obj['id']
                obj_data['age'] = obj['age']
            if 'circularity' in obj:
                obj_data['circularity'] = float(obj['circularity'])
            
            data.append(obj_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def start_advanced_detection(self):
        """Start advanced detection system"""
        self.running = True
        print("Starting Advanced Machine Vision System...")
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save screenshot")
        print("  'd' - Save detection data")
        print("  '1' - Show Canny edges")
        print("  '2' - Show Sobel edges")
        print("  '3' - Show Laplacian edges")
        print("  '4' - Show combined edges")
        
        show_edges = None
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            # Calculate FPS
            self.calculate_fps()
            
            # Process frame
            processed_frame, detected_objects, object_counts, edge_maps = self.process_frame_advanced(frame.copy())
            
            # Draw info panel
            display_frame = self.draw_advanced_info_panel(processed_frame, detected_objects, object_counts)
            
            # Display main frame
            cv2.imshow('Team-Aetherion - UOWD Aerospace Advanced Machine Vision', display_frame)
            
            # Show edge detection if requested
            if show_edges and show_edges in edge_maps:
                edge_display = cv2.cvtColor(edge_maps[show_edges], cv2.COLOR_GRAY2BGR)
                cv2.imshow(f'Edge Detection - {show_edges.title()}', edge_display)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = int(time.time())
                filename = f'uowd_aerospace_screenshot_{timestamp}.jpg'
                cv2.imwrite(filename, display_frame)
                print(f"Screenshot saved: {filename}")
            elif key == ord('d'):
                filename = self.save_detection_data(detected_objects)
                print(f"Detection data saved: {filename}")
            elif key == ord('1'):
                show_edges = 'canny'
            elif key == ord('2'):
                show_edges = 'sobel'
            elif key == ord('3'):
                show_edges = 'laplacian'
            elif key == ord('4'):
                show_edges = 'combined'
            elif key == ord('0'):
                show_edges = None
                cv2.destroyWindow('Edge Detection - Canny')
                cv2.destroyWindow('Edge Detection - Sobel')
                cv2.destroyWindow('Edge Detection - Laplacian')
                cv2.destroyWindow('Edge Detection - Combined')
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Machine Vision System shut down successfully")

def main():
    print("=" * 60)
    print("TEAM-AETHERION - UOWD AEROSPACE ADVANCED MACHINE VISION SYSTEM")
    print("=" * 60)
    print("\nAdvanced Features:")
    print(" Multi-level Object Detection")
    print(" Enhanced Shape Recognition (10+ shapes)")
    print(" Precise Color Detection with Hex Values")
    print(" Real-time Object Tracking with IDs")
    print(" Advanced Edge Detection (Canny, Sobel, Laplacian)")
    print(" Object Circling and Bounding Boxes")
    print(" Statistical Analysis (Area, Circularity, etc.)")
    print(" Data Export to JSON")
    print(" FPS Counter and Performance Metrics")
    print("\nInitializing camera...")
    
    vision_system = AdvancedMachineVision()
    
    # Check if camera is available
    if not vision_system.cap.isOpened():
        print("Error: Could not access camera!")
        print("Please check if your camera is connected and not in use by another application.")
        return
    
    try:
        vision_system.start_advanced_detection()
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user...")
        vision_system.cleanup()
    except Exception as e:
        print(f"\nError occurred: {e}")
        vision_system.cleanup()

if __name__ == "__main__":
    main()
