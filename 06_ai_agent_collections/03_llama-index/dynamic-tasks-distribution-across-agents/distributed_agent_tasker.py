from pydantic import BaseModel, Field
from openai import OpenAI
from typing import List
import os
import sys
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

# print(generate_task_list("""- Basic techniques of prompt engineering @web_search 
#                     \n - LLMs for research @web_search"""))

def extract_agent_task_and_tools(task_input: str):
    """
    Extracts the tasks and tools from each task in the list.
    """
    words = task_input.split()
    tags = [word for word in words if word.startswith("@")]
    task = ' '.join(word for word in words if not word.startswith('@'))
    
    return task.strip(), tags

# print(extract_agent_task_and_tools("Basic techniques of prompt engineering @web_search"))

def web_search(query: str) -> str:
    """
    Searches the web for the query and returns the results.
    """
    search = GoogleSearch({**serpapi_params, "q": query, "n": 5})
    print(search.get_dict())
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

# print(web_search("What is the best way to learn how to use LLMs for personal productivity?"))

tool_mapping = {
    "web_search": web_search,
    "write_file": write_file,
    "read_file": read_file,
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
        read files, write to files. If you're given the write_file tool
        you should always use it at the end of the task to to compile 
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