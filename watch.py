import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

folder_to_watch = r"D:\n8n_data\images"#Change this to your folder
webhook_url = "https://n8nlocal.abhimanyusinghchouhan.tech/webhook/classify"#use your webhook

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"New file detected: {file_path}")
            
            # Wait until the file is fully written (your logic is fine)
            while True:
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read(1)
                    break 
                except PermissionError:
                    print(f"Waiting for file {file_path} to be available...")
                    time.sleep(0.5)

            # --- THIS IS THE MAIN CHANGE ---
            # 1. Create a JSON payload (dictionary)
            payload = {'image_path': file_path} 
            
            try:
                # 2. Send the payload as JSON, not as files
                response = requests.post(webhook_url, json=payload) 
                print("Webhook response:", response.status_code)
            except Exception as e:
                print("Error sending file path:", e)
            # --- End of change ---

observer = Observer()
observer.schedule(Watcher(), folder_to_watch, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

