import requests
import argparse
import logging
import json
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format='%(message)s')

def fetch_repo_info(owner, repo, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    headers = {'Authorization': f'token {token}'} if token else {}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error: {err}")
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
        'created_at': repo_data.get('created_at'),
        'updated_at': repo_data.get('updated_at'),
        'open_issues': repo_data.get('open_issues_count'),
        'license': repo_data['license']['name'] if repo_data.get('license') else 'No license',
    }

def display_repo_info(repo_info, output_format='table'):
    if not repo_info:
        logging.warning("No information to display.")
        return

    if output_format == 'json':
        print(json.dumps(repo_info, indent=2))
    else:
        table = [[key, value] for key, value in repo_info.items()]
        print(tabulate(table, headers=["Field", "Value"], tablefmt="github"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch GitHub repository information.')
    parser.add_argument('owner', help='Repository owner username')
    parser.add_argument('repo', help='Repository name')
    parser.add_argument('--token', help='GitHub personal access token (optional)', default=None)
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    args = parser.parse_args()

    repo_info = fetch_repo_info(args.owner, args.repo, args.token)
    display_repo_info(repo_info, args.format)
