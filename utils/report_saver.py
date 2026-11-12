from pathlib import Path
from datetime import datetime

def save_report(report):

    reports_dir = Path("reports")

    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_content = f"""
# Research Report

## Short Summary

{report.short_summary}


{report.markdown_report}


## Follow-up Questions
"""
    for question in report.follow_up_questions:

        report_content += f"- {question}\n"

    file_path = reports_dir / f"research_report_{timestamp}.md"

    file_path.write_text(
        report_content,
        encoding="utf-8"
    )

    print(f"\nReport saved successfully: {file_path}")

    return file_path