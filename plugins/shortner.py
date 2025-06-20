import requests
import random
import string
from config import SHORTNER_API, SHORTNER_URL


def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars

def get_short(url):
    rget = requests.get(f"https://{SHORTNER_URL}/api?api={SHORTNER_API}&url={url}&alias={generate_random_alphanumeric()}")
    rjson = rget.json()
    if rjson["status"] == "success" or rget.status_code == 200:
        return rjson["shortenedUrl"]
    else:
        return url
