import librosa.display as lid
import torchaudio
import matplotlib.pyplot as plt


def viz_intervals(file_audio, file_intervals):
    '''Функция визуализации интервалов с отсуствием разговоров'''
    lines = []
    with open(file_intervals) as file:
        for line in file:
            values = line.split()
            val0 = float(values[0])
            val1 = float(values[1])
            line = [val0, val1]
            lines.append(line)
    signal, sr = torchaudio.load(file_audio)
    fig, ax = plt.subplots(1, 1, figsize=(15, 6), num='Визуализация временных интервалов')
    lid.waveshow(signal.numpy(), sr=sr, axis='time')
    start, end = 0, 0
    for speech in lines:
        plt.axvspan(end, speech[0], alpha=0.5, color="r")
        start, end = speech[0], speech[1]
        plt.axvspan(start, end, alpha=0.5, color="g")
    plt.title(f"Анализ {'audio.wav'}: интервалы без речи выделены зеленым", size=20)
    plt.xlabel("Время (с)", size=20)
    plt.ylabel("Амплитуда", size=20)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.show()