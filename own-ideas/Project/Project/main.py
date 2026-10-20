import hashlib
import os
import json

def load_existing():
    with open("screen_shot.json", "r") as file:
        return json.load(file)

existing_files = load_existing()
loaded_files = {}

def hash_file(file_path):
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

def scan():
    for file in loaded_files:
        file_found = existing_files.get(file)
        if file_found:
            if not file_found["hash"] == loaded_files[file].get("hash"):
                print(f'{file} has been changed!')
        else:
            print(f'{file} is new!')
    for existing_file in existing_files:
        file_found = loaded_files.get(existing_file)
        if file_found is None:
            print(f"{existing_file} has been removed!")
def load_current():
    for file in os.listdir():
        if not file == "main.py" and not file == "screen_shot.json":
            new_hash = hash_file(file)
            save_file = {
                "hash": new_hash
            }
            loaded_files[file] = save_file

load_current()
# save()
scan()
