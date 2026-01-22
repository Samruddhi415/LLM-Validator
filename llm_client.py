import os
import json
import requests
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"  

def parse_output(text: str) -> dict:
    
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = text[:-3] if text.endswith("```") else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"{.*}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError(f"Cannot find JSON in LLM output:\n{text}")

def call_groq(prompt: str) -> str:
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env")

    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "llama-3.3-70b-versatile",  
        "messages": [
            {"role": "system", "content": "You are a Python validation script."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 300
    }

    resp = requests.post(url, headers=headers, json=body)
    resp.raise_for_status()
    data = resp.json()
    text_output = data["choices"][0]["message"]["content"]
    return parse_output(text_output)

def build_prompt(json_input: dict) -> str:
    
    return f"""
You have to act like a strict python validation script and give the output like a code.
if any of the rules are violated you have to flag the exact rule like how a validation script works.
Reply only with the rules that are violated in errors and warnings and only those rules must be written in your replies.
STRICTLY No extra explanation or text should be given.
You have to only flag the rules that are not satisfied and resposnd only with the rules listed. 
You have to reply with BLANKS if ALL the rules are satisfied.
You can only and must reply in JSON format.
All the rules are equally important and must be satisfied.

Input JSON: {json.dumps(json_input)}
Validate based on these exact rules:
rules for Errors:
- name is required and non-empty
- email must be valid
- age must be positive
- country must be an ISO-2 code
- phone number must be in E.164 format

Rules for warnings:
- age < 18
- name shorter than 3 characters
- disposable email
- country code in phone number does not match country

Requirements:
- Output ONLY JSON
- Keys must be exactly: is_valid, errors[], warnings[]
- Recheck if all the rules for errors and warnings are satisfied.
- When the output is invalid state the exact rules violated.
- If all the rules are fulfilled you must leave errors BLANK 
- If all the rules are fulfilled you must leave warnings BLANK
- Only in case of rule violation of an error, you have to specify only the specific rule for error that was violated in the output
- Only in case of rule violation of a warning, you have to specify only the specific rule for warning that was violated in the output

Output ONLY JSON with keys:
is_valid, errors[], warnings[]
"""

