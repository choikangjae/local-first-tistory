# Local First Tistory

Do not be afraid of shutting down blog server. It will help you organize the articles in `local-first, server-last` rules.

## Table of Contents
- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)

### Features

### Installation

- Python >= 3.6
- To install Python dependencies:

    ```
    pip3 install -r requirements.txt
    ```

### Usage

#### Retrieve Access Token

Briefly, `App ID` and `redirect uri` will be used to get `Authentication code`(or just `code`); `App ID`, `redirect uri` and `Authentication code` will be used to get `Access token`.

To start off, run:

    python3 auth.py

You will see prompts and please follow the instructions.

To get `App ID` and `Secret Key`:

1. Go to `https://www.tistory.com/guide/api/manage/register`

1. Fill out your form. 
    
    Please be aware of `CallBack` column to `{blog_name}.tistory.com`, not `http://{blog_name}.tistory.com`, `https://~` nor `https://www.~`.

    ![retrieve_app_id_and_secret_key](https://github.com/choikangjae/local-first-tistory/assets/99468424/4859388a-6670-4b0b-a2ed-6a4111a03ad1)

1. Now you get `App ID` and `Secret Key`. You can check `CallBack` column and if it doesn't follow the `{blog_name}.tistory.com`, you can modify it here.
    ![result_app_id_and_secret_key](https://github.com/choikangjae/local-first-tistory/assets/99468424/204c4c0e-cccb-455f-940d-f6b3632ba2c2)

1. Enter `App ID` and `Secret key` while following the prompts.

1. All the data you input will be stored at `./.env`. If anything went wrong, you can modify the data manually.

#### Write Markdown

Put the meta data on very top of the `markdown` file like:

```
---
title: your_title [Mandatory]
visibility: 0(private) or 1(protected) or 3(public) (default: 0) [Optional]
category: category_id (default: 0) [Optional]
published: TIMESTAMP (default: current_time) [Optional]
tag: tag1,tag2,tag3 (default: '') [Optional]
acceptComment: 0(to deny) or 1(to accept) (default: '1') [Optional]
---
```

You will notice that only title is mandatory and not the others. So if you want publicly published article:

```
---
title: This is my first article!
visibility: 3
---

And here it is article content!
```

For more information, go to [official API](https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html).

#### Upload Markdown Files

- Put your `.md` files in `./markdowns/`. 

    It can have depth like:
    ```
    markdowns/markdown.md
    markdowns/depth1/markdown1.md
    markdowns/depth1/markdown2.md
    markdowns/depth1/depth2/markdown3.md
    ```
- Run:
    ```
    python3 main.py
    ```
- Modified or created files will be detected using `SHA1` checksum at `./.metadata.toml` and it will send requests to modify for modified files and to create for created files respectively.

#### Upload Images

- Put your `image` binaries in `./images/`. 

    - It can have depth like `./markdowns/`

- Run:
    ```
    python3 image.py
    ```

- Uploaded image url will be stored at `./.images.toml` and you can use `url` when writing markdown.

- Recommend to upload images first before writing your markdowns since you need `url` in `![images](url)`.
