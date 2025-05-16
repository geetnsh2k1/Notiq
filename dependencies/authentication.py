import secrets
from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status

from db.session import get_db
from models import Client
from utils.security import get_superuser_credentials, hash_api_key

security = HTTPBasic()

async def get_client(
    x_api_key: str = Header(..., alias="x-api-key"),
    db: AsyncSession = Depends(get_db),
) -> Client:
    """
    Verifies the provided API key by hashing it and checking it against the
    Client table in the database. The client must be active for the API key to be valid.

    Args:
        x_api_key (str): API key provided in the request header named 'x-api-key'.
        db (AsyncSession): Database session injected via FastAPI dependency.

    Returns:
        Client: The authenticated client object if a valid, active API key is found.

    Raises:
        HTTPException: If the API key is invalid or the client is inactive (HTTP 401).
    """
    # Hash the API key for secure comparison
    hashed_key = hash_api_key(x_api_key)

    result = await db.execute(
select(Client).where(Client.api_key == hashed_key, Client.is_active.is_(True))
    )
    client = result.scalars().first()

    # If no valid client is found, raise an Unauthorized error
    if not client:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")

    # Return the authenticated client instance
    return client

async def get_superuser(
    credentials: HTTPBasicCredentials = Depends(security)
) -> str:
    """
    Verify that the provided HTTP Basic credentials belong to a superuser.
    
    This function retrieves the superuser credentials from the environment (or configuration)
    using `get_superuser_credentials`. It then performs a constant-time comparison of the provided
    username and password with the expected superuser credentials to prevent timing attacks.
    
    Args:
        credentials (HTTPBasicCredentials): The HTTP Basic credentials provided in the request.
        
    Returns:
        str: The username if the credentials are valid.
        
    Raises:
        HTTPException: If either the username or password does not match the expected superuser credentials,
        a 401 Unauthorized error is raised with a WWW-Authenticate header.
    """
    # Retrieve expected superuser credentials from config or environment variables.
    env_user, env_pass = get_superuser_credentials()

    # Perform a constant-time comparison for the username to prevent timing attacks.
    correct_username = secrets.compare_digest(credentials.username, env_user)
    
    # Perform a constant-time comparison for the password to prevent timing attacks.
    correct_password = secrets.compare_digest(credentials.password, env_pass)

    # If either the username or password is incorrect, raise a 401 Unauthorized HTTP exception.
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # Return the username if the credentials are verified successfully.
    return credentials.username