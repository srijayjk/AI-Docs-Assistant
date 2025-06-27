import requests


def generate_answer(full_prompt, model="llama3.2:3b"):
    print(f" 📄 Prompt:  {full_prompt} ")
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": False
        }
    )

    try:
        data = response.json()
        a = data.get("response", "No response")
        print(f"📄 Got to Generate Answer LLM.py {a}")
        return data.get("response", "No response")
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "Error generating response"