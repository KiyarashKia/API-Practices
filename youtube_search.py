import webbrowser
import logging
from googleapiclient.discovery import build
from time import sleep
from datetime import datetime

#with open("myLog.log", "w") as log_file:
    #log_file.write("")

# Set up logging configuration
logging.basicConfig(filename="myLog.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

logging.info(f"\n\n--------- New Session Started on {current_date} ---------\n\n")

def search_youtube(query, api_key):
    logging.info(f"Searching YouTube for query: {query}")
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # Call the search.list method to retrieve search results
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=10
    ).execute()

    # Extract video URLs from the search response
    video_links = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in search_response.get("items", [])]
    
    return video_links

def get_video_link(query, api_key):
    video_links = search_youtube(query, api_key)
    
    if not video_links:
        logging.warning(f"No videos found for query: {query}")
        return "No videos found for this query."

    # Return the first video link
    return video_links[0]

def log_to_file(query, link):
    with open("log.txt", "a") as file:  # "a" mode appends to the file
        file.write(f"Query: {query}, Link: {link}\n\n")
    logging.info(f"Logged to file - Query: {query}, Link: {link}")

def open_in_chrome(url):
    # Try to open the URL using the system's default method
    try:
        webbrowser.get('chrome').open(url)
        logging.info(f"Opened URL in Chrome: {url}")
    except webbrowser.Error:
        # If Chrome is not found, use the default browser
        webbrowser.open(url)
        logging.warning(f"Chrome not found. Opened URL in default browser: {url}")

if __name__ == "__main__":
  
    api_key = "{TO BE REPLACED}"
    user_query = input("Enter your YouTube search query: ")
    video_link = get_video_link(user_query, api_key)
    print("Here's the link to the video:", video_link)

    # Prompt user to open the link in Chrome
    choice = input("Do you want to open the link in Chrome? Y/N: ").strip().lower()
    if choice == 'y':
        open_in_chrome(video_link)
    elif choice == 'n':
        print("Okay, Log is saved anyway!\n Goodbye..")
        logging.info("User chose not to open the link in Chrome.")
    sleep(3)
    log_to_file(user_query, video_link)
