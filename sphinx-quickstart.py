import os
import subprocess

def create_sphinx_docs(project_name, author_name, project_release):
    # Step 1: Initialize Sphinx
    subprocess.run(["sphinx-quickstart", "-q", "-p", project_name, "-a", author_name, "-r", project_release])

    # Step 2: Edit index.rst and create additional documentation files

    # Step 3: Build documentation
    os.chdir("source")  # Change directory to the source folder
    subprocess.run(["make", "html"])

    print("Documentation built successfully!")

if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    author_name = input("Enter the author name: ")
    project_release = input("Enter the project release: ")

    create_sphinx_docs(project_name, author_name, project_release)
