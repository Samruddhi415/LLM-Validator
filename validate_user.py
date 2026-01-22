import sys
import json
from llm_client import call_groq, build_prompt


def load_input(file_path: str) -> dict:
    with open(file_path) as f:
        return json.load(f)

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_user.py input.json")
        sys.exit(1)

    input_file = sys.argv[1]
    inp_json = load_input(input_file)

    prompt = build_prompt(inp_json)
    output_json = call_groq(prompt)

    print(json.dumps(output_json, indent=2))

if __name__ == "__main__":
    main()
