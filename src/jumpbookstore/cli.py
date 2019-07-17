from urllib.parse import urlencode
import click
import os

from . client import Client
from . utils import download_with_progress_bar
from . extract import extract_from_jar


@click.group()
def cli():
    pass


@cli.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def bookshelf(username, password):
    client = Client(username, password)

    shelf_info = client.get_si()
    for cid in shelf_info['shelves'][0]['contents']:
        print(cid)


@cli.command()
@click.argument('cids', nargs=-1)
@click.option("--username", required=True)
@click.option("--password", required=True)
def download(cids, username, password):
    client = Client(username, password)

    for cid in cids:
        expected_jar_filename = cid + '.jar'
        if os.path.isfile(expected_jar_filename):
            print(f'{expected_jar_filename} already exists')
            continue

        data = client.get_contents_license(cid)
        agreement = data['agreement']
        url_prefix = agreement['url_prefix']
        jar_filename = agreement['jar_file_name']
        part_filename = jar_filename + '.part'

        params = data['auth_info']
        url = f'{url_prefix + jar_filename}?{urlencode(params)}'

        print(f'downloading... {jar_filename}')
        download_with_progress_bar(url, part_filename)
        os.rename(part_filename, jar_filename)


@cli.command()
@click.argument('filenames', nargs=-1)
def extract(filenames):
    for filename in filenames:
        print(filename)
        dest_dir = os.path.splitext(filename)[0]
        extract_from_jar(filename, dest_dir)


def main():
    cli()


if __name__ == '__main__':
    main()
