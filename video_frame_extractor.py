#! /usr/bin/python3

from cv2_app.cv2_app import CV2App, VideoFrameLoader, ImageLogger
from argparse import ArgumentParser
import cv2

def image_resizer(app:CV2App):
    app.current_image = cv2.resize(app.current_image,dsize=None, fx=0.5,fy=0.5)
    
def main():
    # get arguemnts. 
    parser = ArgumentParser("frame_extractor")
    parser.add_argument("--file", type=str, required=True, help="path to the video file")
    parser.add_argument("--out", type=str, required=True, help="path to the output files")

    args = parser.parse_args()
    print(f"start capturing {args.file} ...")

    # create image logger
    lg = ImageLogger(args.out)
    
    # create app
    view = CV2App()
    
    # create and set image loader. in this case, video frame loader
    view.set_image_loader(VideoFrameLoader(args.file))
    
    # add key event. this video window will be destoryed when q is pressed.
    view.register_key_event("q",CV2App.quit)
    # do nothing but just activate key match for iterating frame. simply speaking, this is "next frame" button.
    view.register_key_event("n",lambda : None) 
    
    # image will be modified with this callback. 
    # Image resizer. 
    view.register_render_callback(image_resizer,[view]) 
    # Image logger
    view.register_render_callback(lambda x:lg.log_image_with_sequence(x.current_seq,x.current_image),[view]) 
    
    # play video with 1 ms interval between each frame. 
    view.start(1, frame_controled_by_key=False)
    
    # or you can control your image sequence by pressing 'n' key
    # To do so, change frame_controled_by_key from False to True.
    # view.start(33, frame_controled_by_key=True)
    


if __name__ == "__main__":
    main()
    