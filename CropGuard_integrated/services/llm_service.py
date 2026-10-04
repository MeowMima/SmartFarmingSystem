
import os
import requests

def get_llm_solution(disease):
    api_key = os.getenv("OPENROUTER_API_KEY")

    # Graceful fallback: never expose API errors to the farmer.
    if not api_key:
        return (
            "Disease Name: N/A\n"
            "Caused By: N/A\n"
            "Prevention: N/A"
        )

    prompt = f"""Give output EXACTLY in this format:

Disease Name: <text>
Caused By: <text>
Prevention: <text>

Each must be on a separate line.
Each under 10 words.
No extra explanation.

Disease: {disease}
"""

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=8,
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception:
        return (
            "Disease Name: N/A\n"
            "Caused By: Information unavailable\n"
            "Prevention: Use local agricultural guidance"
        )

def parse_llm_response(text):
    data = {
        "Disease Name": "",
        "Caused By": "",
        "Prevention": "",
    }

    for line in text.splitlines():
        if "Disease Name" in line:
            data["Disease Name"] = line.split(":", 1)[-1].strip()
        elif "Caused By" in line:
            data["Caused By"] = line.split(":", 1)[-1].strip()
        elif "Prevention" in line:
            data["Prevention"] = line.split(":", 1)[-1].strip()

    return data
