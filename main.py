import requests
from bs4 import BeautifulSoup
from pprint import pprint


def save_file(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)


def count_books_per_category(caterory: str, index: int, total: dict):
    url = f"https://books.toscrape.com/catalogue/category/books/{caterory}_{index}/index.html"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    number = soup.find("form", class_="form-horizontal").find("strong").text
    number = int(number)
    total[caterory] = number

    print(f"{caterory.replace('-', ' ').capitalize()} contient: {number} livres")


def show_categories_that_has_less_books(categories: dict, limit: int) -> dict:
    print(f"\nListes des catégories de livres contenant moins de {limit+1} livres")
    result = {}
    for category in categories:
        if categories.get(category) <= limit:
            result[category] = categories.get(category)
    return result


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

numbers_of_books = {}
for i, category in enumerate(categories, 2):
    category = category.replace(" ", "-").lower()
    count_books_per_category(category, i, numbers_of_books)


not_enough = show_categories_that_has_less_books(numbers_of_books, 5)
pprint(not_enough)
