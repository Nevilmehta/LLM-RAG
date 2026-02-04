import ollama

MODEL = "phi"  # or "llama3" "mistral"

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Be concise. If you're unsure, say you don't know."
)

def print_help():
    print(
        "\nCommands:\n"
        "  /help                 Show commands\n"
        "  /exit                 Quit\n"
        "  /reset                Clear chat history (keeps current system prompt)\n"
        "  /system               Show current system prompt\n"
        "  /system <new prompt>  Set a new system prompt\n"
    )

def main():
    system_prompt = DEFAULT_SYSTEM_PROMPT
    messages = [{"role": "system", "content": system_prompt}]

    print("CLI Chatbot\n(type /help for commands)\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ["/exit", "exit", "quit"]:
            print("Bye!")
            break

        if cmd == "/help":
            print_help()
            continue

        if cmd == "/reset":
            messages = [{"role": "system", "content": system_prompt}]
            print("(history cleared)\n")
            continue

        # /system handling
        if cmd == "/system":
            print(f"\n(Current system prompt)\n{system_prompt}\n")
            continue

        if user_input.startswith("/system "):
            new_prompt = user_input[len("/system "):].strip()
            if not new_prompt:
                print("(Please provide a system prompt after /system)\n")
                continue

            system_prompt = new_prompt
            # Reset history to avoid mixing old behavior with new rules
            messages = [{"role": "system", "content": system_prompt}]
            print("\n(System prompt updated + history reset)\n")
            continue

        # Normal chat message
        messages.append({"role": "user", "content": user_input})

        response = ollama.chat(
            model=MODEL,
            messages=messages,
            options={"temperature": 0.7}
        )

        assistant_text = response["message"]["content"].strip()
        print(f"\nAssistant: {assistant_text}\n")

        messages.append({"role": "assistant", "content": assistant_text})

if __name__ == "__main__":
    main()
