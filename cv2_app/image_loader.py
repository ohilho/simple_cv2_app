#! /usr/bin/python3

import cv2
from pathlib import Path


class ImageLoader:
    def __init__(self) -> None:
        pass

    def __next__(self):
        raise StopIteration

    def __iter__(self):
        return self

    def title(self):
        return "Abstract Image Loader"


class ImageLoaderException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class VideoFrameLoader(ImageLoader):
    def __init__(self, file: str) -> None:
        super().__init__()
        # check file existance
        if not Path(file).exists():
            raise ImageLoaderException(f"File does not exists: {file}")

        # open video capturer
        self.cap = cv2.VideoCapture(file)

        if not self.cap.isOpened():
            raise ImageLoaderException("VideoCapturer not opened properly")
        self.file = file
        self.seq = -1

    def __next__(self):
        # while file is opened
        if not self.cap.isOpened():
            raise StopIteration
        # read frame and return
        ret, frame = self.cap.read()
        self.seq += 1
        if ret:
            return frame
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def title(self):
        return f"video file: {self.file}"


class DirectoryLoader(ImageLoader):
    def __init__(self, path: str) -> None:
        super().__init__()
        # check file existance
        img_dir = Path(path)
        if not img_dir.exists():
            raise ImageLoaderException(f"Path does not exists: {path}")

        self.img_paths = [
            str(child)
            for child in sorted(img_dir.iterdir())
            if child.is_file() and not child.is_symlink()
        ]
        self.img_path_iter = iter(self.img_paths)
        self.file = "No file"
        self.dir = str(img_dir)
        self.seq = -1

    def __next__(self):
        path = next(self.img_path_iter)
        self.file = path
        return cv2.imread(path, cv2.IMREAD_UNCHANGED)

    def __iter__(self):
        return self

    def title(self):
        return f"path: {self.file}"
