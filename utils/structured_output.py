
import json

from config import gemini_client


async def generate_structured_output(
    instructions: str,
    content: str,
    output_schema,
    model_name: str = "gemini-2.5-flash"
):

    schema = output_schema.model_json_schema()

    response = await gemini_client.chat.completions.create(

        model=model_name,

        messages=[
            {
                "role": "system",
                "content": f"""
                {instructions}

                Return a JSON object matching this schema:

                {json.dumps(schema)}

                Return valid JSON only.
                """
            },
            {
                "role": "user",
                "content": content
            }
        ],

        response_format={"type": "json_object"}
    )

    structured_output = output_schema.model_validate_json(
        response.choices[0].message.content
    )

    return structured_output
