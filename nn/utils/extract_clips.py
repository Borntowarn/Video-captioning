import os
import json

from collections import defaultdict
from .extract_audio import extract_audio_from_video
from .extract_clip import extract_clip
from .voice_activity_detection import find_intervals_to_describe
from .detect_scenes import detect_scenes

def extract_clips(path, threshold):
    
    videos_intervals = defaultdict(dict)
    for video in os.listdir(os.path.join(path, 'videos')):
        audio_name = extract_audio_from_video(path, video)
        intervals = find_intervals_to_describe(path, audio_name)
        clips_folder, intervals = extract_clip(path, video, intervals)
        
        video, ext = os.path.splitext(video)
        videos_intervals[video] = detect_scenes(clips_folder, intervals, threshold)
    
    print('Scenes fully extracted')
    return videos_intervals