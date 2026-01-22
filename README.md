# LLM-Powered Input Validator
A Python-based validation engine that uses Large Language Models (LLMs) to perform data validation. The goal is to build a validator where the LLM is the sole source of logic. By using advanced prompt engineering, we ensure the model returns strictly structured JSON that can be integrated into automated workflows.

## Tech Stack

Language: Python 3.10+  
LLM Provider: Groq (Llama-3.3-70b-versatile)  
Testing & Evals: Promptfoo  

## Getting Started

1. Prerequisites

Python 3.10 or higher installed  
Node.js
Promptfoo installed    
A Groq API Key

2. Installation

```Bash
# Clone the repository
git clone <your-repo-url>
cd llm-validator

# Install Python dependencies
pip install -r requirements.txt

# Install Promptfoo globally
npm install -g promptfoo
```
3. Configuration

Create a .env file in the root directory and add your API key:

```Code snippet
GROQ_API_KEY=your_groq_api_key_here
```
## Usage

To validate a user profile, pass a JSON file to the validate_user.py script:

```Bash
python validate_user.py path/to/your_input.json
```

Example Input

```JSON
{
  "name": "",
  "email": "user@gmail",
  "age": 16,
  "country": "India",
  "phone": "99999"
}
```

Example Output

```JSON
{
  "is_valid": false,
  "errors": [
    "name is required and non-empty",
    "email must be valid",
    "country must be an ISO-2 code",
    "phone number must be in E.164 format"
  ],
  "warnings": [
    "age < 18",
    "disposable email"
  ]
}
```

## Automated Evaluations

We use Promptfoo to ensure the LLM remains grounded and follows the schema strictly. The evaluation suite tests for:

Schema Integrity: Ensures is_valid, errors, and warnings always exist.

Replay Protection: Ensuring the same input yields the same validation results.

Semantic Accuracy: Verifying that specific rules (like ISO-2 or E.164) are caught.

To run the evaluations:

```Bash
npx promptfoo eval
```

To view the results in a web browser:

```Bash
npx promptfoo view
```

## Repository Structure

validate_user.py: Main entry point for the CLI tool.

llm_client.py: Handles API communication and prompt building.

promptfooconfig.yaml: Defines the test cases and validation assertions.

test_data/: Contains JSON files for testing.

requirements.txt: Python dependencies.
