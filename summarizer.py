from openai import OpenAI


def get_tips(disaster_keywords: str, user_role: str, client: OpenAI) -> str:
    """
    Summarize a list of articles using OpenAI.

    Args:
        articles: List of dictionaries with title Daggerboard for each article (title, description).
        client: Initialized OpenAI client.
        user_role: User's role.

    Returns:
        List of dictionaries with title and summary for each article.
    """
    summary = ""

    user_role_improved = "volunteer looking to help victims" if user_role.lower() == "supporter" else user_role

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"Give me a 1-2 sentences text containing the most vital advice for a"
                        f"{user_role_improved} of this disaster: {disaster_keywords}"}
        ]
    )

    return completion.messages[0]["content"]
