#! /usr/bin/python3

import cv2
from pathlib import Path
from .cv2_app import CV2App
from typing import Union

class ImageLogger:
    def __init__(self, out_dir, app:Union[CV2App,None] = None) -> None:
        self.path = Path(out_dir)
        self.app = app
        if app:
            app.register_render_callback(self.log_image_with_app,[self.app]) 

    def log_image_with_name(self, filename, image) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(self.path.joinpath(filename)), image)

    def log_image_with_sequence(self, seq, image) -> None:
        self.log_image_with_name(f"{seq:06d}.png", image)

    def log_image_with_time(self, time, image) -> None:
        self.log_image_with_name(f"{time:.6f}.png", image)

    def log_image_with_app(self,app:CV2App) -> None:
        self.log_image_with_name(f"{app.current_seq:06d}.png", app.processed_image)