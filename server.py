import math
import pandas
import requests
from flask import Flask, render_template
from random import choice


def get_posts_data() -> list:
    """Get data of all posts."""
    response = requests.get(url="https://api.npoint.io/3adfa47d3d9066d9cea3/")
    return response.json()


def get_top_posts(num: int, posts_data: list) -> list:
    """Get data of top posts."""
    df = pandas.DataFrame.from_records(posts_data)
    top_posts_df = df.nlargest(n=num, columns="upvote")
    top_posts_data = [top_posts_df.iloc[row].to_dict() for row in range(num)]
    return top_posts_data


app = Flask(import_name=__name__)


@app.route("/")
def home():
    top_10_posts = get_top_posts(num=10, posts_data=get_posts_data())
    return render_template(template_name_or_list="index.html", top_10_posts=top_10_posts)


@app.route("/our-story")
def our_story():
    return render_template(template_name_or_list="our-story.html")


@app.route("/posts/page-<int:page_no>")
def all_posts(page_no: int):
    top_3_posts = get_top_posts(num=3, posts_data=get_posts_data())
    all_posts_data = get_posts_data()
    num_all_posts = len(all_posts_data)
    total_pages = math.ceil(num_all_posts / 10)
    if 0 < page_no <= total_pages:
        post_index_start = 10 * (page_no - 1)
        post_index_end = 10 * page_no
        if post_index_end > num_all_posts:
            post_index_end = num_all_posts
        else:
            pass
        posts_data = all_posts_data[post_index_start:post_index_end]
        return render_template(template_name_or_list="posts.html", top_3_posts=top_3_posts, posts_data=posts_data, total_pages=total_pages, page_no=page_no)
    elif page_no <= 0:
        all_posts(page_no=1)
    else:
        all_posts(page_no=total_pages)


@app.route("/post/<int:post_id>")
def single_post(post_id: int):
    all_posts_data = get_posts_data()
    post_data = all_posts_data[post_id - 1]
    all_posts_data.pop(post_id - 1)
    recommendations_data = [choice(all_posts_data) for n in range(4)]
    return render_template(template_name_or_list="post.html", recommendations_data=recommendations_data, post_data=post_data)


if __name__ == "__main__":
    app.run()
