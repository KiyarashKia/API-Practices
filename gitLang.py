import requests

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_languages(repo):
    url = repo['languages_url']
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def aggregate_languages(repos):
    language_stats = {}
    for repo in repos:
        languages = get_languages(repo)
        for language, bytes_of_code in languages.items():
            if language in language_stats:
                language_stats[language] += bytes_of_code
            else:
                language_stats[language] = bytes_of_code
    return language_stats

def main(username):
    repos = get_repos(username)
    if not repos:
        print(f"No repositories found for user: {username}")
        return
    language_stats = aggregate_languages(repos)
    for language, bytes_of_code in sorted(language_stats.items(), key=lambda item: item[1], reverse=True):
        print(f"{language}: Found!")

if __name__ == "__main__":
    while True:
        user = input("Enter GitHub username: ")
        main(user)
        choice = input("\nPress 1 to search for another username, or press Enter to exit: \n")
        if choice != '1':
            break
