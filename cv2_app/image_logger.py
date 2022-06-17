#! /usr/bin/python3

import cv2
from pathlib import Path


class ImageLogger:
    def __init__(self, out_dir) -> None:
        self.path = Path(out_dir)

    def log_image_with_name(self, filename, image) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(self.path.joinpath(filename)), image)

    def log_image_with_sequence(self, seq, image) -> None:
        self.log_image_with_name(f"{seq:06d}.png", image)
