from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt4_for_structure(file_text, instruction):
    prompt = f"""
You are a document data extractor.

Extract structured data based on the instruction below. Return result ONLY as valid JSON.

Instruction:
{instruction}

Document content:
{file_text[:4000]}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
