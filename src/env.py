import os
from pathlib import Path

home = str(Path.home())
ROOT = os.path.join(home, ".tistory")
MARKDOWNS = os.path.join(ROOT, "markdowns")
IMAGES = os.path.join(ROOT, "images")
CATEGORIES_TOML = os.path.join(ROOT, ".categories.toml")
IMAGES_TOML = os.path.join(ROOT, ".images.toml")
METADATA_TOML = os.path.join(ROOT, ".metadata.toml")
DOTENV_PATH = os.path.join(ROOT, ".env")


def make_default_dir():
    Path(ROOT).mkdir(parents=True, exist_ok=True)
    Path(MARKDOWNS).mkdir(parents=True, exist_ok=True)
    Path(IMAGES).mkdir(parents=True, exist_ok=True)


# def load_env():
if __name__ == "__main__":
    make_default_dir()
