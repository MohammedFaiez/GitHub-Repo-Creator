import requests
import argparse

def fetch_repo_info(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url)
    
    if response.status_code == 200:
        repo_data = response.json()
        return {
            'name': repo_data['name'],
            'description': repo_data['description'],
            'stars': repo_data['stargazers_count'],
            'forks': repo_data['forks_count'],
            'language': repo_data['language'],
            'url': repo_data['html_url'],
            'created_at': repo_data['created_at'],
            'updated_at': repo_data['updated_at'],
            'open_issues': repo_data['open_issues_count'],
            'license': repo_data.get('license', {}).get('name', 'No license'),
        }
    else:
        print(f"Error fetching repo: {response.json().get('message', 'Unknown error')}")
        return None

def display_repo_info(repo_info):
    if repo_info:
        print(f"Repository Name: {repo_info['name']}")
        print(f"Description: {repo_info['description']}")
        print(f"Stars: {repo_info['stars']}")
        print(f"Forks: {repo_info['forks']}")
        print(f"Language: {repo_info['language']}")
        print(f"URL: {repo_info['url']}")
        print(f"Created At: {repo_info['created_at']}")
        print(f"Updated At: {repo_info['updated_at']}")
        print(f"Open Issues: {repo_info['open_issues']}")
        print(f"License: {repo_info['license']}")
    else:
        print("No information to display.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch GitHub repository information.')
    parser.add_argument('owner', help='Repository owner username')
    parser.add_argument('repo', help='Repository name')
    args = parser.parse_args()
    
    repo_info = fetch_repo_info(args.owner, args.repo)
    display_repo_info(repo_info)
