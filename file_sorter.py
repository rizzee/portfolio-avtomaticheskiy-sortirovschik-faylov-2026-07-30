import os
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileSorterHandler(FileSystemEventHandler):
    def __init__(self, downloads_path):
        self.downloads_path = downloads_path

    def on_modified(self, event):
        for file in os.listdir(self.downloads_path):
            file_path = Path(self.downloads_path) / file
            if file_path.is_file():
                ext = file_path.suffix.lower()[1:]  # Remove dot
                dest_folder = Path(self.downloads_path) / ext
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest_folder / file))


def main():
    downloads_path = str(Path.home() / 'Downloads')
    event_handler = FileSorterHandler(downloads_path)
    observer = Observer()
    observer.schedule(event_handler, downloads_path, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
