import shutil
import os

path = 'tasks'
if os.path.exists(path):
    shutil.rmtree(path)
    print(f"Deleted {path}")
else:
    print(f"{path} does not exist")
