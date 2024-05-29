import requests
from bs4 import BeautifulSoup
from pprint import pprint


def save_file(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)


response = requests.get("https://books.toscrape.com/")
content = response.text
soup = BeautifulSoup(content, "html.parser")
save_file("html_content.txt", soup.prettify())

cat_div = soup.find("div", class_="side_categories").find("ul").find("li").find("ul")

categories = [category.text.strip() for category in cat_div.children if category.name]

save_file("categories.txt", ",\n".join(categories))

articles = soup.find("section").find_all("article", class_="product_pod")
images = []
titles = []
for article in articles:
    img = article.find("img").get("src")
    images.append(img)

    title = article.find("h3").find("a").get("title")
    titles.append(title)

save_file("images.txt", ",\n".join(images))
save_file("titles.txt", ",\n".join(titles))
