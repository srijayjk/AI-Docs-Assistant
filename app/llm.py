import requests


def generate_answer(full_prompt, model="llama3.2:3b"):
    try:
        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        # DEBUG: Print this to be sure
        print("🧠 Ollama responded:", data)

        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print(f"⚠️ HTTP Request Error: {e}")
        return "Ollama generation failed (HTTP error)."

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return "Ollama generation failed (unexpected error)."