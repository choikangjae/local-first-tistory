#!/bin/bash

program="tistory.py"
pyinstaller --onefile $program --hidden-import mdx_truly_sane_lists --hidden-import markdown_link_attr_modifier

