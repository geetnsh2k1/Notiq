import boto3
import json
import logging
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

logger = logging.getLogger(__name__)

def get_secret(secret_name: str, region_name: str = "ap-south-1") -> dict:
    """
    Fetches the secret from AWS Secrets Manager using the boto3 client directly.
    Ensure that AWS credentials and permissions are properly configured.
    """
    try:
        client = boto3.client(
            service_name="secretsmanager",
            region_name=region_name,
        )

        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")

        if not secret_string:
            raise ValueError(f"No SecretString returned for secret: {secret_name}")

        return json.loads(secret_string)

    except NoCredentialsError:
        logger.error("AWS credentials not found.")
        raise

    except PartialCredentialsError:
        logger.error("Incomplete AWS credentials found.")
        raise

    except ClientError as e:
        error_code = e.response['Error']['Code']
        logger.error(f"AWS ClientError occurred: {error_code} - {e.response['Error']['Message']}")
        raise

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode secret JSON: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise
