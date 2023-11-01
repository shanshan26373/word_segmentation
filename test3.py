import os
import subprocess
import threading
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


y, sr = librosa.load("D:/Desktop/data/黄千莹-naming-20230706144708-16.wav")
y_cut, sr_cut = librosa.load("D:/Desktop/data/output/黄千莹-naming-20230706144708-16.wav")
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
plt.figure(figsize=(10, 4))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Original Audio')
plt.tight_layout()

D_cut = librosa.amplitude_to_db(np.abs(librosa.stft(y_cut)), ref=np.max)
plt.figure(figsize=(10, 4))
librosa.display.specshow(D_cut, sr=sr_cut, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Cropped Audio')
plt.tight_layout()
plt.show()

'''
input_files = [
    r"D:\Desktop\data\蔡铎健-naming-20230708170259-36.wav",
    r"D:\Desktop\data\蔡铎健-naming-20230708170302-37.wav",
    r"D:\Desktop\data\蔡铎健-naming-20230708170304-38.wav",
    r"D:\Desktop\data\蔡雄航-naming-20230630183031-6.wav",
    r"D:\Desktop\data\洪晓玫-naming-20230703144250-32.wav",
    r"D:\Desktop\data\洪晓玫-naming-20230703144259-33.wav",
    r"D:\Desktop\data\黄祺惠-naming-20230707181403-21.wav",
    r"D:\Desktop\data\黄祺惠-naming-20230707181414-22.wav",
    r"D:\Desktop\data\黄千莹-naming-20230706144708-16.wav",
    r"D:\Desktop\data\黄千莹-naming-20230706144713-17.wav",
    r"D:\Desktop\data\黄彦彰-naming-20230708170634-41.wav",
    r"D:\Desktop\data\黄彦彰-naming-20230708170636-42.wav",
    r"D:\Desktop\data\李蔓莎-naming-20230705104506-11.wav",
    r"D:\Desktop\data\李蔓莎-naming-20230705104512-12.wav",
    r"D:\Desktop\data\林锦鹏-naming-20230705100655-6.wav",
    r"D:\Desktop\data\林锦鹏-naming-20230705100704-7.wav"
]

output_folder = r"D:\Desktop\data\output"


def process_audio(input_file):
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    # 处理音频文件的代码
    command = [
        r"E:\ffmpeg-6.0-essentials_build\bin\ffmpeg",
        "-i", input_file,
        "-ar", "16000",
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.01:stop_threshold=-30dB",
        output_file
    ]
    subprocess.run(command, shell=False)

    print(f"处理音频文件 {input_file} 完成")


# 创建线程列表

threads = []

# 遍历输入文件列表，为每个文件创建一个线程并启动

for input_file in input_files:
    thread = threading.Thread(target=process_audio, args=(input_file,))
    thread.start()
    threads.append(thread)

# 等待所有线程执行完毕

for thread in threads:
    thread.join()

print("所有音频文件处理完成")

'''
