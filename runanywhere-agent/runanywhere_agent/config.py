"""
Configuration and API key management for RunAnywhere Agent.

This module handles the injection of embedded API keys for internal distribution.

SECURITY WARNING:
These keys CAN be extracted from the distributed package.
Only distribute to trusted internal team members.
"""

import base64
import os
from typing import Optional

# ============================================================================
# API KEY CONFIGURATION
# ============================================================================
# Keys are base64 encoded to prevent casual viewing (NOT cryptographically secure)
# To encode your keys, use:
#   import base64
#   base64.b64encode(b"sk-your-actual-key").decode()
#
# Replace the placeholder values below with your actual base64-encoded keys
# ============================================================================

_EMBEDDED_KEYS = {
    # Base64 encoded Anthropic API key
    # Encode with: base64.b64encode(b"sk-ant-api03-...").decode()
    "anthropic": "REPLACE_WITH_BASE64_ENCODED_ANTHROPIC_KEY",
    
    # Base64 encoded OpenAI API key
    # Encode with: base64.b64encode(b"sk-...").decode()
    "openai": "REPLACE_WITH_BASE64_ENCODED_OPENAI_KEY",
}

# Default model to use
DEFAULT_MODEL = "sonnet"  # Uses Claude Sonnet by default


def _decode_key(encoded_key: str) -> Optional[str]:
    """
    Decode a base64-encoded API key.
    
    Args:
        encoded_key: Base64-encoded key string.
        
    Returns:
        Decoded key string, or None if decoding fails.
    """
    if not encoded_key or encoded_key.startswith("REPLACE_WITH"):
        return None
    
    try:
        return base64.b64decode(encoded_key).decode("utf-8")
    except Exception:
        return None


def get_anthropic_key() -> Optional[str]:
    """Get the Anthropic API key from environment or embedded config."""
    # Check environment first (allows override)
    env_key = os.environ.get("ANTHROPIC_API_KEY")
    if env_key:
        return env_key
    
    # Fall back to embedded key
    return _decode_key(_EMBEDDED_KEYS.get("anthropic", ""))


def get_openai_key() -> Optional[str]:
    """Get the OpenAI API key from environment or embedded config."""
    # Check environment first (allows override)
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    
    # Fall back to embedded key
    return _decode_key(_EMBEDDED_KEYS.get("openai", ""))


def inject_api_keys() -> dict:
    """
    Inject API keys into environment variables if not already set.
    
    This function injects the embedded API keys into the environment
    so that aider and litellm can use them.
    
    Returns:
        Dictionary with status of key injection.
    """
    status = {
        "anthropic_injected": False,
        "openai_injected": False,
        "anthropic_available": False,
        "openai_available": False,
    }
    
    # Inject Anthropic key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        anthropic_key = _decode_key(_EMBEDDED_KEYS.get("anthropic", ""))
        if anthropic_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
            status["anthropic_injected"] = True
            status["anthropic_available"] = True
    else:
        status["anthropic_available"] = True
    
    # Inject OpenAI key
    if not os.environ.get("OPENAI_API_KEY"):
        openai_key = _decode_key(_EMBEDDED_KEYS.get("openai", ""))
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            status["openai_injected"] = True
            status["openai_available"] = True
    else:
        status["openai_available"] = True
    
    return status


def check_api_keys() -> bool:
    """
    Check if required API keys are available.
    
    Returns:
        True if at least one API key is available, False otherwise.
    """
    anthropic_key = get_anthropic_key()
    openai_key = get_openai_key()
    
    return bool(anthropic_key or openai_key)


def get_default_model() -> str:
    """
    Get the default model to use based on available API keys.
    
    Returns:
        Model name string.
    """
    # Check if user specified a model via environment
    env_model = os.environ.get("RUNANYWHERE_DEFAULT_MODEL")
    if env_model:
        return env_model
    
    # Prefer Anthropic Claude if available
    if get_anthropic_key():
        return DEFAULT_MODEL
    
    # Fall back to OpenAI
    if get_openai_key():
        return "gpt-4o"
    
    # Default (will fail if no keys)
    return DEFAULT_MODEL


def print_key_status() -> None:
    """Print the status of available API keys."""
    anthropic_available = bool(get_anthropic_key())
    openai_available = bool(get_openai_key())
    
    print("\nAPI Key Status:")
    print(f"  Anthropic (Claude): {'✓ Available' if anthropic_available else '✗ Not configured'}")
    print(f"  OpenAI (GPT):       {'✓ Available' if openai_available else '✗ Not configured'}")
    print()


# ============================================================================
# HELPER FUNCTION FOR KEY ENCODING
# ============================================================================

def encode_key_for_config(api_key: str) -> str:
    """
    Helper function to encode an API key for embedding in config.
    
    Usage:
        python -c "from runanywhere_agent.config import encode_key_for_config; print(encode_key_for_config('sk-your-key'))"
    
    Args:
        api_key: The raw API key to encode.
        
    Returns:
        Base64-encoded string to put in _EMBEDDED_KEYS.
    """
    return base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
