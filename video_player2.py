#! /usr/bin/python3

from pickle import TRUE
from cv2_app.cv2_app import CV2App
from cv2_app.image_loader import VideoFrameLoader
from cv2_app.mouse import BoxSelectEvent
from argparse import ArgumentParser
import cv2

def image_resizer(app:CV2App):
    app.processed_image = cv2.resize(app.current_image,dsize=None, fx=0.5,fy=0.5)
    
def main():
    # get arguemnts. 
    parser = ArgumentParser("frame_extractor")
    parser.add_argument("--file", type=str, required=True, help="path to the video file")
    args = parser.parse_args()
    print(f"playing {args.file} ...")

    # create app
    view = CV2App()
    
    # create and set image loader. in this case, video frame loader
    view.set_image_loader(VideoFrameLoader(args.file))
    
    # add key event. this video window will be destoryed when q is pressed.
    view.register_key_event("q",CV2App.quit)
    view.register_key_event("n",lambda : None)
    # image will be modified with this callback. 
    # here I made an resizer. 
    view.register_render_callback(image_resizer,[view]) 
    bs = BoxSelectEvent(view)
    
    # play video with 33 ms interval between each frame. 
    view.start(33,True)
    


if __name__ == "__main__":
    main()
    