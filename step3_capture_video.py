import cv2
import numpy as np

def simulate_video_feed():
    print("Initializing Capture...")
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Warning: Real hardware camera not found. Falling back to simulated video feed.")
    
    frame_count = 0
    # Simulate a window
    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
        else:
            # Generate simulated frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add some moving visual elements
            x_pos = (frame_count * 5) % 640
            cv2.rectangle(frame, (x_pos, 220), (x_pos + 40, 260), (0, 255, 0), -1)
            cv2.putText(frame, "Simulated Camera Feed", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to exit", (220, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            frame_count += 1
            cv2.waitKey(30) # Delay to simulate frame rate

        cv2.imshow("Live Camera Feed (Step 3)", frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    simulate_video_feed()
