#!/usr/bin/env python3
"""
Antigravity PreToolUse hook for RTK (Rust Token Killer).
Intercepts run_command tool calls and rewrites supported commands
through `rtk rewrite` to filter token output automatically.
"""
import sys
import json
import subprocess
import os

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})
        command_line = args.get("CommandLine", "").strip()

        # Only process run_command when a command is present
        if tool_name == "run_command" and command_line:
            # Check if rtk is available
            rtk_bin = os.path.expanduser("~/.local/bin/rtk")
            if not os.path.isfile(rtk_bin):
                rtk_bin = "rtk"

            # Avoid recursively rewriting already prefixed commands
            if not command_line.startswith("rtk "):
                try:
                    res = subprocess.run(
                        [rtk_bin, "rewrite", command_line],
                        capture_output=True,
                        text=True,
                        timeout=2,
                    )
                    rewritten = res.stdout.strip()
                    if rewritten and rewritten != command_line:
                        output = {
                            "decision": "allow",
                            "overwrite": {
                                "CommandLine": rewritten
                            }
                        }
                        print(json.dumps(output))
                        return
                except Exception:
                    pass

    except Exception:
        pass

    # Default fallback: allow original command without modification
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
