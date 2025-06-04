import gradio as gr
from base_research_manager import BaseResearchManager


async def run(query: str):
    async for chunk in BaseResearchManager().run(query):
        yield chunk


with gr.Blocks() as ui:
    gr.Markdown("# Base Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")

    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)
    run_button.click(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)
