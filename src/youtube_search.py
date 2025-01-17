from googleapiclient.discovery import build

def youtube_search(query):
    youtube = build('youtube', 'v3', developerKey="AIzaSyA-LJ5wh7JlVriUUGHXDyJcofOLrf7gpZc")
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=10
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append((search_result['snippet']['title'], search_result['id']['videoId']))

    return videos
