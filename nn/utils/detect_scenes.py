import os
import shutil

from collections import defaultdict
from scenedetect import detect, ContentDetector, split_video_ffmpeg, AdaptiveDetector

import cv2


def l(start, end):
    def l1(x):
        return {'start': start + x[0].get_seconds(),
                'end': start + x[1].get_seconds()}
    return l1


def detect_scenes(clips_path, intervals, threshold):
    scene_intervals = defaultdict(dict)
    for clip in os.listdir(clips_path):
        if not '.' in clip:
            continue
        start, end = intervals[clip]['start'], intervals[clip]['end']
        
        clip_name, ext = os.path.splitext(clip)
        clip_path = os.path.join(clips_path, clip)
        scenes_folder = os.path.join(clips_path, clip_name)
        
        if not os.path.isdir(scenes_folder):
            os.mkdir(scenes_folder)
        
        # vidcap = cv2.VideoCapture(clip_path)
        # fps = vidcap.get(cv2.CAP_PROP_FPS)
        # vidcap.release()
        
        scene_list = detect(clip_path, ContentDetector(threshold=threshold))
        tmp = []
        for start1, end1 in scene_list:
            if start1.get_frames() != end1.get_frames() \
            and end1.get_seconds() - start1.get_seconds() > 1:
                tmp.append((start1, end1))
        scene_list = tmp
        if len(scene_list) != 0:
            split_video_ffmpeg(clip_path, scene_list, f'{scenes_folder}/scene_$SCENE_NUMBER.mp4')
            os.remove(clip_path)
            scene_intervals[clip] = dict(zip(os.listdir(scenes_folder), map(l(start, end), scene_list)))
        else:
            shutil.move(clip_path, os.path.join(scenes_folder, "scene_001.mp4"))
            scene_intervals[clip] = {'scene_001.mp4': {'start': start,
                                                       'end': end}}

    return scene_intervals