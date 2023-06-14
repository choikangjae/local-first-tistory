import requests
import os
from dotenv import load_dotenv
import configparser

load_dotenv()
config = configparser.ConfigParser()

APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
BLOG_NAME = os.getenv("BLOG_NAME")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IMAGE_METADATA_PATH = ".images.toml"

def upload_file(path):
    upload_url = "https://www.tistory.com/apis/post/attach"
    upload_data = {
            "access_token": ACCESS_TOKEN,
            "blogName": BLOG_NAME,
            "output": "json",
            }
    files = {'uploadedfile': open(path, 'rb')}

    res = requests.post(upload_url, data=upload_data, files=files).json()
    return res['tistory']['url']

def traverse_images():
    count = 0
    for subdir, _, files in os.walk("images"):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.gif'):
                path = os.path.join(subdir, file)

                config.read(IMAGE_METADATA_PATH)
                # If saved images does not exist, upload the post and save the metadata
                if path not in config:
                    url = upload_file(path)
                    config[path] = {}
                    config[path]['url'] = url
                    config.write(open(IMAGE_METADATA_PATH, 'w'))
                    print(f"이미지가 저장되었습니다. image = {path} url = {url}")
                    count += 1

    print(f"총 {count} 개의 이미지가 저장되었습니다. url은 '{IMAGE_METADATA_PATH}'에서 확인하실 수 있습니다")

traverse_images()
