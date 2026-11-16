# Python
from src.engine import RuleEngine

def main():
    engine = RuleEngine("data/intents.json")
    print("=" * 60)
    print("      DECODELABS AI RULE-BASED ENGINE (v1.0)")
    print("=" * 60)
    print("Type 'exit' or 'bye' to end the conversation.\n")

    while True:
        try:
            user_input = input("You > ")
            tag, response = engine.match_intent(user_input)
            print(f"Bot > {response}\n")

            if tag == "exit":
                break
        except KeyboardInterrupt:
            print("\nSession terminated.")
            break

if __name__ == "__main__":
    main()
