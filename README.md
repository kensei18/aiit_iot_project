## IoT特論 グループワーク

シリアル通信のクライアント、及びモバイルからのHTTP通信のサーバーの役割を担うアプリケーション

### 環境構築

Python はインストールされている前提で説明します。
Python が未インストールの方は各々の環境に合わせてインストールしてください。

推奨: version 3.9 以上

環境構築には [poetry](https://python-poetry.org/) を使用します。

```shell
# poetry のインストール

# MacOS / Linux / bashonwindows の場合
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Windows powershell の場合
$ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

```shell
# パッケージがリポジトリのルートディレクトリの .venv にインストールされる
# 仮想環境に入れば、変なところにインストールされなくなる
$ poetry config virtualenvs.in-project true

# 仮想環境の有効化
# 基本的に python コマンドや poetry コマンドは下記コマンドを実行して、仮想環境に入ってから行う
# 実行後、コマンドラインの先頭に (.venv) と表示されるようになる
$ poetry shell

# パッケージインストール
(.venv)$ poetry install

# 仮想環境の非有効化
(.venv)$ deactivate 
```

```shell
# 環境変数の設定
# .env ファイルに記述すると反映される

# .env.sample から .env を作成する
$ cp .env.sample .env

# .env を開いて必要な設定を記述する
# 好きなエディタで編集してOK
$ vi .env
```

### 実行
#### シリアル通信クライアント

```shell
# 事前に環境変数の設定を完了させておく
(.venv)$ python src/serialclient/main.py

# .env で設定した内容でArduinoとシリアル通信をできるようになる
# 得られたデータは src/data/ 配下のCSVファイルに保存される
```

#### HTTP通信サーバー

```shell
(.venv)$ python src/httpserver/main.py

# 0.0.0.0:8000 にアクセスできるようになる
```

ブラウザで `0.0.0.0:8000/docs` を開くと、APIドキュメントを確認できる。

詳細: [FastAPI](https://fastapi.tiangolo.com/)
