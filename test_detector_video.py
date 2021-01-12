ANNOTATION_PATH = ""
CONFIG_PATH = ""
SAVEDMODEL_PATH = ""
IMAGE = ""
LOG = ""
from object_detection.utils import label_map_util, visualization_utils as viz_utils
import tensorflow as tf
import cv2
import numpy as np
import time

capture = False

detect_fn = tf.saved_model.load(SAVEDMODEL_PATH)
category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt', True)
# video = cv2.VideoCapture(0)  #to use webcam
video = cv2.VideoCapture("") 
timenow = 0
timebef = 0

def get_fps(timenow, timebef):
    timenow = time.time()
    fps = 1/(timenow-timebef)
    timebef = timenow
    return timenow, timebef, fps

def extract(img_np, detections):
    height, width, channel = np.shape(img_np)
    pl_height = int(height * 0.2)
    pl_width = int(width * 0.2)

    y1 = int(detections[0] * height)
    x1 = int(detections[1] * width)
    y2 = int(detections[2] * height)
    x2 = int(detections[3] * width)

    plate = img[y1:y2, x1:x2]
    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    _, plate = cv2.threshold(plate, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    plate = np.stack((plate,) * 3, axis=-1)
    plate = cv2.resize(plate, (pl_width, pl_height))
    img_np[int(height * 0.05):int(height * 0.05 + pl_height), int(height * 0.05):int(height * 0.05 + pl_width)] = plate

    cv2.rectangle(img_np, (int(height * 0.05), int(height * 0.05 + pl_height)),
                  (int(height * 0.05 + pl_width), int(height * 0.05 + pl_height*1.5)), (0,0,0), 2)
    cv2.putText(img_np, "Capture", (int(height * 0.05), int(height * 0.05 + pl_height*1.35)),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
    # print(int(height * 0.05), int(height * 0.05 + pl_height), int(height * 0.05 + pl_width), int(height * 0.05 + pl_height*1.5))

    return img_np, plate

def capture_plate(img):
    global row
    cv2.imwrite(""+str(time.strftime("%y/%m/%d %H:%M:%S"))+".jpg", img)

    with open(LOG, "a") as f:
        f.write(str(time.strftime("%y/%m/%d %H:%M:%S"))+"         "+str(time.time())+".jpg"+"\n")

    print("Image Captured")

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if x > 24 and x < 152 and y>120 and y < 160:
            global capture
            capture = True

while True:
    # timenow, timebef, fps = get_fps(timenow, timebef)
    # print(fps)
    ret, img = video.read()
    img_np = np.array(img)

    input_tensor = tf.convert_to_tensor(img_np)
    detections = detect_fn(np.expand_dims(img_np, 0))
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    if(detections['detection_scores'][0] < 0.4):
        viz_utils.visualize_boxes_and_labels_on_image_array(
            img_np,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.2,
            agnostic_mode=False)

    else:
        ##plate extraction
        img_np, plate = extract(img_np, detections['detection_boxes'][0])


        viz_utils.visualize_boxes_and_labels_on_image_array(
            img_np,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.4,
            agnostic_mode=False)

    cv2.imshow("detector", img_np)
    cv2.setMouseCallback("detector", click_event)
    if capture is True:
        capture_plate(plate)
        capture = False
    if cv2.waitKey(1) >= 0:
        break


