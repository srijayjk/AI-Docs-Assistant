import requests

def generate_answer(prompt, context, model="llama3.2:3b"):
    full_prompt = f"Answer the question based on the following context:\n\n{context}\n\nQuestion: {prompt}"
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": False
        }
    )
    
    data = response.json()
    return data.get("response", "No response")
