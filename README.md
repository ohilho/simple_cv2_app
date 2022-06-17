# simple cv2 app

simple cv2 app framework.

## supports

- image loaders
  - video source
  - directory
- single view, single pipeline
- key event callback
- image logger
- custom callbacks

## 2 image sequence control model

- waiting key event before next image
- key event timeout for each image

## Example

- video player example (only image, no sound)

```shell
video_player.py --file=sample/Big_Buck_Bunny_1080_10s_1MB.mp4
```

- video frame extractor

```shell
video_frame_extractor.py --file=sample/Big_Buck_Bunny_1080_10s_1MB.mp4 --out=out
```

- image iteration in some directory (this works after frame extractor example. this requires some images in out directory.)

```shell
directory_iteration.py  --path=out
```
