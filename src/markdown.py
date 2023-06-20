import requests
import markdown
from dotenv import load_dotenv
import os
import hashlib
import configparser
from .env import CATEGORIES_TOML, DOTENV_PATH, METADATA_TOML, MARKDOWNS

load_dotenv(dotenv_path=DOTENV_PATH)
md_metadata = configparser.ConfigParser()
category_data = configparser.ConfigParser()

APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
BLOG_NAME = os.getenv("BLOG_NAME")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CATEGORIES = category_data.read(CATEGORIES_TOML)

default_params = {
    "access_token": ACCESS_TOKEN,
    "blogName": BLOG_NAME,
    "output": "json",
}


def convert_metadata(meta, path: str, category: str) -> dict:
    metadata = {}

    # title
    if "title" in meta:
        metadata["title"] = meta["title"][0]
    elif "t" in meta:
        metadata["title"] = meta["t"][0]
    elif "제목" in meta:
        metadata["title"] = meta["제목"][0]
    else:
        raise Exception(
            f"""
{path} 파일의 metadata에 title이 존재하지 않습니다. (필수 항목)

다음 내용을 마크다운 최상단에 추가해주세요:
---
title: your_title
---
"""
        )

    for key in meta:
        key = key.lower()
        # visibility
        if key in ("visibility", "vis", "v", "공개여부", "공개"):
            visibility = meta[key][0]
            if visibility in ("public", "3", "공개"):
                metadata["visibility"] = "3"
            elif visibility in ("protected", "1", "보호"):
                metadata["visibility"] = "1"
            elif visibility in ("private", "0", "비공개"):
                metadata["visibility"] = "0"
            else:
                metadata["visibility"] = "0"
        # tag
        if key in ("tag", "tags", "태그"):
            metadata["tag"] = meta[key][0]
        # acceptComment
        if key in ("acceptcomment", "ac", "comment", "댓글"):
            accept_comment: str = meta[key][0]
            if accept_comment in ("yes", "y", "true", "t", "허용", "1"):
                metadata["acceptComment"] = "1"
            elif accept_comment in ("no", "n", "false", "f", "거부", "0"):
                metadata["acceptComment"] = "0"
            else:
                metadata["acceptComment"] = "1"

    # category
    if category != "markdowns":
        metadata["category"] = category_data[category]["id"]
    else:
        metadata["category"] = "0"

    return metadata


def convert_md_to_html_and_metadata(path: str, category: str):
    raw_md = open(path, "r").read()
    sha1 = hashlib.sha1(raw_md.encode()).hexdigest()
    # Convert it to HTML metadata and content
    extension_configs = {
        "markdown_link_attr_modifier": {
            "new_tab": "on",
            "no_referrer": "external_only",
            "auto_title": "on",
        },
    }
    md = markdown.Markdown(
        extensions=[
            "meta",
            "fenced_code",
            "attr_list",
            "mdx_truly_sane_lists",
            "markdown_link_attr_modifier",
        ],
        extension_configs=extension_configs,
    )
    html_content = md.convert(raw_md)
    meta = md.Meta
    metadata = convert_metadata(meta, path, category)
    return html_content, sha1, metadata


def modify_post_in_tistory(post_id: str, metadata: dict, content: str):
    modify_url = "https://www.tistory.com/apis/post/modify"
    modify_params = {
        "postId": post_id,
        "content": content,
    }
    modify_params.update(default_params)
    modify_params.update(metadata)

    modify_response = requests.post(modify_url, data=modify_params).json()
    return modify_response["tistory"]["status"] == "200"


def save_post_to_tistory(metadata: dict, content: str):
    write_url = "https://www.tistory.com/apis/post/write"
    write_params = {
        "content": content,
    }
    write_params.update(default_params)
    write_params.update(metadata)

    write_result = requests.post(write_url, data=write_params).json()
    post_id = write_result["tistory"]["postId"]
    post_url = write_result["tistory"]["url"]
    print(f"티스토리에 새로운 포스트 등록 완료. url = {post_url}")
    return post_id


def save_metadata(md_metadata, md_rel_path: str, post_id: str, sha1: str):
    md_metadata[md_rel_path] = {}
    md_metadata[md_rel_path]["post_id"] = post_id
    md_metadata[md_rel_path]["sha1"] = sha1
    md_metadata.write(open(METADATA_TOML, "w"))


def modify_metadata(md_metadata, md_rel_path: str, sha1: str):
    md_metadata[md_rel_path]["sha1"] = sha1
    md_metadata.write(open(METADATA_TOML, "w"))


# Traverse the directory and save or modify post
def traverse_markdowns():
    uploaded_count = 0
    modified_count = 0
    for subdir, _, files in os.walk(MARKDOWNS):
        for file in files:
            if not file.endswith(".md"):
                continue

            md_rel_path = os.path.join(subdir, file)
            category = subdir.removeprefix(MARKDOWNS + "/")
            html_content, sha1, metadata = convert_md_to_html_and_metadata(
                md_rel_path, category
            )

            md_metadata.read(METADATA_TOML)
            # If saved metadata does not exist, upload the post
            if md_rel_path not in md_metadata:
                post_id = save_post_to_tistory(metadata, html_content)
                save_metadata(md_metadata, md_rel_path, post_id, sha1)
                uploaded_count += 1

            # If sha1 is different from saved sha1, modify the post
            elif sha1 != md_metadata[md_rel_path]["sha1"]:
                post_id = md_metadata[md_rel_path]["post_id"]
                print(
                    f"post_id:{post_id} 변경 감지. \
                        티스토리 서버로 수정 요청 중.."
                )

                modify_post_in_tistory(post_id, metadata, html_content)
                modify_metadata(md_metadata, md_rel_path, sha1)
                modified_count += 1

    print(
        f"""{uploaded_count} 개의 포스트 업로드 완료.
{modified_count} 개의 포스트 수정 완료.
스크립트를 종료합니다."""
    )


if __name__ == "__main__":
    traverse_markdowns()
