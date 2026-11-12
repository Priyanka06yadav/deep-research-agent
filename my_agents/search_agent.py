from agents import Agent
from config import model
from tools.web_search import web_search
from models.schemas import InitialSearchSummary

search_agent = Agent(
    name="SearchAgent",

    instructions=
    """
    You are a web research agent.

    You will receive a research question or a list of
    targeted search queries.

    Your job is to:
    1. Search the web using the search_web tool.
    2. Execute all the provided search queries.
    3. Collect relevant and factual information.
    4. Include useful source URLs.
    5. Avoid repeating information unnecessarily.

    Return the collected research findings clearly.
    Do not invent facts or sources.
    """,
    tools=[web_search],
    model=model
)

