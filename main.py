import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_youtube_videos(api_key, query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=query,
        type='video',
        part='snippet',
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId']
        }
        videos.append(video)
    return videos

 ### Email function right here
def send_email(sender_email, receiver_email, subject, body, credentials_path):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/gmail.send']
    )

    gmail_service = build('gmail', 'v1', credentials=credentials)

 ### Main function
def main():
    youtube_api_key = 'ENTER YOUTUBE API KEY HERE'
    
    ### For your gmail credentials
    gmail_credentials_path = 'JSON FILE HERE' 

    search_query = input("What kind of videos would you like?: ")
    receiver_email = input("Enter your email address: ")

    videos = get_youtube_videos(youtube_api_key, search_query)

    email_subject = f"YouTube Recommendations for {search_query}"
    email_body = "\n".join([f"{video['title']}: https://www.youtube.com/watch?v={video['video_id']}" for video in videos])

    send_email('SERVICE ACCOUNT HERE', receiver_email, email_subject, email_body, gmail_credentials_path)
    print("Email sent successfully.")

if __name__ == "__main__":
    main()