import cv2
import numpy as np

from ultralytics import YOLO

model = YOLO("../../models/fingers-51s.pt")


def check_overlap(l1,r1,l2,r2):
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False

    if l1[1] > r2[1] or l2[1] > r1[1]:
        return False

    return True

def get_overlap_cords(l1,r1,l2,r2):
    new_x1 = max(l1[0],l2[0])
    new_y1 = max(l1[1],l2[1])
    new_x2 = min(r2[0],r1[0])
    new_y2 = min(r1[1],r2[1])

    return [new_x1,new_y1,new_x2,new_y2]

def get_middle(x1,y1,x2,y2):
    middle_x = (x1+x2)/2
    middle_y = (y1+y2)/2
    return [middle_x,middle_y]


cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    results = model.predict(frame,conf=0.5,verbose=False)
    thumb_pose = None
    index_pose = None

    for result in results:
        for i in range(len(result)):
            if int(result.boxes.cls[i]) == 0:
                thumb_pose = result.boxes.xyxy[i].cpu().numpy()
            if int(result.boxes.cls[i]) == 1:
                index_pose = result.boxes.xyxy[i].cpu().numpy()


    if thumb_pose is not None and index_pose is not None:
        overlap = check_overlap(thumb_pose[:2], thumb_pose[2:], index_pose[:2], index_pose[2:])

        print(overlap)

        if overlap:
            overlap_pose = get_overlap_cords(thumb_pose[:2], thumb_pose[2:], index_pose[:2], index_pose[2:])
            print(overlap_pose)
            overlap_center = get_middle(*overlap_pose)
            overlap_center = [float(i) for i in overlap_center]
            print(overlap_center)










