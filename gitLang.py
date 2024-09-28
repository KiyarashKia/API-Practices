import requests
import matplotlib.pyplot as plt
import os

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

def generate_pie_chart(language_percentages, username):
    # Create the pie chart
    labels = list(language_percentages.keys())
    sizes = list(language_percentages.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

    # Create directory if it doesn't exist
    output_dir = 'gitLang'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the pie chart
    output_path = os.path.join(output_dir, f"{username}_language_pie_chart.png")
    plt.savefig(output_path)
    print(f"Pie chart saved to {output_path}")

def main(username):
    repos = get_repos(username)
    if not repos:
        print(f"No repositories found for user: {username}")
        return
    language_stats = aggregate_languages(repos)
    language_percentages = calculate_language_percentages(language_stats)

    # Display percentages
    for language, percentage in sorted(language_percentages.items(), key=lambda item: item[1], reverse=True):
        print(f"{language}: {percentage:.2f}%")

    # Ask user if they want to save the pie chart
    if language_percentages:
        choice = input("Press 'S' to save as image, 'N' for another username, or press Enter to exit: ").upper()
        if choice == 'S' or choice == 's':
            generate_pie_chart(language_percentages, username)
        elif choice == 'N' or choice == 'n':
            return 'N'
        else:
            return 'exit'

if __name__ == "__main__":
    while True:
        user = input("Enter GitHub username: ")
        action = main(user)
        if action == 'exit':
            break
        elif action != 'N':
            choice = input("Press 'N' for another username or press Enter to exit: ").upper()
            if choice != 'N':
                break
