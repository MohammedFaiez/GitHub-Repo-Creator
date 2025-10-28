# GitHub Repo Info Fetcher

A simple command-line tool to fetch and display information about GitHub repositories using the GitHub API.

## Features

- Fetch repository information by name
- Display details like:
  - Repository name
  - Description
  - Stars ⭐
  - Forks 🍴
  - Open issues
  - Primary language
  - License
  - Last updated timestamp

## Prerequisites

- Python 3.6 or higher
- `requests` library (install using `pip install requests`)

## Usage

1. Clone the repository or download the script:

   ```bash
   git clone https://github.com/your-username/github-repo-info-fetcher.git
   cd github-repo-info-fetcher


2. Run the script with the repository name in owner/repo format:
    ```bash
    python fetch_repo_info.py octocat/Hello-World

 3. Example output:
    Repository: Hello-World
    Description: My first repository on GitHub!
    Stars: 1500
    Forks: 300
    Open Issues: 42
    Language: Python
    License: MIT
    Last Updated: 2025-10-28T12:34:56Z
