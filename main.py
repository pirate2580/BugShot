import cv2
from ultralytics import YOLO

# TODO: try wrapping function with modal
import modal

app = modal.App()
image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(  # install system libraries for graphics handling
        ["libgl1-mesa-glx", "libglib2.0-0"]
    )
    .pip_install(  # install python libraries for computer vision
        ["ultralytics~=8.2.68", "roboflow~=1.1.37", "opencv-python~=4.10.0"]
    )
    .pip_install(  # add an optional extra that renders images in the terminal
        "term-image==0.7.1"
    )
)

@app.function(gpu="A100", image=image)
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