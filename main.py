import os
import smtplib
from email.message import EmailMessage
from googleapiclient.discovery import build

# পরিবেশ ভেরিয়েবল থেকে ডেটা নেওয়া (সুরক্ষার জন্য)
API_KEY = os.getenv("YT_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def get_trending_videos():
    # ইউটিউব এপিআই কানেক্ট করা
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # ইন্ডিয়ার ট্রেন্ডিং ভিডিওর লিস্ট চাওয়া
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="IN",
        maxResults=10
    )
    response = request.execute()
    
    video_list = []
    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        video_list.append(f"🎥 {title}\nLink: {url}\n")
    
    return "\n".join(video_list)

def send_mail(body):
    msg = EmailMessage()
    msg.set_content(f"আজকের সেরা ইউটিউব ভিডিওগুলোর তালিকা:\n\n{body}")
    msg['Subject'] = "Daily YouTube Trending Update"
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER # নিজের মেইলেই মেইল যাবে

    # জিমেইল সার্ভারের মাধ্যমে মেইল পাঠানো
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    try:
        content = get_trending_videos()
        send_mail(content)
        print("Mail sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
      
