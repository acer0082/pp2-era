import os
import shutil

os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

with open("source/file.txt", "w") as f:
    f.write("test file")

shutil.move("source/file.txt", "destination/file.txt")