import click
from auth import auth
from category import load_categories_from_tistory
from main import traverse_markdowns
from image import traverse_images


@click.command(name="init")
def init():
    auth()
    load_categories_from_tistory()


@click.command(name="md")
def md():
    traverse_markdowns()


@click.command(name="category")
def category():
    load_categories_from_tistory()


@click.command(name="img")
def img():
    traverse_images()


@click.command(name="auth")
def run_auth():
    auth()


@click.group()
def cli():
    pass


cli.add_command(run_auth)
cli.add_command(img)
cli.add_command(md)
cli.add_command(category)
cli.add_command(init)

if __name__ == "__main__":
    cli()
