from object_detection.utils import label_map_util, visualization_utils as viz_utils
import tensorflow as tf
import cv2
import numpy as np
import tensorflow as tf

IMAGE = #PATH TO IMAGE

PBTXT = "models//label_map.pbtxt"
CONFIG ="models//pipeline.config"
MODEL = "models//exported-models-V2//my_model//saved_model"

detector = tf.saved_model.load(MODEL)
category_index = label_map_util.create_category_index_from_labelmap(PBTXT, True)

img = cv2.imread(IMAGE)
img_np = np.array(img)
detections = detector(np.expand_dims(img_np, 0))
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
detections['num_detections'] = num_detections
detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

height, width, channel = np.shape(img)
pl_height = int(height*0.1)
pl_width = int(width*0.1)

y1 = int(detections['detection_boxes'][0][0]*height)
x1 = int(detections['detection_boxes'][0][1]*width)
y2 = int(detections['detection_boxes'][0][2]*height)
x2 = int(detections['detection_boxes'][0][3]*width)


plate = img[y1:y2, x1:x2]
plate = cv2.resize(plate, (pl_width, pl_height))

image_np_with_detections = img_np.copy()
viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.1,
            agnostic_mode=False)

image_np_with_detections[int(height*0.05):int(height*0.05+pl_height), int(height*0.05):int(height*0.05+pl_width)] = plate

cv2.imshow("image", image_np_with_detections)
cv2.waitKey(0)

