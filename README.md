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
- [Quick Start](#quick-start)
- [Markdown](#markdown)
- [Image](#image)
- [Miscellaneous](#miscellaneous)

### Installation

- Python >= 3.9
- To install package:

    ```bash
    pip install tistory-helper
    ```

### Quick Start

You can use `tistory-helper` using `$ tistory [command]`.

To start off, you run:

```bash
tistory init
```

It will handle 3 things:

- [Authorization](#authorization)
- [Create Default Directory](#default-directory)
- [Create Category Directory](#category-directory)

#### Authorization

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

1. All the data you input will be stored at `$HOME/.tistory/.env`.
If anything went wrong, you can modify the data manually.

#### Default Directory

It will be done automatically. You can check the default directory:

```bash
tree -a ~/.tistory 

$HOME/.tistory
├── .categories.toml
├── .env
├── .metadata.toml
├── images
└── markdowns
```

#### Category Directory

It will create directories according to your categories from blog automatically.

```bash
tree -a ~/.tistory/markdowns 

$HOME/.tistory/markdowns
├── category1
├── category2
│   ├── category3
│   └── category4
└── category5
```

#### Help

`$ tistory` or `$ tistory --help`.

### Markdown

#### Markdown Location

You put all your markdown in `$HOME/.tistory/markdowns/{your_category}`.

#### Upload Markdowns

```bash
tistory md
```

It will detect all the modified or create file and upload it.

#### Write Markdown

Put the meta data on very top of the `markdown` file like:

```md
---
title or t or 제목: your_title [Mandatory]
visibility or vis or v or 공개: [Optional]
published: TIMESTAMP (default: current_time) [Optional]
tag or tags or 태그: tag1,tag2,tag3 (default: '') [Optional]
acceptComment or ac or comment or 댓글: [Optional]
---

Your Content starts from here
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
t: This is my first article!
v: public
ac: 허용
tag: my article,first issue
---

And here it is article content!
```

For more information, go to [official API](https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html).

### Image

#### Image Location

Put your images you want to upload in `$HOME/.tistory/images/`.

#### Upload Images

- Make sure images extension end with `.png`, `.jpg`, `.jpeg` or `.gif`.

- Run:

    ```bash
    tistory img
    ```

- Uploaded image url will be stored at `$HOME/.tistory/.images.toml`
and you can use `url` when writing markdown.

- Recommend to upload images first before writing your markdowns
since you need `url` in `![images](url)`.

### Miscellaneous

#### Category

If you updated category from your blog and to upgrade it:

```bash
tistory category
```

#### Reauthorization

If something went wrong while `tistory init`, you can do authorization step independently:

```bash
tistory auth
```

Or you can modify the field at `$HOME/.tistory/.env` manually.
