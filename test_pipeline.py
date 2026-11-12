
import asyncio

from agents import Runner

from my_agents.search_agent import search_agent
from my_agents.planner_agent import planner_agent
from my_agents.writer_agent import writer_agent
from my_agents.emailer_agent import emailer_agent
from models.schemas import EmailDraft
from tools.email_tool import send_email
from utils.report_saver import save_report

from models.schemas import (
    InitialSearchSummary,
    WebSearchPlan,
    SearchResults,
    ReportData
)

from utils.structured_output import generate_structured_output


async def main():

    research_question = "What are the latest developments in agentic AI?"

    # STEP 1: Initial broad search

    print("\nStarting initial research...")

    initial_search = await Runner.run(
        search_agent,
        input=f"Perform a broad initial search on: {research_question}"
    )

    initial_findings = await generate_structured_output(
        instructions="Summarize the initial web research findings.",
        content=str(initial_search.final_output),
        output_schema=InitialSearchSummary
    )

    print("\nInitial research completed!")

    # STEP 2: Create research plan

    print("\nCreating research plan...")

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

    print("\nResearch plan created!")
    print(research_plan.model_dump_json(indent=2))


    # STEP 3: Targeted second search

    print("\nStarting targeted research...")

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

    print("\nTargeted research completed!")

    print(targeted_findings.model_dump_json(indent=2))


    # step 4: Generate Research report

    print("\nWriting research report...")

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

    report_path = save_report(report)

    print("\nResearch report generated!")

    print("\nSHORT SUMMARY:")
    print(report.short_summary)

    print("\nFULL RESEARCH REPORT:")
    print(report.markdown_report)

    print("\nFOLLOW-UP QUESTIONS:")
    for question in report.follow_up_questions:
        print("-", question)


    # Step 5: Prepare email draft

    print("\n Preparing email draft...")

    recipient  =  input("\nEnter recipient email address:")
    recipient_name = input("\nEnter recipient name: ")

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

    # STEP 6: Display email for approval

    print("\n========== EMAIL DRAFT ==========")

    print("\nTo:", recipient)
    print("Subject:", email_draft.subject)
    print("\nBody:\n")
    print(email_draft.body)

    # STEP 7: Ask for explicit approval

    approval = input(
        "\nDo you want to send this email? (yes/no): "
    )

    if approval.strip().lower() == "yes":

        send_email(
            recipient=recipient,
            subject=email_draft.subject,
            body=email_draft.body,
            attachment_path="reports/research_report.md"
        )

    else:

        print("\nEmail not sent. Draft discarded.")

if __name__ == "__main__":
    asyncio.run(main())
