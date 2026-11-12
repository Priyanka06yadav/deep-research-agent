import asyncio

from agents import Runner

from my_agents.search_agent import search_agent
from my_agents.planner_agent import planner_agent
from my_agents.writer_agent import writer_agent
from my_agents.emailer_agent import emailer_agent

from models.schemas import (
    InitialSearchSummary,
    WebSearchPlan,
    SearchResults,
    ReportData,
    EmailDraft
)

from utils.structured_output import generate_structured_output
from utils.report_saver import save_report

async def run_research(
        research_question: str,
        recipient: str,
        recipient_name: str,
        progress_callback=None
):
        if progress_callback:
            progress_callback(0.05, desc="Starting initial web research...")

        # Step 1: Initial broad search

        initial_search = await Runner.run(
        search_agent,
        input=f"Perform a broad initial search on: {research_question}"
    )

        initial_findings = await generate_structured_output(
            instructions="Summarize the initial web research findings.",
            content=str(initial_search.final_output),
            output_schema=InitialSearchSummary
        )

        if progress_callback:
            progress_callback(0.25, desc="Initial research completed!")

        # Step 2: Create research plan

        planner_input = f"""
            Original Research Question:
            {research_question}

            Initial Research Findings:
            {initial_findings.model_dump_json(indent=2)}
            """

        planner_result = await Runner.run(
                planner_agent,
                input=planner_input
            )

        research_plan = await generate_structured_output(
                instructions="Create a detailed research plan with focused research areas and search queries.",
                content=str(planner_result.final_output),
                output_schema=WebSearchPlan
            )

        if progress_callback:
            progress_callback(0.40, desc="Research plan created!")

        # Step 3: Targeted second search

        targeted_search = await Runner.run(
        search_agent,
        input=f"""
        Original Research Question:
        {research_question}

        Execute the following targeted search queries.
        Search for each query separately:

        {chr(10).join(research_plan.search_queries)}
        """
    )

        targeted_findings = await generate_structured_output(
            instructions="Organize the targeted web research findings by search query. Include relevant findings and source URLs.",
            content=str(targeted_search.final_output),
            output_schema=SearchResults
        )

        if progress_callback:
            progress_callback(0.65, desc="Targeted research completed!")

        # step 4: Generate research report

        writer_input = f"""
        Original Research Question:
        {research_question}

        Initial Research Findings:
        {initial_findings.model_dump_json(indent=2)}

        Research Plan:
        {research_plan.model_dump_json(indent=2)}

        Targeted Research Findings:
        {targeted_findings.model_dump_json(indent=2)}

        """

        writer_result = await Runner.run(
        writer_agent,
        input=writer_input
    )

        report = await generate_structured_output(
            instructions="""
            Convert the research analysis into a comprehensive
            Markdown report.

            Return:
            1. A concise short summary.
            2. A detailed Markdown report.
            3. A list of useful follow-up research questions.
            """,
            content=str(writer_result.final_output),
            output_schema=ReportData
        )

        if progress_callback:
            progress_callback(0.85, desc="Research report generated!")

        # Save Report

        report_path = save_report(report)

        # Step 5: Generate email draft
        
        email_input  = f"""

        Recipient Email: {recipient}

        Recipient Name: {recipient_name}

        Research Question: {research_question}

        Research Summary: {report.short_summary}

        Research Report: {report.markdown_report} 
    """

        emailer_result = await Runner.run(
            emailer_agent,
            input = email_input
        )

        email_draft = await generate_structured_output(

            instructions="""

            Generate a professional email using the research
            report and recipient information.

            Return the recipient, subject, and email body.
            
            """,

            content = str(emailer_result.final_output),
            output_schema=EmailDraft
        )

        if progress_callback:
            progress_callback(1.0, desc="Research completed! Email draft is ready.") 

        # Return results to Gradio
        return report, email_draft, report_path     

