import os
from moviepy.editor import VideoFileClip

def extract_audio_from_video(path, video_name, output_ext="wav"):
    '''Вырезание аудио дорожки из фильма'''
    
    filename, ext = os.path.splitext(video_name)
    video_path = os.path.join(path, 'videos', video_name)
    
    clip = VideoFileClip(video_path)
    
    audio_folder = os.path.join(path, 'audios')
    audio_name = f'{filename}.{output_ext}'
    
    clip.audio.write_audiofile(os.path.join(audio_folder, audio_name))
    return audio_name