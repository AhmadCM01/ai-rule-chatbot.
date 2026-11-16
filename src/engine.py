# Python
import json
import re
import logging

logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class RuleEngine:
    def __init__(self, intents_path: str):
        self.intents = self._load_intents(intents_path)

    def _load_intents(self, path: str) -> list:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("intents", [])
        except Exception as e:
            logging.error(f"Failed to load intents file: {e}")
            return []

    def sanitize_input(self, text: str) -> str:
        text = text.lower().strip()
        # Remove special characters except spaces
        return re.sub(r"[^\w\s]", "", text)

    def match_intent(self, raw_input: str) -> tuple[str, str]:
        cleaned = self.sanitize_input(raw_input)
        if not cleaned:
            return "fallback", "Please provide a valid text input."

        for intent in self.intents:
            tag = intent.get("tag")
            patterns = intent.get("patterns", [])
            for pattern in patterns:
                # Word boundary match using regex for exact pattern matching
                if re.search(r"\b" + re.escape(pattern) + r"\b", cleaned):
                    logging.info(f"Matched intent '{tag}' for input: '{raw_input}'")
                    return tag, intent.get("responses")[0]

        logging.warning(f"Fallback triggered for input: '{raw_input}'")
        return "fallback", "I'm sorry, I couldn't understand your request. Could you rephrase?"
