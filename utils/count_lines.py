import os
from glob import glob

all_python_files = glob("../**/*.py", recursive=True)
line_count = 0
for python_file_path in all_python_files:
    print(python_file_path)
    with open(python_file_path) as f:
        line_count += len(f.readlines())
print(f"Project has {line_count} lines of code")
