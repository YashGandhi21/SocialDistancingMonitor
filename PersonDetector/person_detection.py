import cv2
import os
import numpy as np

initialize = True
net = None

# directory having yolo files
dest_dir = os.path.dirname(os.path.abspath(__file__))
COLORS = np.random.uniform(0, 255, size=(80, 3))


def populate_class_labels():
    class_file_name = 'yolov3_classes.txt'
    class_file_abs_path = dest_dir + os.path.sep + class_file_name
    if not os.path.exists(class_file_abs_path):
        print("Yolo classes file doesn't exist")
        exit(0)
    f = open(class_file_abs_path, 'r')
    classes = [line.strip() for line in f.readlines()]

    return classes


def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_bbox(img, bbox, labels, confidence, colors=None, write_conf=False):
    global COLORS
    global classes

    if classes is None:
        classes = populate_class_labels()

    for i, label in enumerate(labels):

        if colors is None:
            color = COLORS[classes.index(label)]
        else:
            color = colors

        if write_conf:
            label += ' ' + str(format(confidence[i] * 100, '.2f')) + '%'

        cv2.rectangle(img, (bbox[i][0], bbox[i][1]), (bbox[i][2], bbox[i][3]), color, 2)

        cv2.putText(img, label, (bbox[i][0], bbox[i][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return img


def detect_common_objects(image, confidence=0.5, nms_thresh=0.3, model='yolov3', enable_gpu=False):
    Height, Width = image.shape[:2]
    scale = 0.00392

    global classes
    global dest_dir

    if model == 'yolov3-tiny':
        config_file_name = 'yolov3-tiny.cfg'
        cfg_url = "https://github.com/pjreddie/darknet/raw/master/cfg/yolov3-tiny.cfg"
        weights_file_name = 'yolov3-tiny.weights'
        weights_url = 'https://pjreddie.com/media/files/yolov3-tiny.weights'
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)


    else:
        config_file_name = 'yolov3.cfg'
        cfg_url = 'https://github.com/arunponnusamy/object-detection-opencv/raw/master/yolov3.cfg'
        weights_file_name = 'yolov3.weights'
        weights_url = 'https://pjreddie.com/media/files/yolov3.weights'
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    config_file_abs_path = dest_dir + os.path.sep + config_file_name
    weights_file_abs_path = dest_dir + os.path.sep + weights_file_name

    if not os.path.exists(config_file_abs_path):
        print("yolo config file doesn't exist")
        exit(0)

    if not os.path.exists(weights_file_abs_path):
        print("yolo weights file doesn't exist")
        exit(0)

    global initialize
    global net

    if initialize:
        classes = populate_class_labels()
        net = cv2.dnn.readNet(weights_file_abs_path, config_file_abs_path)
        initialize = False

    # enables opencv dnn module to use CUDA on Nvidia card instead of cpu
    if enable_gpu:
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            max_conf = scores[class_id]
            if max_conf > confidence:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - (w / 2)
                y = center_y - (h / 2)
                class_ids.append(class_id)
                confidences.append(float(max_conf))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence, nms_thresh)

    bbox = []
    label = []
    conf = []

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        # make the code work for only person class
        if str(classes[class_ids[i]]) == 'person':
            bbox.append([int(x), int(y), int(x + w), int(y + h)])
            label.append(str(classes[class_ids[i]]))
            conf.append(confidences[i])

    return bbox, label, conf


class YOLO:

    def __init__(self, weights, config, labels, version='yolov3'):

        print('[INFO] Initializing YOLO ..')

        self.config = config
        self.weights = weights
        self.version = version

        with open(labels, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        self.colors = np.random.uniform(0, 255, size=(len(self.labels), 3))

        self.net = cv2.dnn.readNet(self.weights, self.config)

        layer_names = self.net.getLayerNames()

        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_objects(self, image, confidence=0.5, nms_thresh=0.3,
                       enable_gpu=False):

        if enable_gpu:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        Height, Width = image.shape[:2]
        scale = 0.00392

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True,
                                     crop=False)

        self.net.setInput(blob)

        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                max_conf = scores[class_id]
                if max_conf > confidence:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - (w / 2)
                    y = center_y - (h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(max_conf))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence, nms_thresh)

        bbox = []
        label = []
        conf = []

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            bbox.append([int(x), int(y), int(x + w), int(y + h)])
            label.append(str(self.labels[class_ids[i]]))
            conf.append(confidences[i])

        return bbox, label, conf

    def draw_bbox(self, img, bbox, labels, confidence, colors=None, write_conf=False):

        if colors is None:
            colors = self.colors

        for i, label in enumerate(labels):

            color = colors[self.labels.index(label)]

            if write_conf:
                label += ' ' + str(format(confidence[i] * 100, '.2f')) + '%'

            cv2.rectangle(img, (bbox[i][0], bbox[i][1]), (bbox[i][2], bbox[i][3]), color, 2)

            cv2.putText(img, label, (bbox[i][0], bbox[i][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

