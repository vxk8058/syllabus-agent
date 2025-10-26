from crewai import Agent, Task, Crew
from utils import extract_text_from_pdf, extract_topics_from_text, build_study_plan, find_youtube_videos

# === Agents ===
parser_agent = Agent(
    role="Syllabus Parser",
    goal="Extract topics from a syllabus PDF or text input.",
    backstory="You're an expert at academic curriculum analysis."
)

research_agent = Agent(
    role="Research Assistant",
    goal="Find high-quality videos, PDFs, and articles for each topic.",
    backstory="You're excellent at finding concise, top-rated learning resources online."
)

planner_agent = Agent(
    role="Study Planner",
    goal="Create a 1-hour study plan using the best resources per topic.",
    backstory="You're skilled at time-efficient learning plans."
)

# === Crew Tasks ===
parse_task = Task(
    description="Extract topics from syllabus or user input.",
    agent=parser_agent,
    expected_output="List of topics."
)

research_task = Task(
    description="Search for top resources for each topic.",
    agent=research_agent,
    expected_output="Dictionary of topics → list of resources."
)

plan_task = Task(
    description="Create a 1-hour study plan from topics and resources.",
    agent=planner_agent,
    expected_output="Study schedule with topics, resource links, and time allocation."
)

# === Crew ===
crew = Crew(
    agents=[parser_agent, research_agent, planner_agent],
    tasks=[parse_task, research_task, plan_task]
)

# === Main Program ===
def main():
    mode = input("Input PDF syllabus (P) or topics manually (T)? ").strip().upper()
    
    if mode == "P":
        pdf_path = input("Enter PDF path: ").strip()
        syllabus_text = extract_text_from_pdf(pdf_path)
        topics = extract_topics_from_text(syllabus_text)
    else:
        topics = [t.strip() for t in input("Enter comma-separated topics: ").split(',')]

    print("\nExtracted Topics:")
    for t in topics:
        print("-", t)
    
    # --- User configuration ---
    try:
        total_minutes = int(input("Enter total study time in minutes (e.g., 60): ").strip())
    except:
        total_minutes = 60

    try:
        resources_per_topic = int(input("Enter number of resources per topic (e.g., 3): ").strip())
    except:
        resources_per_topic = 3


    # Research Agent
    topics_resources = {}
    for topic in topics:
        resources = find_youtube_videos(topic, max_results=resources_per_topic)
        topics_resources[topic] = resources

    # Planner Agent
    study_plan = build_study_plan(topics_resources, total_minutes=total_minutes, resources_per_topic=resources_per_topic)

    print("\n--- Study Plan ---")
    for entry in study_plan:
        print(f"\nTopic: {entry['topic']} ({entry['time_minutes']} min)")
        if entry['resources']:
            for r in entry['resources']:
                print(f"- {r['title']} ({r['duration']}) - {r['url']}")
        else:
            print("- No resources found")
            
    

if __name__ == "__main__":
    main()
