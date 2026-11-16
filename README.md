# DecodeLabs AI Rule-Based Chatbot

A small, local, command-line chatbot that maps user text to predefined intents and responses. It uses deterministic pattern matching; it does not call an AI model, train on data, or require a network connection.

## What it does

- Reads intent definitions from `data/intents.json`.
- Normalizes input to lowercase, trims surrounding whitespace, and removes punctuation.
- Searches configured patterns using regular-expression word boundaries.
- Returns the first response for the first matching intent, or a fallback response if there is no match.
- Provides a terminal chat loop that ends when an intent tagged `exit` is matched, or when the user presses Ctrl+C.

This is a starter rule engine, not a general-purpose conversational AI or a production service. It has no API, persistence layer, authentication, or runtime dependency on an external model.

## Requirements

- Python 3.10 (the version used by CI)
- pip

The application code uses the Python standard library. `requirements.txt` contains the project's test and lint tools: pytest and flake8.

## Quick start

Run these commands from the repository root.

### Windows PowerShell

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.main
```

### macOS or Linux

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.main
```

Example session:

```text
DECODELABS AI RULE-BASED ENGINE (v1.0)
Type 'exit' or 'bye' to end the conversation.

You > hello
Bot > Hello! Welcome to DecodeLabs AI support. How can I assist you today?
```

The displayed response depends on the matched intent. To end the session, enter a phrase matching the `exit` intent, such as `bye` or `quit`, or press Ctrl+C.

## How matching works

`RuleEngine` in `src/engine.py` loads the JSON file when it is initialized. For each message, it:

1. Converts the message to lowercase, strips its leading and trailing whitespace, and removes characters other than word characters and whitespace.
2. Checks patterns in the order they appear in the intent file. A pattern is matched with regex word boundaries, so a pattern such as `hi` does not match inside a longer word such as `this`.
3. Returns a `(tag, response)` pair using the matched intent's first response.
4. Returns a fallback tag and message if the normalized input is empty or no pattern matches.

There is no ranking, confidence score, multi-intent handling, or random response selection. If more than one pattern matches, ordering in `intents.json` determines which intent wins.

## Configuring intents

Add or edit entries in `data/intents.json`. Each intent should have a descriptive `tag`, a list of `patterns`, and a non-empty list of `responses`. For example:

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["hello", "hi", "good morning"],
      "responses": ["Hello! How can I help?"]
    }
  ]
}
```

The file's top-level object must contain an `intents` array. Put more specific intents before broader ones when their patterns could overlap. The current engine returns only the first response from a matching intent.

To add an intent, update the JSON and add or update tests in `tests/test_engine.py`. The command-line interface exits only when the returned tag is exactly `exit`.

## Project layout

```text
.
├── data/
│   └── intents.json       # Intent patterns and response text
├── src/
│   ├── engine.py          # Input normalization and intent matching
│   └── main.py            # Interactive command-line entry point
├── tests/
│   └── test_engine.py     # Engine behavior tests
├── requirements.txt       # pytest and flake8
└── .github/
    └── workflows/
        └── ci-cd.yml      # Lint and test workflow
```

## Tests and CI

Run the test suite from the repository root:

```bash
python -m pytest
```

Run the same two lint checks used in CI:

```bash
python -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

The GitHub Actions workflow runs on pushes and pull requests targeting `main`. It installs Python 3.10, runs both flake8 checks, and executes pytest. The second lint check is advisory (`--exit-zero`); the first fails the workflow on the selected critical errors.

## Operational notes and limitations

- The application expects `data/intents.json` relative to the current working directory. Launch it from the repository root.
- Intent-file loading errors are written to the log, but the engine continues with an empty intent list. In that case, valid messages receive the normal fallback response.
- Logging is configured in `src/engine.py` to write to `chatbot.log` in the current working directory. Matched and unmatched user text is included in log messages. Avoid entering sensitive information, and review or disable this logging before using the chatbot with real user data.
- The engine assumes each configured intent has a tag, patterns, and at least one response. Keep the JSON valid and follow the schema above.
- CI currently targets Python 3.10; compatibility with other Python versions is not established by this workflow.
- No license file is currently included. Confirm the project's licensing before redistributing it.
