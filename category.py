import requests
from dotenv import load_dotenv
import os
import configparser
from pathlib import Path

load_dotenv()
config = configparser.ConfigParser()

BLOG_NAME = os.getenv("BLOG_NAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CATEGORY_PATH = ".categories.toml"

default_data = {
        "access_token": ACCESS_TOKEN,
        "blogName": BLOG_NAME,
        "output": "json",
        }

def load_categories_from_server():
    print(f"카테고리를 서버에 요청하는 중입니다.. 결과는 {CATEGORY_PATH}에 저장됩니다.")
    category_url = "https://www.tistory.com/apis/category/list"
    category_data = default_data
    category_result = requests.get(category_url, params=category_data).json()

    config.read(CATEGORY_PATH)
    for category in category_result['tistory']['item']['categories']:
        name = category['label'].lower()
        id = category['id']
        config[name] = {}
        config[name]['id'] = id
        config.write(open(CATEGORY_PATH, 'w'))
        Path(os.path.join('./markdowns/', name)).mkdir(parents=True, exist_ok=True)
    print(f"카테고리 저장 및 디렉토리 생성 완료.")
