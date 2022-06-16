import cv2
from pathlib import Path


#####################################################################
#                           Image Loader
#####################################################################

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
        self.seq +=1
        if ret:
            return frame
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def title(self):
        return f'video file: {self.file}'


class DirectoryLoader(ImageLoader):
    def __init__(self, path: str) -> None:
        super().__init__()
        # check file existance
        img_dir = Path(path)
        if not img_dir.exists():
            raise ImageLoaderException(f"Path does not exists: {path}")

        self.img_paths = [str(child) for child in sorted(img_dir.iterdir()) if child.is_file() and not child.is_symlink()]
        self.img_path_iter = iter(self.img_paths)
        self.file = "No file"
        self.dir = str(img_dir)
        self.seq = -1

    def __next__(self):
        path = next(self.img_path_iter)
        self.file = path
        return cv2.imread(path,cv2.IMREAD_UNCHANGED)

    def __iter__(self):
        return self

    def title(self):
        return f'path: {self.file}'


#####################################################################
#                           CV2 App
#####################################################################

# simple, sigle-view application 

class CV2AppException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CV2AppStopIteration(CV2AppException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class CV2App:
    num_windows=0
    def __init__(self) -> None:
        self.image_loader = None
        self.key_event_callbacks = []
        self.render_event_callbacks = []
        self.current_image = None
        self.current_seq= None
        # singleton name during the process.
        self.winname = str(CV2App.num_windows)
        CV2App.num_windows +=1
    
    def set_image_loader(self,image_loader:ImageLoader)->None:
        self.image_loader=iter(image_loader)

    def register_key_event(self,key:str, callback, params=[]):
        self.key_event_callbacks.append({"key": key, "callback":callback, "params":params})

    def register_render_callback(self,callback,params=[]):
        self.render_event_callbacks.append({"callback":callback,"params":params})

    def check_key_event(self,period):
        wk_ret = cv2.waitKey(period)
        for event in self.key_event_callbacks:
            if wk_ret & 0xFF == ord(event["key"][0]):
                event["callback"](*event["params"])
                return True
        return False

    def start(self,period=0,frame_controled_by_key = True):
        try:
            for seq,image in enumerate(self.image_loader):
                self.current_image = image
                self.current_seq = seq
                
                # render event callbacks excution befor rendering
                for event in self.render_event_callbacks:
                    event["callback"](*event["params"])
                
                # show image
                cv2.imshow(self.winname, self.current_image)
                title = self.image_loader.title() + f" seq: {seq}"
                cv2.setWindowTitle(self.winname, title)
                
                # key event
                if frame_controled_by_key:
                    key_match=False
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



class ImageLogger:
    def __init__(self,out_dir) -> None:
        self.path= Path(out_dir) 
    
    def log_image_with_name(self,filename, image)->None:
        self.path.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(self.path.joinpath(filename)),image)

    def log_image_with_sequence(self,seq,image)->None:
        self.log_image_with_name(f'{seq:06d}.png',image)