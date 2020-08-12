# Watchlist

Exercise application for flask tutorial "[Flask 入门教程](http://helloflask.com/tutorial)".

Demo: [http://bl00d.pythonanywhere.com]( http://bl00d.pythonanywhere.com/ )

## Installation

clone:

```bash
$ git clone https://github.com/greyli/watchlist.git
$ cd watchlist
```

create & active virtual enviroment then install dependencies:

```bash
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

generate fake data then run:

```bash
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```