from transformers import AutoTokenizer

# Load once at module level
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", use_fast=True)

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text, truncation=False))