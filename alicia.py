import argparse
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import cv2
import sys
import time
import numpy as np
from inference import Network

INPUT_STREAM = "test_video.mp4"
# MODEL = "models/2019.R3/semantic-segmentation-adas-0001.xml"
MODEL = "models/ssd_mobilnet_v2_coco_2018_03_09_ir7/ssd_mobilnet_v2_coco_2018_03_09_ir7.xml"
DEVICE = "MYRIAD"

COCO = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 
'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 
'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 
'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 
'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 
'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 
'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 
'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 
'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 
'hair brush']

def speak(text):
  os.popen( 'espeak -vf2 "'+text+'" 2>/dev/null' )

def get_class_names(class_nums):
    class_names= []
    for i in class_nums:
        if i > 0:
            class_names.append(COCO[int(i-1)])

    return class_names

def infer_on_video():
    speak('Hello! I am Alicia. Please wait while I boot up the system.')
    # Initialize the Inference Engine
    plugin = Network()
    class_names = []

    # Load the network model into the IE
    plugin.load_model(MODEL, DEVICE)
    net_input_shape = plugin.get_input_shape()

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    speak('System booted.')
    # allow the camera to warmup
    time.sleep(0.1)    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw image 
        image = frame.array

        key_pressed = cv2.waitKey(60)

        # Pre-process the frame
        p_frame = cv2.resize(image, (net_input_shape[3], net_input_shape[2]))
        p_frame = p_frame.transpose((2,0,1))
        p_frame = p_frame.reshape(1, *p_frame.shape)

        # Perform inference on the frame
        plugin.async_inference(p_frame)

        # Get the output of inference
        if plugin.wait() == 0:
            result = plugin.extract_output()
                        
            classes = np.transpose(result[0])[1]
            # classes = np.unique(np.transpose(result[0])[1])
            old_class_names = class_names
            class_names = get_class_names(classes)
            
            # publish the new environment only if something changes
            if class_names and class_names != old_class_names:
                speak_string = ''.join(class_names)                
                speak(speak_string)
                print(class_names)
                print("----------------------")                

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # Break if escape key pressed
        if key_pressed == 27:
            break
        
def main():    
    infer_on_video()


if __name__ == "__main__":
    main()
