'''
@author: Gurpreet Singh
'''

from collections import deque

import cv2
import time
import numpy as np
from device_controller import startDevice
from device_controller import stopDevice
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--confidence", type=float, default=0.3, help="Confidence threshold for person detection")
parser.add_argument("-s", "--stream", help="Video stream source")
parser.add_argument("-rt", "--startthreshold", type=int, default=5, help="Time to wait before starting device (seconds)")
parser.add_argument("-st", "--stopthreshold", type=int, default=20, help="Time to wait before stopping device (seconds)")
args = vars(parser.parse_args())



def init_model():
    # Load model
    model_path = 'models/frozen_inference_graph.pb'
    model_config = 'models/graph.pbtxt'
    global net
    net = cv2.dnn.readNetFromTensorflow(model_path, model_config)   
    global class_names
    labels_file = open("models/class_labels.txt", "r")   
    class_names = list(labels_file.read().split("\n"))
    labels_file.close()



def performDetection(image):
    
    # Read image
    input_image = image
    clone = input_image.copy()  
    h, w = input_image.shape[:2]
    blob = cv2.dnn.blobFromImage(input_image, size=(200,200), swapRB=True, crop=False)
    
    # Pass processed image to network
    net.setInput(blob)
    preds = net.forward()    
    
    detectionQueue = deque(maxlen=20)
    
    # Read results
    for result in preds[0,0]:
        conf = result[2]
        if conf>float(args["confidence"]):
            index = int(result[1])
            detected_class = class_names[index]
            if detected_class != "person":
                detectionQueue.append(0)
                continue
            
            detectionQueue.append(1)     
        
            left = int(result[3] * w)
            top = int(result[4] * h)
            right = int(result[5] * w)
            bottom = int(result[6] * h)
            #cv2.putText(clone, class_names[index] + '( {}% )'.format(round(conf*100,2)), (left, top-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 2)  
            cv2.rectangle(clone, (left, top), (right,bottom), (0,255,0), 2)
    
    overlay = clone.copy()
    cv2.rectangle(overlay, (5,5), (int(0.5 * w), int(0.25 * h)), (0,0,0), -1)
    cv2.addWeighted(overlay, 0.6, clone, 0.4, 0, clone)
    cv2.putText(clone, "Human Activity: ", (int(0.03 * w), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)
    cv2.putText(clone, "Device Status: ", (int(0.03 * w), 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)
    cv2.putText(clone, "Frames per second: ", (int(0.03 * w), 55), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)
    cv2.putText(clone, "Press 'Q' to exit", (int(0.03 * w), 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)
    
    if (len(detectionQueue)>0 and np.array(detectionQueue).mean() >= 0.5):
        activityDetected = True
        cv2.putText(clone, "Detected", (int(0.03 * w)+120, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (0, 255, 0), 1)
        
    else:
        activityDetected = False
        cv2.putText(clone, "Not Detected", (int(0.03 * w)+120, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (0, 0, 255), 1)

    return clone, activityDetected

    
if args["stream"] in ['0','1','2','3','4','5']:
    stream = cv2.VideoCapture(int(args["stream"]))
else:
    stream = cv2.VideoCapture(args["stream"])
init_model()
    
startWaitTimer = None
startTimeLeft = None
stopWaitTimer = 0
stopTimeLeft = None
startThreshold = args["startthreshold"]
stopThreshold = args["stopthreshold"]

while True:
    isRead, frame = stream.read()

    if isRead:
        fps_start = time.time()
        
        processed_frame, activityDetected = performDetection(frame)
        h, w = processed_frame.shape[:2]
        
        if (activityDetected and (startWaitTimer is None) and (startTimeLeft is None)):
            startWaitTimer = time.time()
            startTimeLeft = startThreshold
            cv2.putText(processed_frame, "Device will start in {} seconds".format(startTimeLeft), (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,200,0), 1)
        elif (activityDetected and startTimeLeft is not None and startTimeLeft>0):
            startTimeLeft = startThreshold - int(time.time() - startWaitTimer)
            cv2.putText(processed_frame, "Device will start in {} seconds".format(startTimeLeft), (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,200,255), 1)
        elif (activityDetected):
            # Call to start devices
            if startTimeLeft is not None:
                startDevice()
            startTimeLeft = None
            stopWaitTimer = None
            stopTimeLeft = None
            cv2.putText(processed_frame, "Device working", (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 1)
        elif (not activityDetected and stopWaitTimer is None and stopTimeLeft is None):
            stopWaitTimer = time.time()
            stopTimeLeft = stopThreshold
            cv2.putText(processed_frame, "Device will stop in {} seconds".format(stopTimeLeft), (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,200,0), 1)            
        elif (not activityDetected and stopTimeLeft is not None and stopTimeLeft>0):
            stopTimeLeft = stopThreshold - int(time.time() - stopWaitTimer)
            cv2.putText(processed_frame, "Device will stop in {} seconds".format(stopTimeLeft), (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,200,255), 1)
        else:    
            #Call to stop device
            if stopTimeLeft is not None:
                stopDevice()
            stopTimeLeft = None
            startWaitTimer = None
            startTimeLeft = None
            cv2.putText(processed_frame, "Device stopped", (int(0.03 * w)+120,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)


        fps_end = time.time()
        #print("FPS: {}".format(round(1/(fps_end-fps_start))))
        cv2.putText(processed_frame, "{}".format(round(1/(fps_end-fps_start))), (int(0.03 * w)+140, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        cv2.imshow("Detections", processed_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


