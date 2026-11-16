# Python
import pytest
from src.engine import RuleEngine

@pytest.fixture
def engine():
    return RuleEngine("data/intents.json")

def test_sanitization(engine):
    assert engine.sanitize_input("  HELLO World!!! ") == "hello world"

def test_intent_greeting(engine):
    tag, response = engine.match_intent("hey there")
    assert tag == "greeting"

def test_intent_exit(engine):
    tag, response = engine.match_intent("I want to exit now")
    assert tag == "exit"

def test_fallback(engine):
    tag, response = engine.match_intent("xyz123 random prompt")
    assert tag == "fallback"