import os
from dotenv import load_dotenv
from tavily import TavilyClient
from agents import function_tool

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@function_tool
def web_search(query: str) -> str:
    """
    Search the internet for information related to the given query.

    Args:
        query (str): The topic or question to search for.
    """

    response =  tavily_client.search(
        query = query,
        max_results = 5
    )

    formatted_results = []

    for result in response['results']:
        formatted_results.append(f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n")

    return "\n\n".join(formatted_results)