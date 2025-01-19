import cv2
import os
import google.generativeai as genai
import httpx
import os
import base64
import time
import pyttsx3
# from playsound import playsound

def capture_images(output_folder, num_images=10, fps=1):
    """
    Capture a specified number of images from the webcam at a specified frame rate.
    Helper function that stores images for gemini to use later.

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
    Helper function to deletee all files in the specified folder.

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


def gemini_narrate():
    """
    Function that makes API request to gemini.
    Inputs:
    - 10 images in local storage
    Outputs:
    - String: geminis narration
    Precondition: assumes local storage is not empty
    """
    genai.configure(api_key=os.environ['API_KEY'])
    model = genai.GenerativeModel(model_name = "gemini-1.5-pro")

    # image_path_1 = "./local_storage/image_1.jpg"
    # image_path_2 = "./local_storage/image_2.jpg"
    # image_path_3 = "./local_storage/image_3.jpg"
    # image_path_4 = "./local_storage/image_4.jpg"
    # image_path_5 = "./local_storage/image_5.jpg"
    # image_path_6 = "./local_storage/image_6.jpg"
    # image_path_7 = "./local_storage/image_7.jpg"
    # image_path_8 = "./local_storage/image_8.jpg"
    # image_path_9 = "./local_storage/image_9.jpg"
    # image_path_10 = "./local_storage/image_10.jpg"

    # image_1 = httpx.get(image_path_1)
    # image_2 = httpx.get(image_path_2)
    # image_3 = httpx.get(image_path_3)
    # image_4 = httpx.get(image_path_4)
    # image_5 = httpx.get(image_path_5)
    # image_6 = httpx.get(image_path_6)
    # image_7 = httpx.get(image_path_7)
    # image_8 = httpx.get(image_path_8)
    # image_9 = httpx.get(image_path_9)
    # image_10 = httpx.get(image_path_10)
    image_paths = [
        "./local_storage/image_1.jpg",
        "./local_storage/image_2.jpg",
        "./local_storage/image_3.jpg",
        "./local_storage/image_4.jpg",
        "./local_storage/image_5.jpg",
        "./local_storage/image_6.jpg",
        "./local_storage/image_7.jpg",
        "./local_storage/image_8.jpg",
        "./local_storage/image_9.jpg",
        "./local_storage/image_10.jpg"
    ]

    images = [
        {'mime_type': 'image/jpeg', 'data': base64.b64encode(open(path, 'rb').read()).decode('utf-8')}
        for path in image_paths
    ]

    # TODO: change prompt based on the insects that vision model detects
    prompt ="You are an experienced narrator who gets 10 images in sequential order representing a 10 second video, give a documentary-like narration of whats happening in less than 4 sentences"

    images.append(prompt)

    # response = model.generate_content([
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_1.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_2.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_3.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_4.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_5.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_6.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_7.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_8.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_9.content).decode('utf-8')},
    # {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_10.content).decode('utf-8')},
    # prompt
    # ])
    response = model.generate_content(images)
    return response.text


if __name__ == "__main__":
  genai.configure(api_key=os.environ['API_KEY'])
  model = genai.GenerativeModel(model_name = "gemini-1.5-pro")
  folder = "local_storage"
  delete_all_files(folder)
  capture_images(output_folder="local_storage", num_images=10, fps=1)
#   print(gemini_narrate())
  text = gemini_narrate()
  engine = pyttsx3.init()

    # Set properties for the voice
  engine.setProperty('rate', 150)  # Speed (words per minute)
  engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

  voices = engine.getProperty('voices')
  for voice in voices:
    if 'english' in voice.name.lower():  # Filter for an English voice
        engine.setProperty('voice', voice.id)
        break

  engine.say(text)

  # Wait for the speech to complete
  engine.runAndWait()