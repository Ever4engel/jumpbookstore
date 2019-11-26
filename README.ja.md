# jumpbookstore

[jumpbookstore](http://jumpbookstore.com/)のためのダウンローダーです。

## インストール方法

1. [Poetry](https://poetry.eustace.io/)をインストールします。
```
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```
2. このrepositoryをcloneします。
```
$ git clone https://github.com/h-ishioka/jumpbookstore.git
```
3. 依存関係をインストールします。
```
$ cd jumpbookstore/
$ poetry install --no-dev
```

## 使い方

### `bookshelf` サブコマンド
本棚にある本のコンテンツidを列挙します。

```
$ poetry run jumpbookstore bookshelf --username your-email@example.com --password your-password
```

### `download` サブコマンド
暗号化された .jar ファイルをダウンロードします。

```
$ poetry run jumpbookstore download content-id --username your-email@example.com --password your-password
```

### `extract` サブコマンド
暗号化された .jar ファイルを展開します。

```
$ poetry run jumpbookstore extract content-id.jar
```
