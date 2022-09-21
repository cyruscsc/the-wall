import base64
import requests
import urllib.request
from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint

RANDOM_TEXT_ENDPOINT = "https://baconipsum.com/api/"
POST_DATE_START = "2022-06-01"
post_date = date.fromisoformat(POST_DATE_START)


def generate_date() -> str:
    """Generate a random date which is later than the start date and the previous dates generated."""
    global post_date
    post_date += relativedelta(days=randint(1, 5))
    return date.strftime(post_date, "%b %d, %Y")


def generate_time() -> str:
    """Generate a random time."""
    hh = randint(0, 23)
    mm = randint(0, 59)
    return f"{hh:02d}:{mm:02d}"


def get_image(image_id: int):
    """Get a random image and save it on the device."""
    urllib.request.urlretrieve(url="https://picsum.photos/1200/800/", filename=f"posts_images/image-{image_id}.jpg")


def encode_image(image_id: int) -> str:
    """Encode the image to a base64 string."""
    with open(file=f"posts_images/image-{image_id}.jpg", mode="rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read())).strip("b'")
    return encoded_string


def generate_title() -> str:
    """Generate random text for a title or a subtitle."""
    params = {
        "type": "meat-and-filler",
        "sentences": 1
    }
    response = requests.get(url=RANDOM_TEXT_ENDPOINT, params=params)
    return response.json()[0]


def generate_paras() -> list:
    """Generate random text in five paragraphs."""
    params = {
        "type": "meat-and-filler"
    }
    response = requests.get(url=RANDOM_TEXT_ENDPOINT, params=params)
    return response.json()


def generate_upvote() -> int:
    """Generate random number of upvote with different probabilities."""
    chance = randint(1, 10)
    match chance:
        case 1:
            return randint(1001, 2000)
        case 2:
            return randint(501, 1000)
        case 3:
            return randint(501, 1000)
        case 4:
            return randint(501, 1000)
        case _:
            return randint(1, 500)


posts_data = []
for post_id in range(1, 34):
    get_image(image_id=post_id)
    post_data = {
        "id": post_id,
        "date": generate_date(),
        "time": generate_time(),
        "image": encode_image(image_id=post_id),
        "title": generate_title(),
        "subtitle": generate_title(),
        "content": generate_paras(),
        "upvote": generate_upvote()
    }
    posts_data.append(post_data)
    print(f"Post {post_id} generated.")

with open(file="posts_data.txt", mode="w") as data_file:
    data_file.write(str(posts_data))
print("All posts data saved.")
