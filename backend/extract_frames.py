import cv2
import os

video_path = "sample.mp4"
output_folder = "frames"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)

interval = 5  
frame_number = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    timestamp = frame_number / fps

    if timestamp % interval < 1 / fps:
        filename = f"{output_folder}/frame_{int(timestamp)}s.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")

    frame_number += 1

cap.release()