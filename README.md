# Local First Tistory

Do not be afraid of shutting down blog server.
It will help you organize the posts in `local-first, server-last` rules.

## Why Use This?

If you've ever been in trouble when the blog server were shut down,
(especially the one is big-tech and never expecting abnormal!) this script just
for you.

You will hold all the data in the local and the script will manage all the things
to communicate with the server. You can read the data when you
(or the server 😂) are offline or migrate to the other platforms.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

### Installation

- Python >= 3.9
- To install Python dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

### Usage

There are 3 scripts: `main.py`, `image.py` and `init.py`.
You have to run each script  manually when you need it.
(since it sends HTTP requests every time, I don't want to be burden.)

- `main.py`: It detects created or modified files on `./markdowns/`
and sends requests, save the metadata of it. You can `crontab` this,
it won't send any HTTP requests it hasn't been changed
but it might consume some computing power to hash the `markdown` files.

- `image.py`: It traverses on `./images/` and sends requests,
save the `url` of it at `./.images.toml`. It will skip the already saved images.
- `init.py`: It will generate `access token` and
retrieve `category` from your blog and make subdirectories in `./markdowns/`.

#### Retrieve Access Token

Briefly, `App ID` and `redirect uri` will be used to get `Authentication code`
(or just `code`); `App ID`, `redirect uri` and `Authentication code`
will be used to get `Access token`.

To start off, run:

```bash
python3 init.py
```

You will see prompts and please follow the instructions.

To get `App ID` and `Secret Key`:

1. Go to `https://www.tistory.com/guide/api/manage/register`

1. Fill out your form.

    Please be aware of `CallBack` column to `{blog_name}.tistory.com`,
    not `http://{blog_name}.tistory.com`, `https://~` nor `https://www.~`.

    ![retrieve_app_id_and_secret_key](https://github.com/choikangjae/local-first-tistory/assets/99468424/4859388a-6670-4b0b-a2ed-6a4111a03ad1)

1. Now you get `App ID` and `Secret Key`. You can check `CallBack` column
and if it doesn't follow the `{blog_name}.tistory.com`, you can modify it here.
    ![result_app_id_and_secret_key](https://github.com/choikangjae/local-first-tistory/assets/99468424/204c4c0e-cccb-455f-940d-f6b3632ba2c2)

1. Enter `App ID` and `Secret key` while following the prompts.

1. All the data you input will be stored at `./.env`. If anything went wrong,
you can modify the data manually.

#### Category

By running `init.py`, categories will be retrieved from your blog and
subdirectories is generated by your blog categories.
You just put `markdown` files by your `category`.
The script will detect your directory and send a request from it.

e.g.

1. Put `example.md` in `markdowns/category1/category2/example.md`.
1. `category1/category2` will be your category like: `category : category1/category2`.

#### Write Markdown

Put the meta data on very top of the `markdown` file like:

```md
---
title: your_title [Mandatory]
visibility: [Optional]
published: TIMESTAMP (default: current_time) [Optional]
tag: tag1,tag2,tag3 (default: '') [Optional]
acceptComment: [Optional]
---
```

- `visibility` (default: `private`):
  - `public`: `public` or `3` or `공개`
  - `protected`: `protected` or `1` or `보호`
  - `private`: `private` or `0` or `비공개`
- `acceptComment` (default: `yes`):
  - To accept: `yes` or `y` or `true` or `t` or `허용` or `1`
  - To deny: `no` or `n` or `false` or `f` or `거부` or `0`

You will notice that only title is mandatory and not the others. This is the example:

```md
# markdowns/category/example.md

---
title: This is my first article!
visibility: public
acceptComment: 허용
tag: my article,first issue
---

And here it is article content!
```

For more information, go to [official API](https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html).

#### Upload Markdown Files

- Put your `.md` files in `./markdowns/`.

    Subdirectories might be auto-generated from your blog categories.

    ```bash
    markdowns/markdown.md
    markdowns/category1/markdown1.md
    markdowns/category1/markdown2.md
    markdowns/category1/category2/markdown3.md
    ```

- Run:

    ```bash
    python3 main.py
    ```

- Modified or created files will be detected using `SHA1` checksum
at `./.metadata.toml` and it will send requests to modify for modified files
and to create for created files respectively.

#### Upload Images

- Put your `image` binaries in `./images/`.
  - It can have depth like `./markdowns/`

- Make sure images extension end with `.png`, `.jpg`, `.jpeg` or `.gif`.

- Run:

    ```bash
    python3 image.py
    ```

- Uploaded image url will be stored at `./.images.toml`
and you can use `url` when writing markdown.

- Recommend to upload images first before writing your markdowns
since you need `url` in `![images](url)`.

#### TODO

- Change it to `watchdog` to monitor directories?
