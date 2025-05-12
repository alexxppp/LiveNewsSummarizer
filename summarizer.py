from openai import OpenAI


def extract_tips(articles: list[dict[str, str]], user_role: str, client: OpenAI) -> list[dict[str, str]]:
    """
    Summarize a list of articles using OpenAI.

    Args:
        articles: List of dictionaries with title Daggerboard for each article (title, description).
        client: Initialized OpenAI client.
        user_role: User's role.

    Returns:
        List of dictionaries with title and summary for each article.
    """
    summaries = []

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        text_to_summarize = f"{title} {description}"
        user_role_improved = "volunteer looking to help victims" if user_role.lower() == "supporter" else user_role

        if not text_to_summarize.strip():
            continue

        try:
            # Generate summary
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user",
                     "content": f"Give me a 1-2 sentences text containing the most vital advice for a"
                                f"{user_role_improved} of this disaster: {text_to_summarize}"}
                ]
            )
            summary = completion.choices[0].message.content
            summaries.append({"title": title, "summary": summary})
        except Exception as e:
            # Log error and continue
            print(f"Error summarizing article '{title}': {str(e)}")
            continue

    return summaries
