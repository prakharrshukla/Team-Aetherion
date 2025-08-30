import cv2
import numpy as np
import time

def create_demo_objects():
    """Create a demo image with various objects for testing"""
    # Create a white background
    demo_image = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Draw various shapes in different colors
    objects = [
        # Red circle
        ("Red Circle", lambda img: cv2.circle(img, (150, 150), 60, (0, 0, 255), -1)),
        
        # Green rectangle
        ("Green Rectangle", lambda img: cv2.rectangle(img, (250, 100), (350, 200), (0, 255, 0), -1)),
        
        # Blue triangle
        ("Blue Triangle", lambda img: cv2.fillPoly(img, [np.array([[450, 200], [400, 100], [500, 100]], np.int32)], (255, 0, 0))),
        
        # Yellow square
        ("Yellow Square", lambda img: cv2.rectangle(img, (580, 100), (680, 200), (0, 255, 255), -1)),
        
        # Orange pentagon (approximated)
        ("Orange Pentagon", lambda img: cv2.fillPoly(img, [np.array([[150, 400], [100, 350], [125, 300], [175, 300], [200, 350]], np.int32)], (0, 165, 255))),
        
        # Purple hexagon (approximated)
        ("Purple Hexagon", lambda img: cv2.fillPoly(img, [np.array([[350, 450], [300, 400], [300, 350], [350, 300], [400, 350], [400, 400]], np.int32)], (128, 0, 128))),
        
        # Cyan oval
        ("Cyan Oval", lambda img: cv2.ellipse(img, (550, 400), (80, 40), 0, 0, 360, (255, 255, 0), -1)),
    ]
    
    print("Creating demo objects:")
    for name, draw_func in objects:
        draw_func(demo_image)
        print(f"   {name}")
    
    return demo_image

def demo_detection():
    """Run a demo of the detection system with sample objects"""
    print("\n" + "=" * 60)
    print("TEAM-AETHERION - UOWD AEROSPACE MACHINE VISION DEMO")
    print("=" * 60)
    print("\nThis demo shows the detection capabilities:")
    print("- Shape Detection: Circle, Rectangle, Triangle, Square, Pentagon, Hexagon, Oval")
    print("- Color Detection: Red, Green, Blue, Yellow, Orange, Purple, Cyan")
    print("- Edge Detection: Canny algorithm")
    print("- Object Counting and Hex Color Values")
    
    # Create demo image
    demo_image = create_demo_objects()
    
    # Save demo image
    cv2.imwrite('demo_objects.jpg', demo_image)
    print(f"\n Demo objects saved as 'demo_objects.jpg'")
    
    # Simple detection on demo image
    gray = cv2.cvtColor(demo_image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to find objects
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"\n Detected {len(contours)} objects in demo image")
    
    # Draw detection results
    result_image = demo_image.copy()
    
    for i, contour in enumerate(contours):
        # Filter small contours
        area = cv2.contourArea(contour)
        if area < 500:
            continue
            
        # Draw contour
        cv2.drawContours(result_image, [contour], -1, (0, 255, 0), 3)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Add object number
        cv2.putText(result_image, f"Obj-{i+1}", (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Display results
    print("\n" + "=" * 60)
    print("DEMO RESULTS:")
    print("=" * 60)
    print(" Objects detected and outlined in green")
    print(" Bounding boxes shown in blue") 
    print(" Object numbers displayed")
    print("\nPress any key in the image windows to continue...")
    
    # Show images
    cv2.imshow('Team-Aetherion - UOWD Aerospace Demo Objects', demo_image)
    cv2.imshow('Team-Aetherion - UOWD Aerospace Detection Results', result_image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n Demo completed successfully!")
    print("\nNow you can run the full system with your camera:")
    print("  python machine_vision.py         - Basic real-time version")
    print("  python advanced_machine_vision.py - Advanced version with tracking")

def main():
    demo_detection()

if __name__ == "__main__":
    main()
