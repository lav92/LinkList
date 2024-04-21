import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


def get_url_data(url: str) -> dict:
    url_data = {

    }

    try:
        page = requests.get(url=url)
        page.encoding = 'utf-8'
    except ConnectionError as e:
        raise ValueError("Такой ссылки не существует")

    soup = BeautifulSoup(page.text, 'html.parser')

    og_title = soup.find(name="meta", property="og:title")
    og_description = soup.find(name="meta", property="og:description")
    og_image = soup.find(name="meta", property="og:image")
    og_type = soup.find(name="meta", property="og:type")

    if og_title is None:
        tag_title = soup.find(name="title")
        if tag_title is not None:
            url_data["title"] = tag_title.text
    else:
        url_data["title"] = og_title.get('content')

    if og_description is None:
        tag_description = soup.find(name="meta", attrs={"name": "description"})
        if tag_description is not None:
            url_data["short_description"] = tag_description.get('content')
    else:
        url_data["short_description"] = og_description.get('content')

    if og_type is not None:
        url_data["type"] = og_type.get('content')

    if og_image is not None:
        url_data["image"] = og_image.get('content')

    return url_data
