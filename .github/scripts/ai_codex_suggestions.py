python
import os
import requests

def analyze_code(code_content):
    endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
    payload = {
        "prompt": code_content,
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 150
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    suggestion = response.json().get('choices')[0].get('text', '').strip()
    return suggestion

def main():
    for filename in os.listdir('.'):
        if filename.endswith('.py'):
            with open(filename, 'r') as file:
                content = file.read()
            suggestion = analyze_code(content)
            print(f'Review for {filename}: {suggestion}')
            # Consider auto-applying or storing suggestions for review.
            
if __name__ == "__main__":
    main()
