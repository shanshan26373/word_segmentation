import librosa
import matplotlib.pyplot as plt
import numpy as np

# y是音频的时间序列，是一个float32的numpy数组。sr是采样率(sampling rate)
# mono 意为单声道，如果参数值为True，会将不是单声道的音频转换为单声道
# offset 和 duration 分别表示音频读取的起始时间点和持续时长，默认值分别是0.0和None，即默认读取整段音频文件。
if __name__ == '__main__':
    y1, sr1 = librosa.load('./1.wav',
                         sr=16000, mono=True, offset=0.0, duration=None, )
    y2, sr2 = librosa.load('./voicecut/1.wav',
                         sr=16000, mono=True, offset=0.0, duration=None,)

    # 绘制波形图  max_points 指的是用于绘图的最大样本数，默认值是采样率的一半
    # librosa.display.waveshow(y, sr=16000, max_points=8000, x_axis='time',
    # offset=0.0, marker='', where='post', label=None, ax=None, **kwargs)



    fig = plt.figure(figsize=(12, 9))
    # ax = fig.add_subplot(221)
    # spce1 = librosa.display.waveplot(y1, sr=sr1, offset=0.0, color='blue')
    # ax.set_title('未处理音频波形图', fontproperties="SimSun")

    # ax = fig.add_subplot(222)
    # spec2 = librosa.display.waveplot(y2, sr=sr2, offset=0.0, color='orange')
    # ax.set_title('处理后音频波形图', fontproperties="SimSun")

    ax = fig.add_subplot(221)
    ax.plot(np.arange(len(y1)) / sr1, y1, color='blue')
    ax.set_title('未处理音频波形图', fontproperties="SimSun")

    ax = fig.add_subplot(222)
    ax.plot(np.arange(len(y2)) / sr2, y2, color='orange')
    ax.set_title('处理后音频波形图', fontproperties="SimSun")

    # 绘制线性语谱图
    # librosa.display.specshow(data, x_coords=None, y_coords=None, x_axis=None, y_axis=None,
    # sr=16000, hop_length=512, fmin=None, fmax=None, tuning=0.0,
    # bins_per_octave=12, key='C:maj', Sa=None, mela=None, thaat=None,
    # auto_aspect=True, htk=False, ax=None)
    # 将stft后的幅度值的绝对值转换成分贝值，将返回值传入specshow()方法中
    data1 = librosa.amplitude_to_db(np.abs(librosa.stft(y1)), ref=np.max)
    data2 = librosa.amplitude_to_db(np.abs(librosa.stft(y2)), ref=np.max)

    ax = fig.add_subplot(223)
    # x轴是时间/s，y轴是由fft窗口和采样率决定的频率值/Hz
    spec3 = ax.imshow(data1, aspect='auto', origin='lower', cmap='magma',
                      extent=[0, len(y1) / sr1, 0, sr1 / 2])  # x_axis='time', y_axis='linear' replaced
    ax.set_ylim(0, 5000)     # 5000Hz以上没有能量显示，因此y轴上限设为5500
    ax.set_title('线性频率语谱图1', fontproperties='SimSun')
    fig.colorbar(spec3, ax=ax, format="%+2.fdB")

    ax = fig.add_subplot(224)
    spec4 = ax.imshow(data2, aspect='auto', origin='lower', cmap='magma',
                      extent=[0, len(y2) / sr2, 0, sr2 / 2])  # x_axis='time', y_axis='linear' replaced
    ax.set_ylim(0, 5000)
    ax.set_title('线性频率语谱图2', fontproperties='SimSun')
    fig.colorbar(spec4, ax=ax, format="%+2.fdB")

    plt.show()


    plt.show()