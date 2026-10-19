
import customtkinter

from Helpers.ButtonValue import ButtonValue
from Helpers.Frame import ButtonFrame
from UI.Whiteboard.Constants import *

import cv2
import numpy as np

import threading

from ultralytics import YOLO



class Whiteboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self._set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.model = YOLO("../../models/fingers-51s.pt")

        self.cam = cv2.VideoCapture(0)

        self.title("Whiteboard")

        self.Xpos = 0
        self.Ypos = 0

        self.has_reset = True

        self.camera_last_pose = []

        self.detection_thread = threading.Thread(target=self.handle_camera_detection,daemon=True)
        self.detection_thread.start()

        self.color = ""

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame._set_appearance_mode("dark")
        self.main_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        self.frame = None

        self.draw_button = customtkinter.CTkButton(self.main_frame, text="draw", command=self.build_color_frame, bg_color="#2B2B2B")
        self.draw_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.canvas_frame = customtkinter.CTkFrame(self)
        self.canvas_frame._set_appearance_mode("dark")
        self.canvas_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsw")

        self.canvas = customtkinter.CTkCanvas(self.canvas_frame, width=800, height=750, bg="white")
        self.canvas.grid(column=1, row=0, padx=200, pady=10)

        self.canvas.bind("<Button-1>", self.last_pos)

        self.canvas.bind("<B1-Motion>", self.handle_draw)

    def build_color_buttons(self):
        buttons = []
        for i,color in enumerate(COLOR_BUTTON_LIST):
            buttons.append(ButtonValue(COLOR_BUTTON_LIST[i],lambda color=color:self.change_color(color),HOVER_COLOR_LIST[i],COLOR_BUTTON_LIST[i]))
        return buttons

    def change_color(self, color):
        self.color = color

    def last_pos(self, event):
        self.Xpos = event.x
        self.Ypos = event.y

    def reset_poses(self):
        self.Xpos = 0
        self.Ypos = 0

    def detected_last_pose(self):
        self.Xpos = self.camera_last_pose[0]
        self.Ypos = self.camera_last_pose[1]

    def handle_detection_drw(self):
        if not self.frame.get_tag() == "colors":
            return
        self.canvas.create_line(self.Xpos, self.Ypos, self.camera_last_pose[0], self.camera_last_pose[1], width=2, fill=self.color)
        self.detected_last_pose()

    def handle_draw(self, event):
        if not self.frame.get_tag() == "colors":
            return
        self.canvas.create_line(self.Xpos, self.Ypos, event.x, event.y, width=2, fill=self.color)
        self.last_pos(event)

    def handle_rectangle(self, event):
        if not self.frame.get_tag() == "shapes":
            return

    def build_color_frame(self):
        self.frame = ButtonFrame(self,"colors",self.build_color_buttons(),end_command=self.kill_frame,tag="colors")

    def kill_frame(self):
        self.frame = None

    def check_overlap(self,l1, r1, l2, r2):
        if l1[0] > r2[0] or l2[0] > r1[0]:
            return False

        if l1[1] > r2[1] or l2[1] > r1[1]:
            return False

        return True

    def get_overlap_cords(self,l1, r1, l2, r2):
        new_x1 = max(l1[0], l2[0])
        new_y1 = max(l1[1], l2[1])
        new_x2 = min(r2[0], r1[0])
        new_y2 = min(r1[1], r2[1])

        return [new_x1, new_y1, new_x2, new_y2]

    def get_middle(self,x1, y1, x2, y2):
        middle_x = (x1 + x2) / 2
        middle_y = (y1 + y2) / 2
        return [middle_x, middle_y]

    def handle_camera_detection(self):
        while True:
            ret, frame = self.cam.read()
            frame = cv2.flip(frame, 1)
            results = self.model.predict(frame, conf=0.5, verbose=False)
            thumb_pose = None
            index_pose = None

            for result in results:
                for i in range(len(result)):
                    if int(result.boxes.cls[i]) == 0:
                        thumb_pose = result.boxes.xyxy[i].cpu().numpy()
                    if int(result.boxes.cls[i]) == 1:
                        index_pose = result.boxes.xyxy[i].cpu().numpy()

            if thumb_pose is not None and index_pose is not None:
                overlap = self.check_overlap(thumb_pose[:2], thumb_pose[2:], index_pose[:2], index_pose[2:])

                print(overlap)

                if overlap:
                    overlap_pose = self.get_overlap_cords(thumb_pose[:2], thumb_pose[2:], index_pose[:2],
                                                          index_pose[2:])
                    print(overlap_pose)
                    overlap_center = self.get_middle(*overlap_pose)
                    overlap_center = [int(i) for i in overlap_center]
                    print(overlap_center)

                    self.camera_last_pose = overlap_center
                    if self.has_reset:
                        self.after(0, self.detected_last_pose)
                        self.has_reset = False
                    self.after(0,self.handle_detection_drw)
                else:
                    self.reset_poses()
                    self.has_reset = True







