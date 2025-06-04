import asyncio
from agents import Runner, trace, gen_trace_id
from base_planner_agent import WebSearchPlan, WebSearchPlanItem, planner_agent
from base_search_agent import base_search_agent as search_agent
from base_writer_agent import ReportData, base_writer_agent as writer_agent
from base_email_agent import base_email_agent as email_agent


class BaseResearchManager:
    async def run(self, query: str):
        """Run the base research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()

        with trace("Base Research", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")

            # step 1: create the search plan
            yield "Planning searches..."
            plan_search_result = await self.plan_searches(query)

            yield "Searches planned, starting to search..."

            # step 2: perform the searches
            yield "Performing searches..."
            search_results = await self.perform_searches(plan_search_result)

            # step 3: write the report
            yield "Writing report..."
            report = await self.write_report(query, search_results)

            #yield "Report written, sending email..."
            #await self.send_email(report)

            #yield "Email sent, research complete"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )

        print(result.final_output)
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        print("Performing searches...")
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]

        results = []
        performed_search_count = 0

        for task in asyncio.as_completed(tasks):
            result = await task

            if result is not None:
                results.append(result)
                performed_search_count += 1
                print(f"Searching... {performed_search_count}/{len(tasks)} completed")

        print("Finished searching")

        return results

    async def search(self, search_term: WebSearchPlanItem) -> str:
        print(f"Searching for {search_term}")

        input = f"Search term: {search_term.query}\nReason for searching: {search_term.reason}"

        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        print("Writing report...")
        input = f"Query: {query}\nSearch results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        print("Sending email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Finished sending email")
