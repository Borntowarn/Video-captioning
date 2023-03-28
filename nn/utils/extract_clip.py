import os

from moviepy.video.io.VideoFileClip import VideoFileClip


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
            with VideoFileClip(video_path) as video:
                new = video.subclip(start, end)
                new.write_videofile(os.path.join(clip_folder, f"clip_{k}.mp4"), audio_codec='aac')
            k += 1
    return clip_folder, output

