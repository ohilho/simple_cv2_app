#! /usr/bin/python3
import cv2
import numpy as np
from .cv2_app import CV2App

class MouseEvent:
    def __init__(self, app:CV2App):
        self.app = app
        cv2.setMouseCallback(self.app.winname, self.callback, self.app)
    
    def callback(self, event, x, y, flags, param):
        pass

class BoxSelectEvent(MouseEvent):
    def __init__(self, app: CV2App):
        super().__init__(app)
        self.coordinates = None # x, y, x+w, y+h
        self.selected = False
        self.mouse_down = False
        self.source_image = None
        self.app = app
    
    def mask(self, param):
        h = self.source_image.shape[0]
        w = self.source_image.shape[1]
        mask = np.zeros((h,w), dtype=np.float)
        
        if self.selected:
            mask[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]]=1
        
        return mask
        
    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and not self.mouse_down:
            self.mouse_down = True
            self.selected = False
            
            self.source_image = param.processed_image.copy()
            self.h = self.source_image.shape[0]
            self.w = self.source_image.shape[1]
            self.coordinates = [x,y]
            self.guid_layer = None

        if event == cv2.EVENT_LBUTTONUP and self.mouse_down:
            self.coordinates.extend([x,y])
            self.mouse_down = False
            self.selected = True

        if event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_down:
                # make mask
                self.guid_layer = np.zeros_like(param.processed_image, float)
                self.guid_layer += 0.5
                self.guid_layer[
                    self.coordinates[1]:y,
                    self.coordinates[0]:x,
                ] = 1.0
                self.guid_layer = self.guid_layer * param.processed_image

            else:
                self.guid_layer = np.zeros_like(param.processed_image, float)
                self.guid_layer = param.processed_image * 0.5
                self.guid_layer[
                    :,
                    x,
                ] = 255
                self.guid_layer[
                    y,
                    :,
                ] = 255
            cv2.imshow(param.winname, self.guid_layer.astype("uint8"))
        