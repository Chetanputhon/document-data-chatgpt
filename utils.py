import pandas as pd
import json

def parse_response_to_json(response_text):
    try:
        text = response_text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        return []

def save_to_excel(data, filename="structured_data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename