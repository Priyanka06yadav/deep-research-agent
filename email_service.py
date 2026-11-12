from tools.email_tool import send_email


def send_research_email(
    recipient: str,
    email_draft,
    report_path
):

    send_email(
        recipient=recipient,
        subject=email_draft.subject,
        body=email_draft.body,
        attachment_path=str(report_path)
    )

    return "Email sent successfully!"