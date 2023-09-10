#!/usr/bin/env python

import blog
import flask
import os

app = flask.Flask(__name__)
article_repository = blog.ArticleRepository(
	os.path.join(app.root_path, app.template_folder),
	flask.render_template_string
)

app.url_map.converters["article"] = article_repository.converter()

@app.route("/article/<article:article>")
def article(article: blog.Article) -> str:
	return flask.render_template("article.html", article=article)

@app.route("/")
def index() -> str:
	return flask.render_template("index.html", articles=article_repository.articles)
