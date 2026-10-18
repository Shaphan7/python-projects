import os
files = {
}

def check_duplicate(given_file):
    for file in files.values():
        if file.get("content") == given_file.get("content"):
            given_file["duplicate"] = True
            print(f"'{given_file.get("name")}' is a duplicate of '{file.get("name")}'")

for i, og_file in enumerate(os.listdir()):
    if not og_file == "main.py" and os.path.isfile(og_file):
        with open(og_file, "rb") as  x:
            file = {
                "name": og_file,
                "content": x.read(),
                "duplicate": False
            }
            check_duplicate(file)
            files[i] = file
print(files)

