from openai import OpenAI


def get_suggestion(request_text: str, client: OpenAI):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Determine the urgency level of this help request of a victim of a natural disaster."
                               f"The urgencies levels can be the following: Low, Moderate, High, or Very High."
                               f"This is the request text: {request_text}."
                               f"return only one word (or two if needed), representing the urgency level."
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error while evaluating the request need level: {str(e)}")
