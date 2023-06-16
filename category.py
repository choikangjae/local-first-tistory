import requests
from dotenv import load_dotenv
import os
import configparser
from pathlib import Path

category_data = configparser.ConfigParser()
CATEGORY_PATH = ".categories.toml"
MARKDOWN_FILE_PATH = "./markdowns/"

def save_category(category):
    category_name = category['label'].lower()
    id = category['id']
    category_data[category_name] = {}
    category_data[category_name]['id'] = id
    category_data.write(open(CATEGORY_PATH, 'w'))
    return category_name

def category_mkdir(category_name):
    Path(os.path.join(MARKDOWN_FILE_PATH, category_name)).mkdir(parents=True, exist_ok=True)

def load_categories_from_tistory():
    load_dotenv(override=True)
    BLOG_NAME = os.getenv("BLOG_NAME")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    category_params = {
            "access_token": ACCESS_TOKEN,
            "blogName": BLOG_NAME,
            "output": "json",
            }

    print(f"카테고리를 서버에 요청하는 중입니다.. 결과는 {CATEGORY_PATH}에 저장됩니다.")
    category_url = "https://www.tistory.com/apis/category/list"
    category_from_tistory = requests.get(category_url, params=category_params).json()

    category_data.read(CATEGORY_PATH)
    for category in category_from_tistory['tistory']['item']['categories']:
        category_name = save_category(category)
        category_mkdir(category_name)
    print("카테고리 저장 및 디렉토리 생성 완료.")
