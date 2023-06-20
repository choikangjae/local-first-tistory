import click
from .auth import auth
from .category import load_categories_from_tistory
from .markdown import traverse_markdowns
from .image import traverse_images
from .env import make_default_dir, ROOT, MARKDOWNS, IMAGES


@click.command(name="init", help="Initialize default settings including authorization")
def init():
    auth()
    make_default_dir()
    load_categories_from_tistory()


@click.command(name="md", help="Upload created or modified markdown files")
def md():
    traverse_markdowns()


@click.command(name="category", help="Load categories from your blog")
def category():
    load_categories_from_tistory()


@click.command(name="img", help="Upload images")
def img():
    traverse_images()


@click.command(
    name="auth", help="Authorization, normally you wouldn't want to run this"
)
def run_auth():
    auth()


@click.group()
def cli():
    f"""Your data will be stored in {ROOT}

    Put your markdown files in : {MARKDOWNS}
    Put your images in : {IMAGES}

    """
    pass


cli.add_command(run_auth)
cli.add_command(img)
cli.add_command(md)
cli.add_command(category)
cli.add_command(init)

if __name__ == "__main__":
    cli()
