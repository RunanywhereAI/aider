"""
Supabase email verification for RunAnywhere Agent.

This module handles authentication by verifying if a user's email
is registered in the Supabase authorized_users table.
"""

import os
import sys
from pathlib import Path

import requests

# Supabase configuration
# Replace with your actual Supabase project URL and anon key
SUPABASE_URL = os.environ.get(
    "RUNANYWHERE_SUPABASE_URL",
    "https://your-project.supabase.co"
)
SUPABASE_ANON_KEY = os.environ.get(
    "RUNANYWHERE_SUPABASE_KEY",
    "your-anon-key-here"
)

# Local cache for authenticated email
AUTH_CACHE_FILE = Path.home() / ".runanywhere" / "auth_cache"


def get_cached_email() -> str | None:
    """Get previously authenticated email from cache."""
    try:
        if AUTH_CACHE_FILE.exists():
            return AUTH_CACHE_FILE.read_text().strip()
    except (OSError, IOError):
        pass
    return None


def save_email_to_cache(email: str) -> None:
    """Save authenticated email to cache for future sessions."""
    try:
        AUTH_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        AUTH_CACHE_FILE.write_text(email)
    except (OSError, IOError) as e:
        print(f"Warning: Could not save auth cache: {e}")


def clear_auth_cache() -> None:
    """Clear the authentication cache."""
    try:
        if AUTH_CACHE_FILE.exists():
            AUTH_CACHE_FILE.unlink()
    except (OSError, IOError):
        pass


def verify_email(email: str) -> bool:
    """
    Check if email exists in Supabase authorized_users table.
    
    Args:
        email: The email address to verify.
        
    Returns:
        True if the email is authorized, False otherwise.
    """
    if not email or not email.strip():
        return False
    
    email = email.strip().lower()
    
    # Skip verification in development mode
    if os.environ.get("RUNANYWHERE_DEV_MODE") == "1":
        print("[DEV MODE] Skipping email verification")
        return True
    
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/authorized_users",
            params={"email": f"eq.{email}"},
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        
        if response.status_code == 200:
            users = response.json()
            return len(users) > 0
        else:
            print(f"Warning: Auth check failed with status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("Warning: Authentication server timeout. Please try again.")
        return False
    except requests.exceptions.ConnectionError:
        print("Warning: Could not connect to authentication server.")
        print("Please check your internet connection.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Warning: Authentication error: {e}")
        return False


def prompt_for_email() -> str:
    """
    Prompt the user for their email address.
    
    First checks for cached email, then prompts if needed.
    
    Returns:
        The email address entered by the user.
    """
    # Check for cached email first
    cached_email = get_cached_email()
    if cached_email:
        print(f"Using cached email: {cached_email}")
        use_cached = input("Press Enter to continue, or type 'new' for a different email: ").strip()
        if use_cached.lower() != "new":
            return cached_email
    
    # Check for environment variable
    env_email = os.environ.get("RUNANYWHERE_EMAIL")
    if env_email:
        print(f"Using email from environment: {env_email}")
        return env_email.strip()
    
    # Prompt for email
    print("\n" + "=" * 60)
    print("  RunAnywhere Agent - Authentication Required")
    print("=" * 60)
    print("\nPlease enter your authorized email address.")
    print("Contact founders@runanywhere.ai if you need access.\n")
    
    while True:
        email = input("Email: ").strip()
        
        if not email:
            print("Email cannot be empty. Please try again.")
            continue
            
        if "@" not in email or "." not in email:
            print("Please enter a valid email address.")
            continue
            
        return email


def authenticate() -> str:
    """
    Main authentication flow.
    
    Returns:
        The authenticated email address.
        
    Raises:
        SystemExit: If authentication fails.
    """
    email = prompt_for_email()
    
    print("\nVerifying email...")
    
    if verify_email(email):
        print(f"✓ Email verified: {email}")
        save_email_to_cache(email)
        return email
    else:
        print("\n" + "=" * 60)
        print("  Access Denied")
        print("=" * 60)
        print(f"\nThe email '{email}' is not authorized to use RunAnywhere Agent.")
        print("\nTo get access:")
        print("  1. Visit https://www.runanywhere.ai")
        print("  2. Sign up for an account")
        print("  3. Contact founders@runanywhere.ai for agent access")
        print()
        
        # Clear cache if auth fails
        clear_auth_cache()
        
        sys.exit(1)


def logout() -> None:
    """Clear authentication and logout."""
    clear_auth_cache()
    print("Logged out successfully. You will need to re-authenticate next time.")
