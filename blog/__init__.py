import bs4
import dataclasses
import datetime
import glob
import json
import os
import typing
import werkzeug.routing

@dataclasses.dataclass
class Article:
	title: str
	author: str
	date: datetime.date
	subpath: str
	template_path: str
	template_renderer: typing.Callable[[str], str]

	@classmethod
	def from_json(cls, path: str, template_renderer: typing.Callable[[str], str]) -> 'Article':
		with open(path) as file:
			json_ = json.load(file)

			return Article(
				title=json_["title"],
				author=json_["author"],
				date=datetime.date.fromisoformat(json_["date"]),
				subpath=json_["subpath"],
				template_path=os.path.join(os.path.dirname(path), json_["templatePath"]),
				template_renderer=template_renderer
			)

	def preview(self) -> str:
		soup = bs4.BeautifulSoup(self.rendered())

		for tag in soup.select("figcaption"):
			tag.extract()

		return soup.get_text()

	def rendered(self) -> str:
		with open(self.template_path, "r") as file:
			return self.template_renderer(file.read())

class ArticleRepository:
	articles: typing.List[Article]
	articles_by_subpath: typing.Dict[str, Article]

	def __init__(self, article_directory: str, template_renderer: typing.Callable[[str], str]):
		self.articles = []
		self.articles_by_subpath = {}

		for path in glob.glob("**/*.json", root_dir=article_directory, recursive=True):
			article = Article.from_json(os.path.join(article_directory, path), template_renderer)

			self.articles.append(article)
			self.articles_by_subpath[article.subpath] = article

	def converter(self) -> type[werkzeug.routing.BaseConverter]:
		repository = self

		class ArticleConverter(werkzeug.routing.BaseConverter):
			def to_python(self, subpath: str) -> typing.Optional[Article]:
				return repository.articles_by_subpath.get(subpath)

			def to_url(self, article: Article) -> str:
				return article.subpath

		return ArticleConverter
