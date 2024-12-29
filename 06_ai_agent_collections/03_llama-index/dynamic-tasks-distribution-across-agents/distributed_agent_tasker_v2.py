from pydantic import BaseModel, Field
from openai import OpenAI
from typing import List
import os
import sys
import pickle
import keyring
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

# Set up OpenAI API client
client = OpenAI()

MODEL_TASK_HANDLER = "gpt-4o-mini"
MODEL_AGENT = "gpt-4o"
FOLDER_BASE = "./agent_artifacts"

serpapi_params = {
    "engine": "google",
    "api_key": os.getenv("SERP_API_KEY"),
}

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_NAME = 'GoogleCalendarAPI'
TOKEN_KEY = 'token'

class TaskHandler(BaseModel):
    tasks: List[str] = Field(description="List of tasks extracted from the user's message.")

def generate_task_list(task_input: str) -> List[str]:
    """Generates a list of tasks from the user's message."""
    
    response = client.beta.chat.completions.parse(
        model=MODEL_TASK_HANDLER,
        messages=[{"role": "system", "content": """
                   You take in text as a list of bullet points containing task descriptions
                    with potentially tool calling indicators specified with @tags you output a list 
                    ofthose tasks where each bullet point is an individual element in the list.
                    For example, if the input is: '''- Basic techniques of prompt engineering @web_search 
                    \n - LLMs for research @web_search\n - LLMs for programming @web_search @write_file @read_file\n'''
                    the output should be ['Basic techniques of prompt engineering @web_search', 
                    'LLMs for research @web_search', 'LLMs for programming @web_search @write_file @read_file']
                   """},
            {"role": "user", "content": task_input}],
        response_format=TaskHandler,
    )
    return response.choices[0].message.parsed.tasks

def extract_agent_task_and_tools(task_input: str):
    """Extracts the tasks and tools from each task in the list."""
    words = task_input.split()
    tags = [word for word in words if word.startswith("@")]
    task = ' '.join(word for word in words if not word.startswith('@'))
    
    return task.strip(), tags

def web_search(query: str) -> str:
    """Searches the web for the query and returns the results."""
    search = GoogleSearch({**serpapi_params, "q": query, "n": 5})
    results = search.get_dict()["organic_results"]
    search_results = "\n-----\n".join(
        ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
    )
    return search_results

def write_file(file_path: str, content: str) -> str:
    file_path = os.path.join(FOLDER_BASE, file_path)
    with open(file_path, "w") as f:
        f.write(content)
    return f"File {file_path} written successfully."

def read_file(file_path: str) -> str:
    file_path = os.path.join(FOLDER_BASE, file_path)
    with open(file_path, "r") as f:
        return f.read()

def authenticate_google_calendar():
    """Authenticate and authorize the user with Google Calendar API."""
    creds = None
    token_data = keyring.get_password(SERVICE_NAME, TOKEN_KEY)
    if token_data:
        creds = pickle.loads(token_data.encode('utf-8'))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        keyring.set_password(SERVICE_NAME, TOKEN_KEY, pickle.dumps(creds).decode('utf-8'))
    return build('calendar', 'v3', credentials=creds)

def create_calendar_event(event_details: dict) -> str:
    """Create a Google Calendar event."""
    service = authenticate_google_calendar()
    event = {
        'summary': event_details['summary'],
        'location': event_details.get('location', ''),
        'description': event_details.get('description', ''),
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_details['end_time'],
            'timeZone': 'UTC',
        },
        'attendees': [{'email': attendee} for attendee in event_details.get('attendees', ['abc@gmail.com'])],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60 * 24 * 7},  # 1 week
                {'method': 'email', 'minutes': 60 * 24 * 2},  # 2 days
                {'method': 'email', 'minutes': 60 * 24},      # 1 day
                {'method': 'email', 'minutes': 120},          # 2 hours
            ],
        },
    }
    try:
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {created_event.get('htmlLink')}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_todays_events() -> str:
    """Get today's events from Google Calendar."""
    service = authenticate_google_calendar()
    now = datetime.utcnow().isoformat() + 'Z'
    end_of_day = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=end_of_day, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return "No events found for today."
    return "\n".join([f"{event['summary']} at {event['start'].get('dateTime', event['start'].get('date'))}" for event in events])

def get_events_on_date(date: str) -> str:
    """Get events on a specific date from Google Calendar."""
    service = authenticate_google_calendar()
    start_of_day = datetime.strptime(date, "%Y-%m-%d").isoformat() + 'Z'
    end_of_day = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=start_of_day,
                                          timeMax=end_of_day, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return f"No events found for {date}."
    return "\n".join([f"{event['summary']} at {event['start'].get('dateTime', event['start'].get('date'))}" for event in events])

def delete_event(event_id: str) -> str:
    """Delete an event from Google Calendar."""
    service = authenticate_google_calendar()
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f"Event {event_id} deleted successfully."
    except Exception as e:
        return f"An error occurred: {e}"

tool_mapping = {
    "web_search": web_search,
    "write_file": write_file,
    "read_file": read_file,
    "create_calendar_event": create_calendar_event,
    "get_todays_events": get_todays_events,
    "get_events_on_date": get_events_on_date,
    "delete_event": delete_event,
}

def create_agent(llm, tools):
    """Create an agent with a set of tools"""
    
    tools_list = []
    for tool in tools:
        tool = tool.strip("@")
        tool = FunctionTool.from_defaults(fn=tool_mapping[tool])
        tools_list.append(tool)
    return ReActAgent.from_tools(tools_list, llm=llm, verbose=True, max_iterations=10)

def main():
    task_string = sys.argv[1]
    llm = LlamaOpenAI(
        model=MODEL_AGENT,
        system_prompt="""
        You are a helpful assistant that can search the web,
        read files, write to files, and manage calendar events. If you're given the write_file tool
        you should always use it at the end of the task to compile 
        the outputs of the research or other tasks. When given the web_search tool, 
        you should always use it to search the web for information relevant to the 
        task one to 3 times at the max, then write the results of that search with 
        the sources used in an organized document.
        """)
    task_list = generate_task_list(task_string)
    
    for task in task_list:
        print(f"Processing task: {task}")
        agent_task, agent_tools = extract_agent_task_and_tools(task)
        agent = create_agent(llm, agent_tools)
        response = agent.chat(agent_task)
        print("OUTPUT: ", response)
        

if __name__ == "__main__":
    main()
