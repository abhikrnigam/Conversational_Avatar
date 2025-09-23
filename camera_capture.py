# camera_capture.py
import cv2

def capture_image(output_path="captured.jpg"):
    """Capture an image from the laptop camera and save it."""
    cap = cv2.VideoCapture(0)  # 0 = default camera
    if not cap.isOpened():
        raise RuntimeError("❌ Could not open camera.")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("❌ Failed to capture image from camera.")

    cv2.imwrite(output_path, frame)
    print(f"📸 Image captured and saved to {output_path}")
    return output_path
