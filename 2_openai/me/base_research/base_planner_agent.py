from pydantic import BaseModel, Field
from agents import Agent
import os


INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {os.environ.get('HOW_MANY_SEARCHES', 5)} terms to query for."
)


class WebSearchPlanItem(BaseModel):
    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchPlanItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
