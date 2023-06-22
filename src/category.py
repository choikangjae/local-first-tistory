import requests
from dotenv import load_dotenv
import os
import configparser
from pathlib import Path
from .env import MARKDOWNS, CATEGORIES_TOML, DOTENV_PATH

category_data = configparser.ConfigParser()


def save_category(category):
    category_name = category["label"].lower()
    id = category["id"]
    category_data[category_name] = {}
    category_data[category_name]["id"] = id
    category_data.write(open(CATEGORIES_TOML, "w"))
    return category_name


def category_mkdir(category_name):
    Path(os.path.join(MARKDOWNS, category_name)).mkdir(parents=True, exist_ok=True)


def load_categories_from_tistory():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
    BLOG_NAME = os.getenv("BLOG_NAME")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    category_params = {
        "access_token": ACCESS_TOKEN,
        "blogName": BLOG_NAME,
        "output": "json",
    }

    print(
        f"카테고리를 서버에 요청하는 중입니다.. \
            결과는 {CATEGORIES_TOML}에 저장됩니다."
    )
    category_url = "https://www.tistory.com/apis/category/list"
    category_from_tistory = requests.get(category_url, params=category_params).json()[
        "tistory"
    ]["item"]["categories"]

    category_data.read(CATEGORIES_TOML)
    category_data.clear()

    for category in category_from_tistory:
        category_name = save_category(category)
        category_mkdir(category_name)
    print("카테고리 저장 및 디렉토리 생성 완료.")


if __name__ == "__main__":
    load_categories_from_tistory()
