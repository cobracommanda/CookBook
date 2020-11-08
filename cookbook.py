from requests_html import HTML, HTMLSession
import csv

url = "https://www.seriouseats.com/recipes/topics/seasonal-and-holiday/christmas?page={}#recipes"

master_links = []
session = HTMLSession()

for page in range(1, 25):
    url_formatted = url.format(page)
    r = session.get(url_formatted)
    cards = r.html.find(".c-cards--3-wide", first=True)
    articles = cards.find("article")
    cookbook = []
    for article in articles:
        link = article.find("a", first=True)
        recipe_link = link.attrs["href"]
        master_links.append(recipe_link)
        recipe_page = link.attrs["href"].split("/")[-1]
        recipe = recipe_page[:-5].replace("-", " ")


csv_file = open("christmas_recipes.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    ["dish", "image", "recipe_teaser", "recipe_info", "ingredients", "directions"]
)

session = HTMLSession()

for lnk in master_links:
    r = session.get(lnk)
    main_content = r.html.find("div.content-main", first=True)
    recipe_container = main_content.find("section.entry-container", first=True)
    recipe_card = recipe_container.find("article.print-hide-images", first=True)

    header = recipe_card.find("header.entry-header", first=True)
    recipe_name_div = header.find("div.entry-header-inner", first=True)
    recipe_name = recipe_name_div.find("h1.title", first=True).text
    recipe_body = recipe_card.find("div.recipe-body", first=True)
    recipe_teaser = recipe_body.find("div.recipe-introduction-body", first=True)
    teaser = recipe_teaser.text
    recipe = recipe_teaser = recipe_body.find("div.recipe-wrapper", first=True)
    recipe_info = recipe.find("ul.recipe-about", first=True).text
    ingredients = recipe.find("div.recipe-ingredients", first=True).text
    recipe_procedures = recipe.find("div.recipe-procedures", first=True)
    procedure = recipe.find("ol.recipe-procedures-list", first=True)
    step_by_step = procedure.find("li.recipe-procedure")
    camera_roll = []
    index_card = []

    for step in step_by_step:

        image_container = step.find("figure.recipe-procedure-image", first=True)

        try:
            image_src = image_container.find("img", first=True)
            image = image_src.attrs["data-src"]
            camera_roll.append(image)
        except AttributeError as AE:
            image = "Video in Iframe"

        index_card.append(step.text)

    images = ""
    for img in camera_roll:
        images += img
        images += "\n"

    directions = ""
    for step in index_card:
        directions += step
        directions += "\n"

    csv_writer.writerow(
        [recipe_name, images, teaser, recipe_info, ingredients, directions]
    )
