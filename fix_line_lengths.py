import os
import subprocess

def fix_line_lengths(root_directory):
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(subdir, file)
                subprocess.run(["black", "-l", "79", filepath], check=True)

if __name__ == "__main__":
    root_directory = '.'  # Root of the repository

    try:
        fix_line_lengths(root_directory)
        print("Line lengths fixed successfully.")
    except Exception as e:
        print(f"Error occurred while fixing line lengths: {e}")
