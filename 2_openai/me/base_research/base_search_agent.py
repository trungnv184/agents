from agents import Agent, ModelSettings, Runner, WebSearchTool, gen_trace_id


INSTRUCTIONS = """
You are a helpful assistant that can search the web for information.
you will given a search term and a reason for searching.
you will search the web based on the information provided.
you produce the concise summary of the results.
the summary must be 2-3 paragraphs and less than 300 words and highlight the most important points.
"""

base_search_agent = Agent(
    name="SearchAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)
