#!/bin/bash

source .venv/bin/activate
echo "venv is activated"
rm -rf "./dist"
echo "dist is erased"
bump
python setup.py sdist bdist_wheel
echo "setup is done"
twine upload dist/*
echo "package uploaded"
