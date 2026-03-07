import os
import smtplib
from email.message import EmailMessage
from googleapiclient.discovery import build
import isodate # ভিডিওর ডিউরেশন ফরম্যাট করার জন্য

def get_top_videos():
    api_key = os.getenv("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # ভিডিওর ডিউরেশন এবং অন্যান্য ডিটেইলস পাওয়ার জন্য রিকোয়েস্ট
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        chart="mostPopular",
        regionCode="IN",
        maxResults=10
    )
    response = request.execute()
    
    # ইমেইল বডি তৈরির জন্য HTML ফরম্যাট ব্যবহার করা হচ্ছে
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #FF0000;">Top 10 Trending Videos in India</h2>
        <hr>
    """
    
    for i, item in enumerate(response['items'], 1):
        title = item['snippet']['title']
        v_id = item['id']
        views = item['statistics'].get('viewCount', '0')
        thumbnail = item['snippet']['thumbnails']['high']['url']
        
        # ডিউরেশন ফরম্যাট করা (যেমন: PT5M20S থেকে 5:20)
        duration_raw = item['contentDetails']['duration']
        duration = str(isodate.parse_duration(duration_raw))
        
        html_content += f"""
        <div style="margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
            <h3>#{i} {title}</h3>
            <img src="{thumbnail}" alt="Thumbnail" style="width: 320px; border-radius: 10px;">
            <p><b>⏱ Duration:</b> {duration}</p>
            <p><b>👁 Views:</b> {int(views):,}</p>
            <p><a href="https://www.youtube.com/watch?v={v_id}" style="background-color: #FF0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Watch Video</a></p>
        </div>
        """
    
    html_content += "</body></html>"
    return html_content

def send_mail(html_body):
    user = os.getenv("GMAIL_USER")
    pw = os.getenv("GMAIL_PASS")
    
    msg = EmailMessage()
    msg['Subject'] = "YouTube Top 10 Detailed Report"
    msg['From'] = user
    msg['To'] = user
    msg.add_alternative(html_body, subtype='html') # HTML ইমেইল পাঠানোর জন্য

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user, pw)
        smtp.send_message(msg)

if __name__ == "__main__":
    try:
        data = get_top_videos()
        send_mail(data)
        print("Detailed report sent!")
    except Exception as e:
        print(f"Error: {e}")
        
