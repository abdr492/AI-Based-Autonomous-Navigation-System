import cv2
import numpy as np
import os

def object_detection():
    # Load pre-trained YOLO model
    if not (os.path.exists("yolov3-tiny.weights") and os.path.exists("yolov3-tiny.cfg")):
        print("YOLO weights not found. Please run 'python setup_yolo.py' first.")
        return

    print("Loading YOLOv3-tiny model...")
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
        
    layer_names = net.getLayerNames()
    try:
        # For newer OpenCV versions
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except Exception:
        # Fallback for older formats
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Open camera
    cap = cv2.VideoCapture(0)
    
    frame_count = 0
    print("Starting Object Detection Feed...")
    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
        else:
            # Simulated video feed if no real camera
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "No Camera: Simulated YOLO Feed", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Simulate a moving object to "detect"
            x_pos = (frame_count * 8) % 640
            cv2.rectangle(frame, (x_pos, 200), (x_pos + 60, 260), (0, 0, 255), -1)
            cv2.putText(frame, "Obstacle (Simulated)", (x_pos, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(frame, (x_pos, 200), (x_pos + 60, 260), (0, 255, 0), 2) # Bounding box
            
            frame_count += 1
            cv2.waitKey(30)
            
            # Still process through YOLO to simulate the workload (though it won't detect the drawn rectangle as COCO objects)
            
        height, width, channels = frame.shape
        
        # Prepare frame for YOLO
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    
        # Apply Non-Max Suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                conf = confidences[i]
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    object_detection()
