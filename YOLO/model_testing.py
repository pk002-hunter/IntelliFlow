import os
from collections import Counter
import cv2
from ultralytics import YOLO

def detect_and_count_vehicles():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to your trained best weights
    weights_path = os.path.join(current_dir, 'runs', 'indian_driving_model', 'weights', 'best.pt')
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Could not find trained weights at: {weights_path}")

    print("Loading trained YOLO model...")
    model = YOLO(weights_path)

    # ⚠️ UPDATE THIS to the path of the image you want to test
    media_path = os.path.join(current_dir, 'testing_yolo', 'your_image.jpg')
    
    if not os.path.exists(media_path):
        print(f"Warning: Test image not found at {media_path}. Please update 'media_path' to a valid image file.")
        return

    print(f"Running detection on: {media_path}")
    
    # Run prediction (device=0 uses your RTX 4050 GPU)
    results = model(media_path, conf=0.3, device=0)
    
    for r in results:
        # Get the image frame with default bounding boxes drawn by Ultralytics
        annotated_frame = r.plot()
        
        # Extract detected class IDs and map them to class names
        cls_ids = r.boxes.cls.cpu().numpy()
        names = model.names
        detected_classes = [names[int(cls)] for cls in cls_ids]
        
        # Count occurrences of each vehicle type
        vehicle_counts = Counter(detected_classes)
        
        # Print summary to console
        print("\n==============================")
        print("    VEHICLE COUNT SUMMARY     ")
        print("==============================")
        if not vehicle_counts:
            print("No vehicles detected.")
        for vehicle, count in vehicle_counts.items():
            print(f"  • {vehicle}: {count}")
        print("==============================\n")
        
        # Overlay the counts textually onto the top-left of the display frame
        y_offset = 35
        for vehicle, count in vehicle_counts.items():
            text = f"{vehicle}: {count}"
            cv2.putText(
                annotated_frame, 
                text, 
                (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0, 255, 0),  # Bright green text
                2, 
                cv2.LINE_AA
            )
            y_offset += 35

        # Display the output window on screen
        cv2.imshow("IntelliFlow - Vehicle Detection & Count", annotated_frame)
        print("Image window open! Press any key while focusing the window to close it.")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_and_count_vehicles()