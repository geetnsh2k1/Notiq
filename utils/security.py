import os
import secrets
import hashlib

from config.client import ConfigClient

def hash_api_key(api_key: str) -> str:
    """
    Hash the API key using SHA-256.
    This is used for comparing the stored hashed key with the provided key.
    """
    # Ensure the API key is in bytes before hashing
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

def generate_api_key(
        client_name: str
) -> tuple[str, str]:
    """
    Generate a high-entropy API key for a client.
    The API key is a combination of the environment, client ID, and a random token.
    The key is hashed using SHA-256 for security.
    """
    # Generate a random token
    token = secrets.token_hex(32)  # 64-character high-entropy token

    # Combine the environment, client name, and token
    raw_key = f"{os.getenv("APP_ENV", "local").lower()}-{client_name}-{token}"
    
    # Hash using SHA-256 for storage
    hashed_key = hash_api_key(raw_key)
    
    # Return both the raw and hashed keys
    return raw_key, hashed_key

# Function to get credentials from env (can be made async if needed)
def get_superuser_credentials() -> tuple[str, str]:
    """
    Retrieve superuser credentials from environment variables.
    This is used for basic authentication in the admin interface.
    """
    return (
        ConfigClient.get_property(key="SUPERUSER_USERNAME", section="CREDENTIALS"),
        ConfigClient.get_property(key="SUPERUSER_PASSWORD", section="CREDENTIALS"),
    )