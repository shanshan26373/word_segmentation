# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# class WavFileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         self.process_file(event.src_path)

#     def on_modified(self, event):
#         self.process_file(event.src_path)

#     def process_file(self, file_path):
#         if file_path.endswith(".wav"):
#             # 执行deal.py处理程序
#             os.system("python audio_processing.py")

#             # 执行cut.py处理程序
#             os.system("python audio_segmentation.py")

# if __name__ == "__main__":
#     # 监视的目录路径
#     directory_to_watch = "./"

#     event_handler = WavFileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, directory_to_watch, recursive=False)
#     observer.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()


# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# class WavFileHandler(FileSystemEventHandler):
#     def __init__(self):
#         self.processed_files = set()  # 保存已处理的文件名的集合
#         self.load_processed_files()  # 从文件中加载已处理的文件名

#     def load_processed_files(self):
#         try:
#             with open("processed_files.txt", "r") as file:
#                 for line in file:
#                     self.processed_files.add(line.strip())
#         except FileNotFoundError:
#             pass

#     def save_processed_files(self):
#         with open("processed_files.txt", "w") as file:
#             for file_name in self.processed_files:
#                 file.write(file_name + "\n")

#     def on_created(self, event):
#         if not event.is_directory and event.src_path.endswith(".wav"):
#             file_name = os.path.basename(event.src_path)
#             if file_name not in self.processed_files:
#                 self.processed_files.add(file_name)
#                 self.process_file(event.src_path)

#     def process_file(self, file_path):
#         if file_path.endswith(".wav"):
#             # 执行deal.py处理程序
#             os.system("python audio_processing.py")

#             # 执行cut.py处理程序
#             os.system("python audio_segmentation.py")

# if __name__ == "__main__":
#     directory_to_watch = "./"
#     event_handler = WavFileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, directory_to_watch, recursive=False)
#     observer.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()

#     event_handler.save_processed_files()  # 保存已处理的文件名到文件中



import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WavFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.process_file(event.src_path)

    def on_modified(self, event):
        file_path = event.src_path
        created_time = os.path.getctime(file_path)
        modified_time = os.path.getmtime(file_path)
        if modified_time > created_time:
            self.process_file(file_path)

    def process_file(self, file_path):
        if file_path.endswith(".wav"):
            # 执行audio_processing.py处理程序（非阻塞方式）
            subprocess.Popen(["python", "audio_processing.py"])

            # 执行cut.py处理程序（非阻塞方式）
            subprocess.Popen(["python", "audio_segmentation.py"])

if __name__ == "__main__":
    directory_to_watch = "./"

    event_handler = WavFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
