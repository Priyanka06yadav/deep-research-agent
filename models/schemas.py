from pydantic import BaseModel
from typing import List

# Search agent output
class InitialSearchSummary(BaseModel):
    summary: str
    key_findings: List[str]
    sources: List[str]

# Planner agent output
class WebSearchPlan(BaseModel):
    research_topic: str
    research_areas: List[str]
    search_queries: List[str]

# Second search agent output
class SearchResult(BaseModel):
    query: str
    findings: List[str]
    sources: List[str]

class SearchResults(BaseModel):
    results: List[SearchResult]

# Writern agent output
class ReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: List[str]

# Emailer agent output
class EmailDraft(BaseModel):
    subject: str
    body: str
