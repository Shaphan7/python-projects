import hashlib
import os
import json

def load():
    with open("screen_shot.json", "r") as file:
        return json.load(file)

existing_files = load()
loaded_files = {}

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

for file in os.listdir():
    if not file == "main.py" and not file == "screen_shot.json":
        with open(file, 'rb') as content:
            hash = hashlib.sha3_256(content.read())
            save_file = {
                "hash": hash.hexdigest()
            }
            loaded_files[file] = save_file

# save()
scan()

