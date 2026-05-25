import urllib.request
import os

def download_yolo():
    print("Setting up YOLOv3-tiny for object detection simulation...")
    
    base_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/"
    weights_url = "https://pjreddie.com/media/files/yolov3-tiny.weights"
    names_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    if not os.path.exists("yolov3-tiny.cfg"):
        print("Downloading YOLO config (yolov3-tiny.cfg)...")
        urllib.request.urlretrieve(base_url + "yolov3-tiny.cfg", "yolov3-tiny.cfg")
    
    if not os.path.exists("yolov3-tiny.weights"):
        print("Downloading YOLO weights (yolov3-tiny.weights ~33MB)...")
        urllib.request.urlretrieve(weights_url, "yolov3-tiny.weights")
        
    if not os.path.exists("coco.names"):
        print("Downloading coco labels (coco.names)...")
        urllib.request.urlretrieve(names_url, "coco.names")
        
    print("YOLO setup complete!")

if __name__ == "__main__":
    download_yolo()
