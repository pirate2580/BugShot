import cv2
from ultralytics import YOLO
import math
import struct
import serial


# @app.function(gpu="A100", image=image, mounts=[model_mount])
def infer_from_webcam(model_path):
    """
    Performs inference using a YOLOv8 model from a webcam feed.
    
    Args:y
        model_path (str): Path to the fine-tuned YOLOv8 model file.
    Outputs:
    -   (x, y, z coordinates)
    Output Assumption: Assume the x
    """
    ser = serial.Serial('COM6', 9600)  # Replace 'COM3' with your Arduino's port
    # Load the YOLOv8 model
    model = YOLO(model_path)
    
    # Initialize the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    
    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("width: " + str(width) + " height: " + str(height))
    print("Press 'q' to exit.")
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Couldn't read a frame from the webcam.")
            break
        
        # Run inference on the current frame
        results = model.predict(source=frame, conf=0.6, show=True)

        classes = results[0].boxes.cls.tolist()
        pos = results[0].boxes.xywh.tolist()
        # print(pos)
        ser.timeout = 2  # Optional: timeout for read/write operations
        bad_bugs = [0, 3, 4, 5, 7, 8] #ant, catterpillar, grasshopper, moth, cockroach, scorpion
        baddest_bug = []
        for i in range(len(pos)):
            if(classes[i] in bad_bugs):
                baddest_bug = pos[i]
                break
        if baddest_bug:
            x = baddest_bug[0]
            y = baddest_bug[1]
            print(baddest_bug, x, y)
            pitch_send = (x-120)/410*60+60
            yaw_send = 45-35*((y-90)/240)
            print(pitch_send, yaw_send)
        
            #data = struct.pack('BB', x, y)
            # ser.write(data)
            # ser.close()
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    infer_from_webcam("model.pt")

