def ask_ollama(prompt: str):
    try:
        import ollama
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except:
        return None
