import requests
import markdown
from dotenv import load_dotenv
import os
import hashlib
import configparser

load_dotenv()
config = configparser.ConfigParser()

APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
BLOG_NAME = os.getenv("BLOG_NAME")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MARKDOWN_METADATA_PATH = ".metadata.toml"
CATEGORIES = config.read(".categories.toml")

default_data = {
        "access_token": ACCESS_TOKEN,
        "blogName": BLOG_NAME,
        "output": "json",
        }

def load_raw_markdown(path: str):
    raw_md = open(path, "r").read()
    sha1 = hashlib.sha1(raw_md.encode()).hexdigest()
# Convert it to HTML metadata and content
    md = markdown.Markdown(extensions=['meta'])
    html_content = md.convert(raw_md)
# pyright: reportGeneralTypeIssues=false
    meta = md.Meta

# Parsing metadata
    metadata = {}
    if 'title' in meta:
        metadata['title'] = meta['title'][0]
    else:
        raise Exception(f"""
{path} 파일의 metadata에 title이 존재하지 않습니다. (필수 항목)

다음 내용을 마크다운 최상단에 추가해주세요:
---
title: your_title
---
""")
    if "visibility" in meta:
        visibility = meta['visibility'][0].lower()
        if visibility == "public" or visibility == "3" or visibility == "공개":
            metadata["visibility"] = "3"
        elif visibility == "protected" or visibility == "1" or visibility == "보호":
            metadata["visibility"] = "1"
        elif visibility == "private" or visibility == "0" or visibility == "비공개":
            metadata["visibility"] = "0"
        else:
            metadata["visibility"] = "0"
    else:
        metadata["visibility"] = "0"

    if "category" in meta:
        category = meta['category'][0].lower()
        metadata["category"] = config[category]['id']
    else:
        metadata["category"] = "0"

    if "tag" in meta:
        metadata["tag"] = meta["tag"][0]
    else:
        metadata["tag"] = ""

    if "acceptcomment" in meta:
        accept_comment: str = meta['acceptcomment'][0].lower()
        print(accept_comment)
        if accept_comment == "yes" or accept_comment == "y" or accept_comment == "true" or accept_comment == "t" or accept_comment == '허용' or accept_comment == "1":
            metadata["acceptComment"] = "1"
        elif accept_comment == "no" or accept_comment == "n" or accept_comment == "false" or accept_comment == "f" or accept_comment == '거부' or accept_comment == "0":
            metadata["acceptComment"] = "0"
        else:
            metadata["acceptComment"] = "1"
    else:
        metadata["acceptComment"] = "1"
    
    return html_content, sha1, metadata

def modify_post(post_id: str, metadata: dict, content: str):
    modify_url = "https://www.tistory.com/apis/post/modify"
    modify_data = {
        "postId": post_id,
        "content": content,
            }
    modify_data.update(default_data)
    modify_data.update(metadata)

    modify_response = requests.post(modify_url, data=modify_data).json()
    return modify_response['tistory']['status'] == '200'

def save_post(metadata: dict, content: str):
    post_write_url = "https://www.tistory.com/apis/post/write"
    post_write_data = {
            "content": content,
            }
    post_write_data.update(default_data)
    post_write_data.update(metadata)

    res = requests.post(post_write_url, data=post_write_data).json()
    post_id = res['tistory']['postId']
    print(f'새로운 포스트가 등록되었습니다. post_id = {post_id}')
    return post_id

# Traverse the directory and check the md5 and modify the post
def traverse_markdowns():
    upload_count = 0
    modified_count = 0
    for subdir, _, files in os.walk("markdowns"):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(subdir, file)
                # Load raw markdown
                html_content, sha1, metadata = load_raw_markdown(path)

                config.read(MARKDOWN_METADATA_PATH)
                # If saved metadata does not exist, upload the post and save the metadata
                if path not in config:
                    post_id = save_post(metadata, html_content)
                    config[path] = {}
                    config[path]['post_id'] = post_id
                    config[path]['sha1'] = sha1
                    config.write(open(MARKDOWN_METADATA_PATH, 'w'))
                    upload_count += 1
                # If sha1 is different from saved sha1, modify the post
                elif sha1 != config[path]['sha1']:
                    print(f"post_id:{config[path]['post_id']} 변경 감지. 수정 요청 중..")
                    modify_post(config[path]['post_id'], metadata, html_content)
                    config[path]['sha1'] = sha1
                    config.write(open(MARKDOWN_METADATA_PATH, 'w'))
                    modified_count += 1
    print(f"""{upload_count} 개의 포스트 업로드 완료.
{modified_count} 개의 포스트 수정 완료.
스크립트를 종료합니다.""")

traverse_markdowns()
