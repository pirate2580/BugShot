import cv2
from ultralytics import YOLO

# TODO: try wrapping function with modal
def infer_from_webcam(model_path):
    """
    Performs inference using a YOLOv8 model from a webcam feed.
    
    Args:
        model_path (str): Path to the fine-tuned YOLOv8 model file.
    """
    # Load the YOLOv8 model
    model = YOLO(model_path)
    
    # Initialize the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    
    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Press 'q' to exit.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Couldn't read a frame from the webcam.")
            break
        
        # Run inference on the current frame
        results = model.predict(source=frame, conf=0.3, show=True)
        
        # Optionally, process results (e.g., extract bounding boxes or labels)
        for r in results:
            boxes = r.boxes  # Get bounding boxes
            print(f"Detected objects: {boxes.xyxy}, {boxes.conf}, {boxes.cls}")
        
        # Display the frame with predictions (already handled by `show=True`)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    infer_from_webcam("model.pt")