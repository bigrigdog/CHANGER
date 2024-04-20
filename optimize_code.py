import openai
import os


def optimize_python_code(file_path, api_key):
    """Uses OpenAI's Codex to refactor and optimize Python code dynamically."""
    with open(file_path, "r", encoding="utf-8") as file:
        original_code = file.read()

    prompt = f"### Refactor and optimize this Python code with explanations\n{original_code}\n###"
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=0.1,
        max_tokens=len(prompt.split()) * 2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        api_key=api_key,
    )
    improved_code = response.choices[0].text.strip()

    if improved_code and improved_code != original_code:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(improved_code)
        return True
    return False


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    root_directory = "."  # Root of the repository
    files_updated = 0

    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(subdir, file)
                if optimize_python_code(filepath, api_key):
                    files_updated += 1

    if files_updated > 0:
        print(f"{files_updated} files optimized.")
    else:
        print("No files were optimized.")
