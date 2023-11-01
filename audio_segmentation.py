# import os
# import subprocess
# import shutil

# input_dir = "./voicecut"
# output_dir = "./output"

# # 创建输出文件夹
# os.makedirs(output_dir, exist_ok=True)

# input_files = []
# for filename in os.listdir(input_dir):
#     if filename.endswith(".wav"):
#         input_files.append(os.path.join(input_dir, filename))

# def process_audio(input_file):
#     filename = os.path.basename(input_file)
#     output_file = os.path.join(output_dir, filename)

#     duration_command = [
#         "ffprobe",
#         "-v", "error",
#         "-show_entries", "format=duration",
#         "-of", "default=noprint_wrappers=1:nokey=1",
#         input_file
#     ]
#     duration_output = subprocess.check_output(duration_command, shell=False)
#     duration = float(duration_output)

#     if duration <= 16:
#         # 小于等于16秒，直接复制原文件到输出文件夹
#         shutil.copy(input_file, output_file)
#     else:
#         # 大于16秒，切割为小于等于16秒的片段
#         num_segments = int(duration / 16) + 1
#         for i in range(num_segments):
#             segment_output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_segment{i+1}.wav")
#             start_time = i * 16
#             end_time = min(start_time + 16, duration)
#             command = [
#                 "ffmpeg",
#                 "-ss", str(start_time),
#                 "-i", input_file,
#                 "-t", str(end_time - start_time),
#                 "-acodec", "copy",
#                 "-ar","16000",
#                 segment_output_file
#             ]
#             subprocess.run(command, shell=False)

#     print(f"处理音频文件 {filename} 完成")

# # 处理所有音频文件
# for input_file in input_files:
#     process_audio(input_file)

# print("所有音频文件处理完成，并保存在output文件夹中")


import os
import subprocess
import shutil

input_dir = "./voicecut"
output_dir = "./output"

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

processed_files = set()  # 用于存储已经处理过的文件名

def is_audio_file(filename):
    return filename.endswith(".wav")

def process_audio(input_file):
    filename = os.path.basename(input_file)
    output_file = os.path.join(output_dir, filename)

    duration_command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ]
    duration_output = subprocess.check_output(duration_command, shell=False)
    duration = float(duration_output)

    if duration <= 16:
        # 小于等于16秒，直接复制原文件到输出文件夹
        shutil.copy(input_file, output_file)
    else:
        # 大于16秒，切割为小于等于16秒的片段
        num_segments = int(duration / 16) + 1
        for i in range(num_segments):
            segment_output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_segment{i+1}.wav")
            start_time = i * 16
            end_time = min(start_time + 16, duration)
            command = [
                "ffmpeg",
                "-ss", str(start_time),
                "-i", input_file,
                "-t", str(end_time - start_time),
                "-acodec", "copy",
                "-ar","16000",
                segment_output_file
            ]
            subprocess.run(command, shell=False)

    print(f"处理音频文件 {filename} 完成")

def process_new_audio_files():
    input_files = []
    for filename in os.listdir(input_dir):
        if is_audio_file(filename) and filename not in processed_files:
            input_files.append(os.path.join(input_dir, filename))

    # 处理所有音频文件
    for input_file in input_files:
        process_audio(input_file)
        processed_files.add(os.path.basename(input_file))

    print("所有音频文件处理完成，并保存在output文件夹中")

process_new_audio_files()


