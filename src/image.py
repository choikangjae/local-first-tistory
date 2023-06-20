import requests
import os
from dotenv import load_dotenv
import configparser
import hashlib
from .env import DOTENV_PATH, IMAGES, IMAGES_TOML

load_dotenv(dotenv_path=DOTENV_PATH)
image_info = configparser.ConfigParser()

APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
BLOG_NAME = os.getenv("BLOG_NAME")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def upload_file(path):
    upload_url = "https://www.tistory.com/apis/post/attach"
    upload_file_params = {
        "access_token": ACCESS_TOKEN,
        "blogName": BLOG_NAME,
        "output": "json",
    }
    files = {"uploadedfile": open(path, "rb")}

    res = requests.post(upload_url, data=upload_file_params, files=files).json()
    return res["tistory"]["url"]


def save_image_url(image_hash: str, image_rel_path: str, url: str):
    image_info[image_hash] = {}
    image_info[image_hash]["path"] = image_rel_path
    image_info[image_hash]["url"] = url
    image_info.write(open(IMAGES_TOML, "w"))
    print(
        f"이미지가 티스토리 서버에 저장되었습니다. \
            image = {image_rel_path} url = {url}"
    )


def traverse_images():
    count = 0
    for subdir, _, files in os.walk(IMAGES):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                image_rel_path = os.path.join(subdir, file)
                with open(image_rel_path, "rb") as f:
                    image_hash = hashlib.sha1(f.read()).hexdigest()

                image_info.read(IMAGES_TOML)
                # If saved images does not exist, upload the post
                # and save the metadata
                if image_hash not in image_info:
                    url = upload_file(image_rel_path)
                    save_image_url(image_hash, image_rel_path, url)
                    count += 1
                # If image is saved but the path is changed,
                # modify the path of image.
                elif (
                    image_hash in image_info
                    and image_info[image_hash]["path"] != image_rel_path
                ):
                    image_info[image_hash]["path"] = image_rel_path
                    image_info.write(open(IMAGES_TOML, "w"))

    print(
        f"총 {count} 개의 이미지가 저장되었습니다. \
            url은 '{IMAGES_TOML}'에서 확인하실 수 있습니다"
    )


if __name__ == "__main__":
    traverse_images()
