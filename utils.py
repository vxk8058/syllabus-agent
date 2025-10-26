import PyPDF2
from googlesearch import search
import os
from dotenv import load_dotenv
from openai import OpenAI
from googleapiclient.discovery import build
import isodate


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- PDF Reader ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# --- Topic extraction via LLM ---
def extract_topics_from_text(text, max_topics=10):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Extract the main topics and subtopics from this syllabus:\n{text[:3000]}"
        }]
    )
    return [t.strip() for t in response.choices[0].message.content.split('\n')[:max_topics]]


# --- Resource search ---
def find_resources(topic, num_results=5):
    query = f"{topic} lecture site:youtube.com OR site:medium.com OR filetype:pdf"
    return list(search(query, num_results=num_results))


# --- Planner: allocate time per topic ---
def build_study_plan(topics_resources, total_minutes=60, resources_per_topic=3):
    plan = []
    num_topics = len(topics_resources)
    if num_topics == 0:
        return plan
    time_per_topic = max(total_minutes // num_topics, 5)
    
    for topic, resources in topics_resources.items():
        plan.append({
            "topic": topic,
            "time_minutes": time_per_topic,
            "resources": resources[:resources_per_topic]  # list of dicts now
        })
    return plan


# --- YouTube Data API ---
def find_youtube_videos(topic, max_results=3):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    request = youtube.search().list(
        q=f"{topic} tutorial",
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    
    videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get video duration using YouTube Videos API
        video_request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        video_response = video_request.execute()
        iso_duration = video_response['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(iso_duration)
        # Convert to mm:ss
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        duration_str = f"{minutes}:{seconds:02d}"
        
        videos.append({
            'title': title,
            'url': url,
            'duration': duration_str
        })
    
    return videos