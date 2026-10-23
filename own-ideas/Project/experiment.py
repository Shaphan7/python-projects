import os

for dirpath, dirnames, filenames in os.walk("test_folder"):
    if filenames:
        for i in filenames:
            print(os.path.join(dirpath, i).replace("\\", '/'))