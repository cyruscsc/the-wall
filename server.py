import math
from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_ckeditor import CKEditor, CKEditorField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from random import choice

app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = "SecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
ckeditor = CKEditor(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    author = db.Column(db.String(16), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(160), nullable=False)
    body = db.Column(db.String(8000), nullable=False)
    upvote = db.Column(db.Integer, nullable=False)


class WritePostForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired(), Length(min=1, max=80)], render_kw={"placeholder": "Title"}, id="input-title")
    subtitle = StringField(label="Subtitle", validators=[DataRequired(), Length(min=1, max=160)], render_kw={"placeholder": "Subtitle"}, id="input-subtitle")
    img_url = StringField(label="Image URL", validators=[DataRequired(), URL()], render_kw={"placeholder": "Image URL"}, id="input-image-url")
    body = CKEditorField(label="Body", validators=[DataRequired(), Length(min=1, max=8000)], id="input-body")
    submit = SubmitField(label="Post")


@app.route("/")
def home():
    top_10_posts = Post.query.order_by(Post.upvote.desc()).limit(10).all()
    return render_template(template_name_or_list="index.html", top_10_posts=top_10_posts)


@app.route("/our-story")
def our_story():
    return render_template(template_name_or_list="our-story.html")


@app.route("/posts/page-<int:page_no>")
def get_all_posts(page_no: int):
    top_3_posts = Post.query.order_by(Post.upvote.desc()).limit(3).all()
    all_posts = Post.query.order_by(Post.id.desc()).all()
    num_all_posts = len(all_posts)
    total_pages = math.ceil(num_all_posts / 10)
    if 0 < page_no <= total_pages:
        post_index_start = 10 * (page_no - 1)
        post_index_end = 10 * page_no
        if post_index_end > num_all_posts:
            post_index_end = num_all_posts
        else:
            pass
        displayed_posts = all_posts[post_index_start:post_index_end]
        return render_template(template_name_or_list="posts.html", top_3_posts=top_3_posts, displayed_posts=displayed_posts, total_pages=total_pages, page_no=page_no)
    elif page_no <= 0:
        get_all_posts(page_no=1)
    else:
        get_all_posts(page_no=total_pages)


@app.route("/post/<int:post_id>")
def get_post(post_id: int):
    post = Post.query.get(post_id)
    all_posts = Post.query.all()
    recommendations = [choice(all_posts) for n in range(4)]
    return render_template(template_name_or_list="post.html", recommendations=recommendations, post=post)


@app.route("/write", methods=["GET", "POST"])
def write_post():
    form = WritePostForm()
    if form.validate_on_submit():
        new_post = Post(
            date=datetime.now().date().strftime("%b %d, %Y"),
            time=datetime.now().time().strftime("%H:%M"),
            author="testing_bot",
            img_url=form.img_url.data,
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            upvote=0
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts", page_no=1))
    return render_template(template_name_or_list="write.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
