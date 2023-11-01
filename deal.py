#case 1
# import os
# import numpy as np
# import librosa

# def split_audio_by_silence(audio, sr, min_silence_duration=0.5, silence_threshold=-40):
#     # 将音频数据转换为单声道
#     if len(audio.shape) > 1:
#         audio = np.mean(audio, axis=1)

#     # 计算音频的短时能量
#     # energy = librosa.feature.rms(audio, frame_length=1024, hop_length=512)[0]
#     energy = librosa.feature.rms(y=audio, frame_length=1024, hop_length=512)[0]

#     # 根据能量阈值和最小静音时长切割音频
#     splits = []
#     start = 0
#     is_silence = False

#     for i in range(len(energy)):
#         if energy[i] < silence_threshold and not is_silence:
#             is_silence = True
#             start = i
#         elif energy[i] >= silence_threshold and is_silence:
#             is_silence = False
#             duration = (i - start) * 512 / sr
#             if duration >= min_silence_duration:
#                 splits.append((start * 512 / sr, i * 512 / sr))

#     # 返回切割后的音频段
#     segments = []
#     for split in splits:
#         start_frame = int(split[0] * sr / 512)
#         end_frame = int(split[1] * sr / 512)
#         segments.append(audio[start_frame:end_frame])

#     return segments

# # 获取当前目录下的所有WAV文件
# current_dir = os.getcwd()
# wav_files = [file for file in os.listdir(current_dir) if file.endswith(".wav")]

# # 创建voicecut文件夹（如果不存在）
# output_dir = os.path.join(current_dir, "voicecut")
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # 处理每个WAV文件
# for wav_file in wav_files:
#     # 读取音频文件
#     audio, sr = librosa.load(os.path.join(current_dir, wav_file), sr=None)

#     # 切割音频
#     segments = split_audio_by_silence(audio, sr)

#     # 保存切割后的音频段
#     for i, segment in enumerate(segments):
#         output_file = os.path.join(output_dir, f"{wav_file}_{i}.wav")
#         librosa.output.write_wav(output_file, segment, sr)



# #case 2
# import os
# import wave

# # 创建一个名为'voicecut'的子目录
# output_dir = 'voicecut'
# os.makedirs(output_dir, exist_ok=True)

# # 定义一个静音检测函数
# def is_silent(audio_data, threshold=100):
#     return max(audio_data) < threshold

# # 处理同一目录下的所有WAV文件
# input_dir = '.'  # 当前目录
# for filename in os.listdir(input_dir):
#     if filename.endswith(".wav"):
#         input_path = os.path.join(input_dir, filename)

#         # 打开WAV文件并读取音频数据
#         with wave.open(input_path, 'rb') as wav_file:
#             sample_width = wav_file.getsampwidth()
#             framerate = wav_file.getframerate()
#             n_channels = wav_file.getnchannels()
#             n_frames = wav_file.getnframes()
#             audio_data = wav_file.readframes(n_frames)

#         # 切割静音段
#         silent_segments = []
#         current_segment = []
#         for i in range(0, len(audio_data), sample_width):
#             sample = audio_data[i:i + sample_width]
#             if is_silent(sample):
#                 if current_segment:
#                     silent_segments.append(current_segment)
#                     current_segment = []
#             else:
#                 current_segment.append(sample)

#         # 将非静音段保存到'voicecut'子目录中
#         for i, segment in enumerate(silent_segments):
#             output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_{i}.wav")
#             with wave.open(output_path, 'wb') as output_file:
#                 output_file.setnchannels(n_channels)
#                 output_file.setsampwidth(sample_width)
#                 output_file.setframerate(framerate)
#                 output_file.writeframes(b''.join(segment))
#             print(f"Saved {output_path}")


import os
from pydub import AudioSegment, silence

# 创建一个名为'voicecut'的子目录
output_dir = 'voicecut'
os.makedirs(output_dir, exist_ok=True)

# 处理同一目录下的所有WAV文件
input_dir = '.'  # 当前目录
for filename in os.listdir(input_dir):
    if filename.endswith(".wav"):
        input_path = os.path.join(input_dir, filename)

        # 使用pydub加载音频文件

        audio = AudioSegment.from_file(input_path, format="wav")

        # 切割静音段
        silent_ranges = silence.detect_silence(audio, min_silence_len=100, silence_thresh=-30)

        # 创建一个新的音频对象，用于存储非静音段
        non_silent_audio = AudioSegment.empty()

        # 将非静音段添加到新的音频对象中
        for start, end in silent_ranges:
            non_silent_audio += audio[start:end]

        # 保存非静音段到'voicecut'子目录中
        output_path = os.path.join(output_dir, filename)
        non_silent_audio.export(output_path, format="wav")
        print(f"Saved {output_path}")


# import os
# from pydub import AudioSegment, silence

# # 创建一个名为'voicecut'的子目录
# output_dir = 'voicecut'
# os.makedirs(output_dir, exist_ok=True)

# # 处理同一目录下的所有WAV文件
# input_dir = '.'  # 当前目录
# for filename in os.listdir(input_dir):
#     if filename.endswith(".wav"):
#         input_path = os.path.join(input_dir, filename)

#         # 使用pydub加载音频文件
#         audio = AudioSegment.from_file(input_path, format="wav")

#         # 切割静音段
#         silent_ranges = silence.detect_silence(audio, min_silence_len=100, silence_thresh=-30)

#         # 创建一个新的音频对象，用于存储非静音段
#         non_silent_audio = AudioSegment.empty()

#         # 将非静音段添加到新的音频对象中
#         for i, (start, end) in enumerate(silent_ranges):
#             if i < len(silent_ranges) - 1:
#                 next_start = silent_ranges[i + 1][0]
#                 non_silent_audio += audio[start:next_start]  # 非静音段为[start, next_start)
#             else:
#                 non_silent_audio += audio[start:end]  # 最后一个静音段后的部分也添加到非静音段中

#         # 保存非静音段到'voicecut'子目录中
#         output_path = os.path.join(output_dir, filename)
#         non_silent_audio.export(output_path, format="wav")
#         print(f"Saved {output_path}")