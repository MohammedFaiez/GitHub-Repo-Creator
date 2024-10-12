import os
import requests
import json
import subprocess

# Replace these with your own details
GITHUB_TOKEN = 'your_personal_access_token'
GITHUB_USERNAME = 'your_github_username'
REPO_NAME = 'new_repository_name'
REPO_DESCRIPTION = 'Description of your new repository'
PRIVATE = False  # Change to True for a private repo

# Function to create a new GitHub repository
def create_github_repo():
    url = f'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    data = {
        'name': REPO_NAME,
        'description': REPO_DESCRIPTION,
        'private': PRIVATE,
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print(f'Repository {REPO_NAME} created successfully!')
    else:
        print(f'Failed to create repository: {response.json()}')

# Function to initialize a local repository
def initialize_local_repo():
    subprocess.run(['git', 'init'])
    with open('README.md', 'w') as f:
        f.write(f'# {REPO_NAME}\n\n{REPO_DESCRIPTION}\n')
    subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', 'Initial commit'])

# Function to push local repo to GitHub
def push_to_github():
    subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git'])
    subprocess.run(['git', 'branch', '-M', 'main'])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])

if __name__ == '__main__':
    create_github_repo()
    initialize_local_repo()
    push_to_github()
