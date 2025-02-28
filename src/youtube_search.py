from googleapiclient.discovery import build

def youtube_search(query):
    """
    Search for videos on YouTube based on a query string.
    """
    # create a connection to the YouTube API
    youtube = build('youtube', 'v3', developerKey="AIzaSyA-LJ5wh7JlVriUUGHXDyJcofOLrf7gpZc")
    #send a search request to the API
    search_response = youtube.search().list(
        q=query,#search query
        part='snippet',#recieve metadata about the video
        maxResults=10
    ).execute()

    videos = []
    #extract the video id and title from the search response
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append((search_result['snippet']['title'], search_result['id']['videoId']))

    return videos
