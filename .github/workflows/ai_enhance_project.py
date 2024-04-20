import os
import requests
import subprocess
import json

# Function to read and filter changed files
def fetch_changed_files():
    output = subprocess.run(['git', 'diff', '--name-only', 'HEAD', 'HEAD~1'], capture_output=True, text=True)
    return [f for f in output.stdout.split('\n') if f.endswith('.py')]

# Function to get OpenAI Codex suggestions
def get_codex_suggestions(file_content):
    response = requests.post(
        "https://api.openai.com/v1/engines/codex-cushman-002/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "prompt": f"# Explain and suggest improvements for the following Python code\n{file_content}\n###",
            "temperature": 0.3,
            "max_tokens": 150,
        }
    )
    response_json = response.json()
    suggestions = response_json['choices'][0]['text'].strip() if response_json['choices'] else ''
    return suggestions

# Function to apply suggestions
def apply_suggestions(filename, suggestions):
    # Dummy function for applying Suggestions
    if "improve" in suggestions.lower():
        new_content = suggestions + '\n' + open(filename, 'r').read()
        with open(filename, 'w') as f:
            f.write(new_content)
        subprocess.run(['git', 'add', filename])
        commit_message = f"Automated enhancement: {suggestions.split('\n')[0][:50]}"
        subprocess.run(['git', 'commit', '-m', commit_message])

def main():
    changed_files = fetch_changed_files()
    for file in changed_files:
        file_path = os.path.join(os.getenv('GITHUB_WORKSPACE', '.'), file)
        content = open(file_path, 'r').read()
        suggestions = get_codex_suggestions(content)
        if suggestions:
            print(f"Suggestions for {file}:", suggestions)
            apply_suggestions(file_path, suggestions)

if __name__ == '__main__':
    main()
