from openai import OpenAI


def get_tips(disaster_keywords: str, user_role: str, client: OpenAI) -> str:
    """
    Generate a summary or vital advice for a disaster using OpenAI's ChatGPT.

    Args:
        disaster_keywords: Keywords describing the disaster (e.g., "Earthquake in China").
        user_role: User's role (e.g., "victim", "supporter").
        client: Initialized OpenAI client.

    Returns:
        A string containing 1-2 sentences of vital advice or summary.
    """
    user_role_improved = "volunteer looking to help victims" if user_role.lower() == "supporter" else user_role

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a 1-2 sentence text containing the most vital advice for a "
                               f"{user_role_improved} of this disaster: {disaster_keywords}. It is important "
                               f"that you repeat the name of the disaster, and take into account that this message "
                               f"is for a user of an emergency app, that is currently a {user_role_improved} of this disaster. "
                               f"Adding to this, make research on this disaster and find helpful information, like "
                               f"emergency points, volunteering organizations, etc..."
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating summary from OpenAI: {str(e)}")
