import hashlib
import os
import json

def load_existing():
    if not os.path.exists("screen_shot.json"):
        return {}
    with open("screen_shot.json", "r") as file:
        return json.load(file)

existing_files = load_existing()
loaded_files = {}
restricted_files = ["main.py", "screen_shot.json", "settings.json"]
restricted_dirs = [".git", "node_modules", "__pycache__", ".venv", "venv"]

def hash_file(file_path):
    print("Hash called!")
    if os.path.exists(file_path):
        with open(file_path, "rb")as file:
            chunk = file.read(5)
            new_hash = hashlib.sha256()
            while len(chunk):
                new_hash.update(chunk)
                chunk = file.read(5)
            return new_hash.hexdigest()
    else:
        print(f'"{file_path}" is not found!')

def save():
    with open("screen_shot.json", "w") as file:
        json.dump(loaded_files, file, indent=4)
        print("Screen_shot saved!")

def scan():
    if not os.path.exists("screen_shot.json"):
        print("No screen-shot found!")
    elif existing_files == {}:
        print("Screen-shot is empty!")
    else:
        for file in loaded_files:
            file_found = existing_files.get(file)
            if file_found:
                if file_found.get("recorded_date") != loaded_files[file].get("recorded_date") or file_found.get("recorded_size") != loaded_files[file].get("recorded_size"):
                    if not file_found["hash"] == loaded_files[file].get("hash"):
                        print(f'{file} has been changed!')
            else:
                print(f'{file} is new!')
        for existing_file in existing_files:
            file_found = loaded_files.get(existing_file)
            if file_found is None:
                print(f"{existing_file} has been removed!")

def load_current():
        for dirpath, dirname, filename in os.walk("./"):
            dirname[:] = [d for d in dirname if d not in restricted_dirs]            
            if filename:
                for i in filename:
                    file = os.path.relpath(os.path.join(dirpath, i), ".")
                    file = file.replace("\\", '/')
                    print(file)
                    if not file in restricted_files:
                        info = os.stat(file)
                        existing_file = existing_files.get(file)
                        if existing_file:
                            if existing_file.get("recorded_date") == info.st_mtime_ns and existing_file.get("recorded_size") == info.st_size and existing_file.get("hash"):
                                new_hash = existing_file.get("hash")
                            else:
                                new_hash = hash_file(file)
                        else:
                            new_hash = hash_file(file)
                        save_file = {
                            "hash": new_hash,
                            "recorded_date": info.st_mtime_ns,
                            "recorded_size": info.st_size
                        }
                        loaded_files[file] = save_file

load_current()
# save()
scan()
 
