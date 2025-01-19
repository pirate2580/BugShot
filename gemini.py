"AIzaSyDVZhuLIArx77Kif6dVuEg6nH0PYxUa8WQ"

import cv2
import os
import google.generativeai as genai
import httpx
import os
import base64
import time

def capture_images(output_folder, num_images=10, fps=1):
    """
    Capture a specified number of images from the webcam at a specified frame rate.

    Args:
        output_folder (str): Path to the folder where images will be saved.
        num_images (int): Number of images to capture.
        fps (int): Frames per second (time between frames will be 1/fps).
    """
    # Open the webcam
    cap = cv2.VideoCapture(0)
    
    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print(f"Starting to capture {num_images} images at {fps} FPS...")
    count = 0
    interval = 1 / fps  # Time between frames in seconds

    try:
        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                print("Error: Couldn't capture an image from the webcam.")
                break
            
            # Save the frame as an image
            image_path = f"{output_folder}/image_{count+1}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Captured {image_path}")
            
            count += 1
            time.sleep(interval)  # Wait before capturing the next image
    finally:
        # Release the webcam and close all OpenCV windows
        cap.release()
        print("Image capture completed.")

def delete_all_files(folder_path):
    """
    Deletes all files in the specified folder.

    Args:
        folder_path (str): Path to the folder whose files are to be deleted.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"Skipped non-file item: {file_path}")

    print(f"All files in '{folder_path}' have been deleted.")


if __name__ == "__main__":
  # genai.configure(api_key=os.environ['API_KEY'])
  # model = genai.GenerativeModel(model_name = "gemini-1.5-pro")
  folder = "local_storage"
  delete_all_files(folder)
  capture_images(output_folder="local_storage", num_images=10, fps=1)

