import os
import librosa
from pyannote.audio import Pipeline


def find_intervals_to_describe(path, audio_name):
    '''Функция поиска интервалов аудио без голосов (для передачи в модель)'''
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                        use_auth_token='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')
    audio_path = os.path.join(path, 'audios', audio_name)
    output = pipeline(audio_path)
    
    start = 0.0
    end = librosa.get_duration(filename=audio_path)
    
    intervals = []
    for speech in output.get_timeline().support():
        intervals.append([start, speech.start])
        start = speech.end
    intervals.append([start, end])
    
    return intervals