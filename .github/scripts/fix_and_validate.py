python
import os
from pathlib import Path

def validate_directories(base_path):
    # Checks if recommended files/directories exist. If not, raise flagged notices.
    synthesizer_path = Path(base_path, 'models/synthesizer/synthesizer.pt')
    vocoder_path = Path(base_path, 'models/vocoder/vocoder.pt')
    
    if not synthesizer_path.exists():
        raise FileNotFoundError("No synthesizer models found!")
    if not vocoder_path.exists():
        raise FileNotFoundError("No vocoder models found!")
        
    print("All necessary model files are present.")

def main():
    base_path = Path(os.getenv('GITHUB_WORKSPACE', '.'))
    try:
        validate_directories(base_path)
    except Exception as e:
        print(f"Validation error: {e}")
        exit(1)  # Fails the job step if there’s an error

if __name__ == '__main__':
    main()
