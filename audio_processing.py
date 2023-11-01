# import os
# import subprocess
# import threading
# from pydub import AudioSegment

# input_dir = "./"
# output_dir = "voicecut"
# os.makedirs(output_dir, exist_ok=True)

# processed_files = set()  # 用于存储已经处理过的文件名

# def is_audio_file(filename):
#     return filename.endswith(".wav")

# def process_audio(input_file):
#     output_file = os.path.join(output_dir, os.path.basename(input_file))
#         # 处理音频文件的代码,这段代码定义了要执行的FFmpeg命令。它创建了一个command列表，其中包含了FFmpeg命令行的参数。-i指定输入文件，-af指定音频过滤器，
#     # 此处使用了silenceremove过滤器来去除音频中的静音部分。最后，output_file指定了输出文件的路径。然后使用subprocess.run()执行该命令，即运行FFmpeg进行音频处理
#     command = [
#         "ffmpeg",
#         "-i", input_file,
#         "-af", "silenceremove=stop_periods=-1:stop_duration=0.05:stop_threshold=-30dB",
#         "-ar","16000",
#         output_file]

#     subprocess.run(command, shell=False)

#     audio = AudioSegment.from_file(input_file, format="wav")
#     duration = len(audio) / 1000  # 音频时长（秒）

#     if duration <= 16:
#         audio.export(output_file, format="wav")
#     else:
#         segments_count = int(duration // 16)  # 切割次数
#         remaining_time = duration % 16  # 剩余时间（秒）
#         segment_length = 16 * 1000  # 每个小段的长度（毫秒）

#         for i in range(segments_count):
#             start_time = i * segment_length
#             end_time = (i + 1) * segment_length
#             segment = audio[start_time:end_time]
#             segment.export(f"{output_file}_{i+1}.wav", format="wav")

#         if remaining_time > 0:
#             start_time = segments_count * segment_length
#             end_time = start_time + remaining_time * 1000
#             segment = audio[start_time:end_time]
#             segment.export(f"{output_file}_last.wav", format="wav")

#     print(f"处理音频文件 {input_file} 完成")

# def process_new_audio_files():
#     input_files = []
#     for filename in os.listdir(input_dir):
#         if is_audio_file(filename) and filename not in processed_files:
#             input_files.append(os.path.join(input_dir, filename))

#     # 创建线程列表
#     threads = []

#     # 遍历输入文件列表，为每个文件创建一个线程并启动
#     for input_file in input_files:
#         thread = threading.Thread(target=process_audio, args=(input_file,))
#         thread.start()
#         threads.append(thread)
#         processed_files.add(os.path.basename(input_file))

#     # 等待所有线程执行完毕
#     for thread in threads:
#         thread.join()

#     print("所有音频文件处理完成")

# process_new_audio_files()






import os
import subprocess
import threading

input_dir = "./"
output_dir = "voicecut"
os.makedirs(output_dir, exist_ok=True)

processed_files = set()  # 用于存储已经处理过的文件名

def is_audio_file(filename):
    return filename.endswith(".wav")

def process_audio(input_file):
    output_file = os.path.join(output_dir, os.path.basename(input_file))

    # 处理音频文件的代码,这段代码定义了要执行的FFmpeg命令。它创建了一个command列表，其中包含了FFmpeg命令行的参数。-i指定输入文件，-af指定音频过滤器，
    # 此处使用了silenceremove过滤器来去除音频中的静音部分。最后，output_file指定了输出文件的路径。然后使用subprocess.run()执行该命令，即运行FFmpeg进行音频处理
    command = [
        "ffmpeg",
        "-i", input_file,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.05:stop_threshold=-30dB",
        "-ar","16000",
        output_file]

    subprocess.run(command, shell=False)

    print(f"处理音频文件 {input_file} 完成")

def process_new_audio_files():
    input_files = []
    for filename in os.listdir(input_dir):
        if is_audio_file(filename) and filename not in processed_files:
            input_files.append(os.path.join(input_dir, filename))

    # 创建线程列表
    threads = []

    # 遍历输入文件列表，为每个文件创建一个线程并启动
    for input_file in input_files:
        thread = threading.Thread(target=process_audio, args=(input_file,))
        thread.start()
        threads.append(thread)
        processed_files.add(os.path.basename(input_file))

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

    print("所有音频文件处理完成")

process_new_audio_files()

