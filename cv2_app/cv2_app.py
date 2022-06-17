#! /usr/bin/python3

import cv2
from pathlib import Path
from .image_loader import ImageLoader
import numpy as np


class CV2AppException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CV2AppStopIteration(CV2AppException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CV2App:
    num_windows = 0

    def __init__(self) -> None:
        self.image_loader = None
        self.key_event_callbacks = []
        self.render_event_callbacks = []
        self.current_image = None
        self.processed_image = None
        self.current_seq = None
        # singleton name during the process.
        self.winname = str(CV2App.num_windows)
        cv2.imshow(self.winname, np.zeros((100, 100, 3), dtype=np.uint8))
        CV2App.num_windows += 1

    def set_image_loader(self, image_loader: ImageLoader) -> None:
        self.image_loader = iter(image_loader)

    def register_key_event(self, key: str, callback, params=[]):
        self.key_event_callbacks.append(
            {"key": key, "callback": callback, "params": params}
        )

    def register_render_callback(self, callback, params=[]):
        self.render_event_callbacks.append({"callback": callback, "params": params})

    def check_key_event(self, period):
        wk_ret = cv2.waitKey(period)
        for event in self.key_event_callbacks:
            if wk_ret & 0xFF == ord(event["key"][0]):
                event["callback"](*event["params"])
                return True
        return False

    def start(self, period=0, frame_controled_by_key=True):
        try:
            for seq, image in enumerate(self.image_loader):
                self.current_image = image
                self.processed_image = image
                self.current_seq = seq

                # render event callbacks excution befor rendering
                for event in self.render_event_callbacks:
                    event["callback"](*event["params"])

                # show image
                cv2.imshow(self.winname, self.processed_image)
                title = self.image_loader.title() + f" seq: {seq}"
                cv2.setWindowTitle(self.winname, title)

                # key event
                if frame_controled_by_key:
                    key_match = False
                    while not key_match:
                        key_match = self.check_key_event(period)
                else:
                    self.check_key_event(period)

        except CV2AppStopIteration:
            cv2.destroyAllWindows()
            return

    @staticmethod
    def quit():
        raise CV2AppStopIteration
