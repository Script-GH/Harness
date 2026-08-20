import json

from llm import call_llm
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools for listing, reading, "
    "and writing files inside a workspace directory. Use them when needed."
)


def run_tool(name, args):
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return f"Error: no such tool '{name}'"
    try:
        return fn(**args)
    except Exception as e:
        return f"Error: {e}"


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Basic harness. Type 'exit' to quit.")

    while True:
        user_input = input("\nyou> ").strip()
        if user_input in ("exit", "quit"):
            break
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})

        # Inner loop: keep going until the model responds with plain text
        # instead of a tool call. This is the core of an agent harness -
        # everything else (permissions, streaming, sub-agents) builds on it.
        while True:
            response = call_llm(messages, TOOLS)
            message = response.choices[0].message
            messages.append(message.model_dump(exclude_none=True))

            if not message.tool_calls:
                print(f"\nassistant> {message.content}")
                break

            for call in message.tool_calls:
                args = json.loads(call.function.arguments)
                print(f"\n[tool call] {call.function.name}({args})")
                result = run_tool(call.function.name, args)
                print(f"[tool result] {result}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result),
                    }
                )


if __name__ == "__main__":
    main()
