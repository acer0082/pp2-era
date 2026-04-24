import shutil
import os

# copy file
shutil.copy("sample.txt", "backup.txt")

# append
with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("\nNew line added")

# safe delete
if os.path.exists("backup.txt"):
    os.remove("backup.txt")