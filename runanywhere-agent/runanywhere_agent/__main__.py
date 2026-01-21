#!/usr/bin/env python
"""
RunAnywhere Agent - AI coding assistant for RunAnywhere SDK development.

This is the main entry point for the runanywhere-agent CLI.
"""

import sys
import os

from runanywhere_agent import __version__


def print_banner():
    """Print the RunAnywhere Agent banner."""
    banner = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🚀 RunAnywhere Agent v{__version__:<43}║
║                                                                  ║
║   AI coding assistant for on-device AI mobile development       ║
║   Powered by aider - https://aider.chat                         ║
║                                                                  ║
║   SDKs: Swift • Kotlin • React Native • Flutter                 ║
║   Docs: https://github.com/RunanywhereAI/runanywhere-sdks       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_help_flags():
    """Check if user is asking for help or version."""
    if "--version" in sys.argv or "-v" in sys.argv and len(sys.argv) == 2:
        print(f"runanywhere-agent {__version__}")
        sys.exit(0)
    
    if "--help" in sys.argv or "-h" in sys.argv:
        # Let aider handle --help, but show our banner first
        print_banner()
        return


def main():
    """Main entry point for RunAnywhere Agent."""
    
    # Check for help/version flags first
    check_help_flags()
    
    # Show banner
    print_banner()
    
    # Check for logout command
    if "--logout" in sys.argv:
        from runanywhere_agent.auth import logout
        logout()
        sys.exit(0)
    
    # Check for skip-auth flag (for development)
    skip_auth = "--skip-auth" in sys.argv or os.environ.get("RUNANYWHERE_SKIP_AUTH") == "1"
    if "--skip-auth" in sys.argv:
        sys.argv.remove("--skip-auth")
    
    # Step 1: Authenticate user (unless skipped)
    if not skip_auth:
        from runanywhere_agent.auth import authenticate
        email = authenticate()
        print(f"\nWelcome, {email}!\n")
    else:
        print("[DEV MODE] Skipping authentication\n")
    
    # Step 2: Inject API keys
    from runanywhere_agent.config import inject_api_keys, check_api_keys, print_key_status
    
    key_status = inject_api_keys()
    
    if not check_api_keys():
        print("\n" + "=" * 60)
        print("  Error: No API Keys Available")
        print("=" * 60)
        print("\nNo API keys are configured. Please set one of:")
        print("  - ANTHROPIC_API_KEY (for Claude models)")
        print("  - OPENAI_API_KEY (for GPT models)")
        print("\nOr contact founders@runanywhere.ai for embedded key access.")
        sys.exit(1)
    
    # Show key status in verbose mode
    if "--verbose" in sys.argv or "-v" in sys.argv:
        print_key_status()
    
    # Step 3: Patch aider with RunAnywhere SDK prompts
    from runanywhere_agent.prompts import patch_aider_prompts
    from runanywhere_agent.prompts.patch import apply_all_patches
    
    apply_all_patches()
    
    # Step 4: Set default model if not specified
    from runanywhere_agent.config import get_default_model
    
    if "--model" not in sys.argv and "-m" not in " ".join(sys.argv):
        default_model = get_default_model()
        sys.argv.extend(["--model", default_model])
        print(f"Using model: {default_model}")
    
    print("\n" + "-" * 60)
    print("Starting coding session... (type /help for commands)")
    print("-" * 60 + "\n")
    
    # Step 5: Run aider
    try:
        from aider.main import main as aider_main
        return aider_main()
    except KeyboardInterrupt:
        print("\n\nSession ended. Goodbye!")
        return 0
    except Exception as e:
        print(f"\nError: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


def run_with_args(args: list = None):
    """
    Run the agent with specific arguments.
    
    Useful for programmatic usage or testing.
    
    Args:
        args: List of command line arguments. Defaults to sys.argv[1:].
    """
    if args is not None:
        sys.argv = ["runanywhere-agent"] + args
    return main()


if __name__ == "__main__":
    sys.exit(main() or 0)
