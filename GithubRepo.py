import requests
import argparse
import logging
import json
from tabulate import tabulate
from datetime import datetime

# Set up basic logging format
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Function to fetch repository information from GitHub API
def fetch_repo_info(owner, repo, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    headers = {
        'Accept': 'application/vnd.github.mercy-preview+json',
        'Authorization': f'token {token}' if token else ''
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            logging.error("Rate limit exceeded or access forbidden. Try using a token.")
            return None
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error {response.status_code}: {err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error: {err}")
        return None

    repo_data = response.json()

    return {
        'name': repo_data.get('name'),
        'description': repo_data.get('description'),
        'stars': repo_data.get('stargazers_count'),
        'forks': repo_data.get('forks_count'),
        'language': repo_data.get('language'),
        'url': repo_data.get('html_url'),
        'created_at': format_date(repo_data.get('created_at')),
        'updated_at': format_date(repo_data.get('updated_at')),
        'open_issues': repo_data.get('open_issues_count'),
        'license': repo_data['license']['name'] if repo_data.get('license') else 'No license',
        'topics': ', '.join(repo_data.get('topics', [])) or 'No topics'
    }

def format_date(date_str):
    if not date_str:
        return "N/A"
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

# Function to display repository info
def display_repo_info(repo_info, output_format='table', save=False):
    if not repo_info:
        logging.warning("No information to display.")
        return

    if output_format == 'json':
        output = json.dumps(repo_info, indent=2)
        print(output)
    else:
        table = [[key, value] for key, value in repo_info.items()]
        output = tabulate(table, headers=["Field", "Value"], tablefmt="github")
        print(output)

    if save:
        filename = f"{repo_info['name']}_info.json"
        with open(filename, 'w') as f:
            json.dump(repo_info, f, indent=2)
        logging.info(f"\n✅ Repository info saved to {filename}")

# Main CLI entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch GitHub repository information.')
    parser.add_argument('owner', help='Repository owner username')
    parser.add_argument('repo', help='Repository name')
    parser.add_argument('--token', help='GitHub personal access token (optional)', default=None)
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    parser.add_argument('--save', action='store_true', help='Save output to JSON file')
    args = parser.parse_args()

    repo_info = fetch_repo_info(args.owner, args.repo, args.token)
    display_repo_info(repo_info, args.format, args.save)
