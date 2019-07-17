# jumpbookstore

downloader for [jumpbookstore](http://jumpbookstore.com/)

## Installation

1. Install [Poetry](https://poetry.eustace.io/)
```
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```
2. Clone this repository
```
$ git clone https://github.com/h-ishioka/jumpbookstore.git
```
3. Install dependencies
```
$ cd jumpbookstore/
$ poetry install --no-dev
```

## Usage

### `bookshelf` subcommand
list content ids of books in your bookshelf

```
$ poetry run jumpbookstore bookshelf --username your-email@example.com --password your-password
```

### `download` subcommand
download encrypted .jar file

```
$ poetry run jumpbookstore download content-id --username your-email@example.com --password your-password
```

### `extract` subcommand
extract encrypted .jar file

```
$ poetry run jumpbookstore extract content-id.jar
```
