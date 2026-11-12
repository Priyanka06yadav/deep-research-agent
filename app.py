
import gradio as gr

from research_pipeline import run_research
from email_service import send_research_email
from models.schemas import EmailDraft

# FUNCTION 1: GENERATE RESEARCH


async def generate_research(
    research_question,
    recipient,
    recipient_name,
    progress=gr.Progress()
):

    if not research_question.strip():
        raise gr.Error("Please enter a research topic.")

    if not recipient.strip() or not recipient_name.strip():
        raise gr.Error("Please enter the recipient's name and email.")

    report, email_draft, report_path = await run_research(
        research_question=research_question,
        recipient=recipient,
        recipient_name=recipient_name,
        progress_callback=progress
    )

    follow_up_questions = "\n".join(
        f"- {question}"
        for question in report.follow_up_questions
    )

    return (
        report.short_summary,
        report.markdown_report,
        follow_up_questions,
        email_draft.subject,
        email_draft.body,
        str(report_path),
        "Research completed successfully.",
        str(report_path)
    )

# FUNCTION 2: SEND APPROVED EMAIL

def send_approved_email(
    recipient,
    subject,
    body,
    report_path,
    approved
):

    if not approved:
        raise gr.Error("Please confirm email approval before sending.")

    if not report_path:
        raise gr.Error("Please generate a research report first.")

    if not recipient.strip():
        raise gr.Error("Recipient email is missing.")

    email_draft = EmailDraft(
        subject=subject,
        body=body
    )

    result = send_research_email(
        recipient=recipient,
        email_draft=email_draft,
        report_path=report_path
    )

    return result


# CUSTOM CSS

custom_css = """

.gradio-container {
    max-width: 1450px !important;
    margin: auto !important;
    background: #f5f7fb !important;
}

.main-header {
    background: linear-gradient(120deg, #101c35, #203c68);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.main-header h1 {
    color: white !important;
    font-size: 32px !important;
    margin-bottom: 8px !important;
}

.main-header p {
    color: #d3def0 !important;
    font-size: 15px;
}

.header-tag {
    display: inline-block;
    background: #314c77;
    color: #dce9ff;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin-bottom: 15px;
}

.section-heading {
    font-size: 19px;
    font-weight: 700;
    color: #172b4d;
    margin-bottom: 12px;
}

.panel {
    background: white;
    border: 1px solid #e3e8f0;
    border-radius: 16px;
    padding: 20px;
}

.primary-button {
    min-height: 48px !important;
    font-weight: 600 !important;
}

.status-text {
    color: #28745a;
    font-weight: 600;
}

.footer-text {
    text-align: center;
    color: #8491a5;
    font-size: 12px;
    padding: 20px;
}

"""


# GRADIO APPLICATION

with gr.Blocks(title="AI Deep Research Agent") as demo:

    # HEADER

    gr.HTML("""
        <div class="main-header">
            <div class="header-tag">AI-POWERED RESEARCH WORKSPACE</div>
            <h1>Deep Research Agent</h1>
            <p>
                Transform complex questions into structured,
                evidence-based research reports.
            </p>
        </div>
    """)

    report_path_state = gr.State(value=None)

    # MAIN WORKSPACE

    with gr.Row(equal_height=False):

        # LEFT: RESEARCH CONFIGURATION

        with gr.Column(scale=1, min_width=300):

            gr.Markdown(
                "### Research Configuration"
            )

            research_question = gr.Textbox(
                label="Research Topic",
                placeholder="What are the latest developments in Agentic AI?",
                lines=5
            )

            gr.Markdown("### Email Details")

            recipient_name = gr.Textbox(
                label="Recipient Name",
                placeholder="Enter recipient name"
            )

            recipient = gr.Textbox(
                label="Recipient Email",
                placeholder="Enter email address"
            )

            research_button = gr.Button(
                "Start Research",
                variant="primary",
                elem_classes=["primary-button"]
            )

            status = gr.Markdown(
                "Ready to start your research.",
                elem_classes=["status-text"]
            )

            gr.Markdown("""
                ---
                **How it works**

                1. Initial web research
                2. Research planning
                3. Targeted web searches
                4. Report generation
                5. Email draft preparation
            """)

        # RIGHT: RESEARCH RESULTS

        with gr.Column(scale=2, min_width=450):

            gr.Markdown(
                "### Research Workspace"
            )

            with gr.Tabs():

                with gr.Tab("Summary"):

                    summary = gr.Markdown(
                        "Your research summary will appear here."
                    )

                with gr.Tab("Full Report"):

                    full_report = gr.Markdown(
                        "Your detailed research report will appear here."
                    )

                with gr.Tab("Follow-up Questions"):

                    follow_up = gr.Markdown(
                        "Suggested follow-up questions will appear here."
                    )

            download_button = gr.DownloadButton(
                "Download Research Report",
                variant="secondary"
            )

    # EMAIL SECTION

    gr.Markdown("---")

    gr.Markdown("### Email Draft & Approval")

    gr.Markdown(
        "Review the generated email. You can edit it before sending."
    )

    with gr.Column():

        email_subject = gr.Textbox(
            label="Email Subject"
        )

        email_body = gr.Textbox(
            label="Email Body",
            lines=10
        )

        approved = gr.Checkbox(
            label="I have reviewed this email and approve sending it."
        )

        send_button = gr.Button(
            "Send Email",
            variant="primary"
        )

        email_status = gr.Textbox(
            label="Email Delivery Status",
            interactive=False
        )

    # RESEARCH EVENT

    research_button.click(
        fn=generate_research,
        inputs=[
            research_question,
            recipient,
            recipient_name
        ],
        outputs=[
            summary,
            full_report,
            follow_up,
            email_subject,
            email_body,
            report_path_state,
            status,
            download_button
        ]
    )

    # EMAIL EVENT

    send_button.click(
        fn=send_approved_email,
        inputs=[
            recipient,
            email_subject,
            email_body,
            report_path_state,
            approved
        ],
        outputs=email_status
    )

    # FOOTER

    gr.HTML("""
        <div class="footer-text">
            AI Deep Research Agent · Powered by Gemini, Tavily and OpenAI Agents SDK
        </div>
    """)


# LAUNCH APPLICATION

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="blue",
            neutral_hue="slate"
        ),
        css=custom_css
    )
