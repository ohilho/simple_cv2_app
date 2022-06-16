#! /usr/bin/python3

from cv2_app.cv2_app import CV2App, DirectoryLoader
from argparse import ArgumentParser
    
def main():
    # get arguemnts. 
    parser = ArgumentParser("frame_extractor")
    parser.add_argument("--path", type=str, required=True, help="path to the video file")
    args = parser.parse_args()
    print(f"iterating {args.path} ...")

    # create app
    view = CV2App()
    
    # create and set image loader. in this case, Directory loader
    view.set_image_loader(DirectoryLoader(args.path))
    
    # add key event. this video window will be destoryed when q is pressed.
    view.register_key_event("q",CV2App.quit)
    # do nothing but just activate key match for iterating frame. simply speaking, this is "next frame" button.
    view.register_key_event("n",lambda : None) 
    
    # play video with 33 ms interval between each frame. 
    view.start(1, frame_controled_by_key=False)
    
    # or you can control your image sequence by pressing 'n' key
    # To do so, change frame_controled_by_key from False to True.
    # view.start(33, frame_controled_by_key=True)
    


if __name__ == "__main__":
    main()
    