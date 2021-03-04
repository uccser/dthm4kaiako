import os
import json
from base64 import b64decode

FILEPATH_ENV = 'GOOGLE_APPLICATION_CREDENTIALS_FILEPATH'
CONTENT_ENV =  'GOOGLE_APPLICATION_CREDENTIALS_BASE64'


def get_env(env_key):
    try:
        value = os.environ[env_key]
    except KeyError:
        raise Exception(f"Could not find environment variable {env_key}")
    return value


def main():
    # Get envs
    filepath = get_env(FILEPATH_ENV)
    content_base64 = get_env(CONTENT_ENV)

    # Convert Base64 content to JSON
    content = b64decode(content_base64)
    content_json = json.loads(content)

    # Write JSON file
    with open(filepath, 'w') as f:
        json.dump(content_json, f, ensure_ascii=False)


main()