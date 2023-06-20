import requests
import urllib.parse
from dotenv import load_dotenv, set_key
import os
from .env import DOTENV_PATH

load_dotenv(dotenv_path=DOTENV_PATH)

APP_ID = os.getenv("APP_ID")
BLOG_NAME = os.getenv("BLOG_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


# Generate authorize url
def generate_auth_url():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
    APP_ID = os.getenv("APP_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")

    auth_url = "https://www.tistory.com/oauth/authorize"
    auth_data = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
    }
    return f"{auth_url}?{urllib.parse.urlencode(auth_data)}"


# Generate access token
def retrieve_access_token():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
    APP_ID = os.getenv("APP_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")

    access_token_url = "https://www.tistory.com/oauth/access_token"
    access_token_data = {
        "client_id": APP_ID,
        "client_secret": SECRET_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": AUTHORIZATION_CODE,
        "grant_type": "authorization_code",
    }
    access_token_response = requests.get(access_token_url, params=access_token_data)

    access_token = access_token_response.text.split("=")[1]
    return access_token


def auth():
    print(f"모든 정보는 {DOTENV_PATH}에 저장됩니다.")
    if ACCESS_TOKEN is not None:
        print(f"이미 access token이 발급되었습니다. access token = {ACCESS_TOKEN}")
        print(
            f"다시 발급받고자 하는 경우 \
                {DOTENV_PATH}의 데이터를 지우고 다시 시도해주세요"
        )
        return

    if BLOG_NAME is None:
        print(
            "블로그 이름. 블로그 이름은 \
                https://{{{blog_name}}}.tistory.com에서 확인할 수 있습니다."
        )
        blog_name = input("블로그 이름을 입력해주세요: ")
        set_key(key_to_set="BLOG_NAME", value_to_set=blog_name, dotenv_path=DOTENV_PATH)
        set_key(
            key_to_set="REDIRECT_URI",
            value_to_set=f"{blog_name}.tistory.com",
            dotenv_path=DOTENV_PATH,
        )
        print("블로그 이름 저장 완료")

    if APP_ID is None:
        print(
            "https://www.tistory.com/guide/api/manage/register \
                에서 App ID와 Secret Key를 발급받아주세요."
        )
        app_id = input("App ID를 입력해주세요: ")
        set_key(key_to_set="APP_ID", value_to_set=app_id, dotenv_path=DOTENV_PATH)
        print("App ID 저장 완료")

    if SECRET_KEY is None:
        secret_key = input("Secret Key를 입력해주세요: ")
        set_key(
            key_to_set="SECRET_KEY", value_to_set=secret_key, dotenv_path=DOTENV_PATH
        )
        print("Secret Key 저장 완료")

    if AUTHORIZATION_CODE is None:
        print("다음 url로 접속한 후 code를 발급받아주세요")
        print(generate_auth_url())

        code = input(
            """code를 입력해주세요. \
                code는 다음과 같은 형태이며 \
                리다이렉트 된 주소를 통해 확인할 수 있습니다.
    https://www.tistory.com/oauth/your_blog_name.tistory.com?code={{{code}}}&state=
: """
        )
        set_key(
            key_to_set="AUTHORIZATION_CODE", value_to_set=code, dotenv_path=DOTENV_PATH
        )

        print("code 저장 완료")

    if ACCESS_TOKEN is None:
        print("access token 발급 요청 중..")
        access_token = retrieve_access_token()
        set_key(
            key_to_set="ACCESS_TOKEN",
            value_to_set=access_token,
            dotenv_path=DOTENV_PATH,
        )
        print(f"access token 발급 및 저장 완료. access token = {access_token}")
        print("이제 티스토리 api를 이용하실 수 있습니다")


if __name__ == "__main__":
    auth()
