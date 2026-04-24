import os

os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Current dir:", os.getcwd())

print("Files:", os.listdir("."))