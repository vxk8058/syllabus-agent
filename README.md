# Syllabus-Agent

AI-powered study planner that extracts topics from a syllabus PDF or manual input and generates a time-efficient study plan with curated online (youtube) resources.

## Features
- Uses OpenAI GPT-4 to identify key topics and subtopics from a syllabus.
- Fetches top YouTube tutorials with video durations for each topic.
- Customizable study time and resources per topic.
- Built using CrewAI for modular, role-based task handling.

## Tech Stack
- Python 3.12
- OpenAI API
- Youtube Data API v3
- CrewAI
- PyPDF2
- Google API Client
- python-dotenv

## Setup & Installation
1. Clone the repo
- git clone https://github.com/vxk8058/syllabus-agent.git
- cd syllabus-agent

2. Create a Virtual Environment
- python3 -m venv venv
- source venv/bin/activate

3. Install Dependencies
- pip install -r requirements.txt

4. Add Environment Variables
- OPENAI_API_KEY=your_openai_api_key
- YOUTUBE_API_KEY=your_youtube_api_key

5. Run the program
- python main.py

### You will be promted to:
- Upload a PDF Syllabus or enter topics manually
- Specify total study time (in minutes)
- Choose the number of resources per topic

## Future Improvements
- Enhance the AI Parser to handle different syllabus/curricular formats (PDFs, DOCX, slides.etc).
- Integrate articles, blogs, and PDFs alongside YouTube videos.
- Upgrade the study planner logic to dynamically allocate the time.
