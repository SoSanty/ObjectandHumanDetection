#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:55:46 2021

@author: esantisor23
"""
import numpy as np
import cv2
import pickle
from utils import receiving, encryption


class YoloFeat():

    def __init__(self, configPath, weightsPath, LABELS, COLORS):

        self.configPath = ''
        self.weightsPath = ''
        self.LABELS = ''
        self.COLORS = ''

    def loading(self):

        # load the COCO class labels our YOLO model was trained on
        labelsPath = '/Users/esantisor23/Desktop/THESIS/PYTHON/YOLO/coco.names'
        self.LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
                                        dtype="uint8")
        # derive the paths to the YOLO weights and model configuration
        self.weightsPath = '/Users/esantisor23/Desktop/THESIS/PYTHON/YOLO/yolov3.weights'
        self.configPath = '/Users/esantisor23/Desktop/THESIS/PYTHON/YOLO/yolov3.cfg'
        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")

    def layers(self, client_socket, data, payload_size, args):
        net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        while True:
            frame = receiving(data, payload_size, client_socket)
            message = self.reading(frame, net, ln, args,
                                   self.COLORS, self.LABELS)
            message = pickle.dumps(message)
            client_socket.send(message)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    def reading(self, frame, net, ln, args):

        (W, H) = (None, None)
        # loop over frames from the video file stream
        # read the next frame from the file
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > args["confidence"]:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                                args["threshold"])
        IDs = ''
        # ensure at least one detection exists
        l = 0
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],
                                           confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                if classIDs[i] == 0:
                    IDs = IDs + str(classIDs[i]) + ';' + '0' + ';'
                elif 0 < classIDs[i] < 10:
                    IDs = IDs + str(classIDs[i]) + ';' + '1' + ';'
                elif 9 < classIDs[i] < 15:
                    IDs = IDs + str(classIDs[i]) + ';' + '2' + ';'
                elif 14 < classIDs[i] < 25:
                    IDs = IDs + str(classIDs[i]) + ';' + '3' + ';'
                elif 24 < classIDs[i] < 30:
                    IDs = IDs + str(classIDs[i]) + ';' + '4' + ';'
                elif 29 < classIDs[i] < 40:
                    IDs = IDs + str(classIDs[i]) + ';' + '5' + ';'
                elif 39 < classIDs[i] < 47:
                    IDs = IDs + str(classIDs[i]) + ';' + '6' + ';'
                elif 46 < classIDs[i] < 57:
                    IDs = IDs + str(classIDs[i]) + ';' + '7' + ';'
                elif 56 < classIDs[i] < 64:
                    IDs = IDs + str(classIDs[i]) + ';' + '8' + ';'
                elif 64 < classIDs[i] < 69:
                    IDs = IDs + str(classIDs[i]) + ';' + '9' + ';'
                elif 68 < classIDs[i] < 81:
                    IDs = IDs + str(classIDs[i]) + ';' + '10' + ';'
                l = l+1

        # write the output frame to disk
        cv2.imshow("Video Live Stream", frame)
        message = encryption(IDs, l)
        return message
