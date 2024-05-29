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



