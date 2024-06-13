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

def calculate_language_percentages(language_stats):
    total_bytes = sum(language_stats.values())
    language_percentages = {}
    for language, bytes_of_code in language_stats.items():
        language_percentages[language] = (bytes_of_code / total_bytes) * 100
    return language_percentages

def main(username):
    repos = get_repos(username)
    if not repos:
        print(f"No repositories found for user: {username}")
        return
    language_stats = aggregate_languages(repos)
    language_percentages = calculate_language_percentages(language_stats)
    for language, percentage in sorted(language_percentages.items(), key=lambda item: item[1], reverse=True):
        print(f"{language}: {percentage:.2f}%")

if __name__ == "__main__":
    while True:
        user = input("Enter GitHub username: ")
        main(user)
        print("\n**Percentages are the ratio of each language in the entire profile")
        choice = input("Press 1 to search for another username, or press Enter to exit: \n")
        if choice != '1':
            break
