import os
import json

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from .convert_intervals import convert_intervals

def extract_clip(path, video, intervals):
    video_path = os.path.join(path, 'videos', video)
    video_name, ext = os.path.splitext(video)
    clip_folder = os.path.join(path, 'clips', video_name)
    
    if not os.path.isdir(clip_folder):
        os.mkdir(clip_folder)
    
    output = {}
    k = 0
    for start, end in intervals:
        if end - start > 2:
            output[f"clip_{k}.mp4"] = {'end': end, 'start': start}
            ffmpeg_extract_subclip(
                video_path, 
                start, 
                end, 
                targetname=os.path.join(clip_folder, f"clip_{k}.mp4")
            )
            k += 1
    
    return clip_folder, output

