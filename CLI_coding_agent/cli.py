"""
CLI Coding Agent
----------------
This script implements a simple AI agent that executes CLI commands.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from current directory
load_dotenv()

# ─── Tool Definitions ───────────────────────────────────────────────────────

def runcommand(command: str) -> str:
    """Run a shell command and return its output or status."""
    try:
        # Handle 'cd' specially since os.system or os.popen doesn't change the current process's directory
        if command.strip().startswith("cd "):
            target_dir = command.strip()[3:].strip()
            os.chdir(target_dir)
            return f"Successfully changed directory to {os.getcwd()}"
        else:
            # os.popen executes the command and returns a file object connected to the command's standard output
            output = os.popen(command).read()
            return output if output else "Command executed successfully (no output)."
    except Exception as e:
        return f"Error executing command: {str(e)}"

# ─── Client Setup ────────────────────────────────────────────────────────────

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ─── System Prompt ───────────────────────────────────────────────────────────

System_prompt = """
You are a helpful CLI AI assistant. You can execute shell commands on the user's system to help them.
You must use the exact format requested.
When you need to execute a command, output ONLY a JSON object with this format exactly:
{"command": "your_shell_command_here"}

Do not wrap it in markdown block quotes (```json). Just output the raw JSON string.

When you have the final answer and do not need to execute any more commands, output your response normally as text (not JSON).
"""

# ─── Main Agent Loop ─────────────────────────────────────────────────────────

def main():
    message_history = [
        {"role": "system", "content": System_prompt}
    ]

    user_query = input("🧑‍💻 Enter command or request: ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=message_history
            )
        except Exception as e:
            print(f"❌ API Error: {e}")
            break

        assistant_msg = response.choices[0].message.content.strip()
        message_history.append({"role": "assistant", "content": assistant_msg})

        # Check if the assistant wants to run a command (if it's a JSON string)
        if assistant_msg.startswith("{") and assistant_msg.endswith("}"):
            try:
                cmd_data = json.loads(assistant_msg)
                if "command" in cmd_data:
                    command = cmd_data["command"]
                    print(f"🔧 Executing: {command}")
                    
                    output = runcommand(command)
                    print(f"📡 Output:\n{output}")
                    
                    # Feed the output back to the LLM
                    message_history.append({
                        "role": "user",
                        "content": f"Command output:\n{output}"
                    })
                    continue # Let the LLM process the output and decide what to do next
            except json.JSONDecodeError:
                # If it's not valid JSON despite looking like it, we just print it
                pass 
                
        # If we reach here, it implies it's a normal text response (final answer) or we failed to parse a command
        print(f"\n🤖 Agent: {assistant_msg}")
        
        # Ask for next user input
        print("-" * 40)
        user_query = input("🧑‍💻 Enter next command (or type 'exit'): ")
        if user_query.lower() in ['exit', 'quit']:
            break
        message_history.append({"role": "user", "content": user_query})

if __name__ == "__main__":
    main()
