from agents import Agent, Runner, gen_trace_id
from pydantic import BaseModel, Field

INSTRUCTIONS = """
You are a helpful assistant that can write a report based on the information provided.
you will be given a query and search results was done by research assistant.
you should come up with define the outline of the report and then write the report.
the report should format in markdown and highlight the most important points.
the content of report should limit within 1000 words and maximum 3-5 pages
"""


class ReportData(BaseModel):
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(
        description="Suggested topics to research further"
    )


base_writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
