import os
import smtplib
from email.message import EmailMessage
from googleapiclient.discovery import build

API_KEY = os.getenv("YT_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def get_top_viewed_videos():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # mostPopular চার্ট ব্যবহার করে ভারতের ভিডিও আনা
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="IN",
        maxResults=10
    )
    response = request.execute()
    
    # ভিউ সংখ্যা অনুযায়ী সর্ট করা (নিশ্চিত হওয়ার জন্য)
    items = sorted(response['items'], key=lambda x: int(x['statistics'].get('viewCount', 0)), reverse=True)
    
    video_list = []
    for index, item in enumerate(items, start=1):
        title = item['snippet']['title']
        v_id = item['id']
        views = item['statistics'].get('viewCount', '0')
        url = f"https://www.youtube.com/watch?v={v_id}"
        video_list.append(f"{index}. [Top {index}] {title}\n📊 Views: {int(views):,}\n🔗 {url}\n")
    
    return "\n".join(video_list)

def send_mail(body):
    msg = EmailMessage()
    msg.set_content(f"ভারতের আজকের টপ ১০ ভিডিওর তালিকা (ভিউ অনুযায়ী):\n\n{body}")
    msg['Subject'] = "India Top 10 YouTube Videos Report"
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    try:
        content = get_top_viewed_videos()
        send_mail(content)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
        
