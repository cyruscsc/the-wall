import requests
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint

connection = sqlite3.connect("../database.db")
cursor = connection.cursor()

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


def generate_title() -> str:
    """Generate random text for a title."""
    params = {
        "type": "meat-and-filler",
        "sentences": 1
    }
    response = requests.get(url=RANDOM_TEXT_ENDPOINT, params=params)
    title = response.json()[0]
    if len(title) > 80:
        title = title[:79]
    else:
        pass
    return title


def generate_subtitle() -> str:
    """Generate random text for a subtitle."""
    params = {
        "type": "meat-and-filler",
        "sentences": 1
    }
    response = requests.get(url=RANDOM_TEXT_ENDPOINT, params=params)
    subtitle = response.json()[0]
    if len(subtitle) > 160:
        subtitle = subtitle[:159]
    else:
        pass
    return subtitle


def generate_body() -> str:
    """Generate random text in five paragraphs."""
    params = {
        "type": "meat-and-filler"
    }
    response = requests.get(url=RANDOM_TEXT_ENDPOINT, params=params)
    body = "".join([f"<p>{response.json()[n]}</p>" for n in range(5)])
    if len(body) > 8000:
        body = body[:7995] + "</p>"
    else:
        pass
    return body


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


posts = []
for post_id in range(1, 52):
    post = {
        "id": post_id,
        "date": generate_date(),
        "time": generate_time(),
        "author": "testing_bot",
        "img_url": f"https://picsum.photos/id/{post_id}/1200/800",
        "title": generate_title(),
        "subtitle": generate_subtitle(),
        "body": generate_body(),
        "upvote": generate_upvote()
    }
    posts.append(post)
    print(f"Post {post_id} generated.")

data = []
for post in posts:
    row = tuple(post.values())
    data.append(row)
cursor.executemany("INSERT INTO post VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
connection.commit()
print("All posts saved to database.")
