import fileinput
import re
import os

def fix_resample_usage(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            if filepath.endswith(".py"):  # Target only Python files
                with fileinput.FileInput(filepath, inplace=True, backup='.bak') as file:
                    for line in file:
                        # Regex to find the incorrect resample usage which assumes three arguments wrongly placed
                        line = re.sub(r'librosa\.resample\((.*?), (.*?), (.*?)\)', r'librosa.resample(\1, orig_sr=\2, target_sr=\3)
', line)
                        print(line, end='')  # This redirection to `print` is necessary with `fileinput` to write changes

fix_resample_usage('C:/Users/wyatt/CLONE/Real-Time-Voice-Cloning-GUI')  # Update to your project path
