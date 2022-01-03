from markdown2 import Markdown
import os
import datetime
from jinja2 import Environment, FileSystemLoader

content_folder = "./posts"

templates = Environment(loader=FileSystemLoader("templates"))
md = Markdown(extras=["fenced-code-blocks","metadata","task_list","tables","target-blank-links"])

files = os.listdir(content_folder)
files = [x for x in files if x.endswith(".md")]

class blog_post:
    def __init__(self,title,link,tags,date,content,description):
        self.title = title
        self.link = link
        self.tags = tags
        self.date = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M")
        self.content = content
        self.description = description

def render_markdown_post(html,metadata=None,template="post.html",posts=[]):
	global templates

	if len(posts) != 0:
		posts = sorted(posts,key=lambda i:i["date"],reverse=True)
	return templates.get_template(template).render(content=html,posts=posts)

posts = []

for file in files:
    fpath = os.path.join(content_folder,file)
    _html = md.convert(open(fpath).read())
    _title = _html[4:_html.find("</h1>")]
    _post = _html.metadata
    _post["link"] = fpath.replace("md","html")
    _post["tags"] = [x.strip() for x in _post["tags"].split(",")]
    post = blog_post(_title,_post["link"],_post["tags"],_post["date"],_html,_post["description"])
    print(post.title)
    print(post.description)
    print(post.link)
    print(post.tags)
    print(post.date)
    posts.append(post)

for post in posts:
    with open(post.link,"w") as f:
        html = templates.get_template("post.html").render(content=post.content)
        f.write(html)

with open("index.html","w") as f:
    posts = sorted(posts,key=lambda i:i.date,reverse=True)
    with open("index.md") as f2:
        _html= md.convert(f2.read())
    html = templates.get_template("index.html").render(content=_html,posts=posts)
    f.write(html)