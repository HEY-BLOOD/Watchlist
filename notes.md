[toc]

## 简介

这是一篇 Flask 的笔记，是我在学习 [Flask 入门教程](http://helloflask.com/tutorial/) 时所写下的，为的是当我需要用到某个知识点却又想不起来时能够在这里快速的找到解决方案。

## 第 1 章：准备工作

### 安装编辑器和浏览器
[Visual Studio Code](https://code.visualstudio.com/) 和 [Microsoft Edge Insider](https://www.microsoftedgeinsider.com/zh-cn)

### 使用命令行

因为是 Windows 系统，所以我使用 PowerShell  任务自动化和配置管理框架。

创建工作目录 `mkdir watchlist`

### 使用 Git
1. 用户信息：

    ```powershell
    git config --global user.name "blood"
    git config --global user.email "blood1740@aliyun.com"
    ```

2. 初始化 Git 仓库：

    ```powershell
    git init
    ```

3. 忽略文件规则：

    项目根目录新建文件 `touch .gitignore`

4. 写入常见的可忽略文件规则：

    ```
    *.pyc
    *~
    __pycache__
    .DS_Store
    ```

### 将程序托管到 GitHub
1. 设置 SSH 密钥：

   ```powershell
   ssh-keygen
   ```

   一路按下 Enter 采用默认值，最后会在用户根目录创建一个 .ssh 文件夹，其中包含两个文件，id_rsa 和 id_rsa.pub，前者是私钥，不能泄露出去，后者是公钥，用于认证身份，就是我们要保存到 GitHub 上的密钥值。再次使用前面提到的命令获得文件内容：

   ```powershell
   $ cat ~/.ssh/id_rsa.pub
   ssh-rsa AAAAB3Nza...省略 N 个字符...3aph book@greyli
   ```

   选中并复制输出的内容，访问 GitHub 的 SSH 设置页面（导航栏头像 - Settings -SSH and GPG keys），点击 New SSH key 按钮，将复制的内容粘贴到 Key 输入框里，再填一个标题，比如“My PC”，最后点击“Add SSH key”按钮保存。


2. 创建远程仓库：

   访问新建仓库页面（导航栏“+” - New repository），在“Repository name”处填写仓库名称，这里填“watchlist”即可，接着选择仓库类型（公开或私有）等选项，最后点击“Create repository”按钮创建仓库。

   因为我们已经提前创建了本地仓库，所以需要指定仓库的远程仓库地址（如果还没有创建，则可以直接将远程仓库克隆到本地）：

   ```powershell
   git remote add origin git@github.com:HEY-BLOOD/watchlist.git # 注意更换地址中的用户名
   ```

   这会为本地仓库关联一个名为“origin”的远程仓库。

### 创建虚拟环境

我的电脑上安装的是 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 因此使用 conda 创建虚拟环境：

```powershell
conda create -n myenv python=3.6 flask
```

激活虚拟环境：

```powershell
conda activate myenv
```

退出虚拟环境：

```powershell
conda deactivate
```

### 本章小结

项目的准备已经完成，使用 `git status` 命令可以查看当前仓库的文件变动状态：

```powershell
(myenv) PS E:\PyCode\watchlist> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

提交进 Git 仓库，并推送到在 GitHub 上创建的远程仓库：

```powershell
git add . # 暂存所有更改
git commit -m "I'm ready!"
git push -u origin master
```

最后一行命令添加了 -u 参数，会将推送的目标仓库和分支设为默认值，后续的推送直接 `git push` 命令即可。



## 第 2 章：Hello, Flask!

### 主页

主页的 URL 一般就是根地址，即 `/` 。

在项目根目录新建 app.py 文件：程序主页

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Welcome to My Watchlist!'
```

在命令行窗口执行 flask run 命令启动程序（按下 Control + C 可以退出）

```powershell
(myenv) PS E:\PyCode\watchlist> flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

打开浏览器，访问 http://localhost:5000 即可访问程序主页，执行 flask run 命令时，Flask 会使用内置的开发服务器来运行程序。这个服务器默认监听本机的 5000 端口，可以在地址栏输入 http://127.0.0.1:5000 访问程序。

> 注意 内置的开发服务器只能用于开发时使用，部署上线时要用性能更好的服务器，这在最后一章学习。

### 解剖时间

下面分解这个 Flask 程序，了解它的基本构成。

首先我们从 flask 包导入 Flask 类，通过实例化这个类，创建一个程序对象 app ：

```python
from flask import Flask
app = Flask(__name__)
```

注册一个处理函数，这个函数是处理某个请求的处理函数，Flask 官方把它叫做视图函数（view funciton），使用 `app.route()` 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：

```python
@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'
```

`app.route()` 装饰器的第一个参数是 URL 规则字符串，其中 `/` 代表根地址，也就是  http://127.0.0.1:5000/ 。

### 程序发现机制

如果把程序 app.py 保存成其他的名字，比如 hello.py，接着执行 flask run 命令会返回一个错误提示。因为 Flask 默认会假设你把程序存储在名为 app.py 或 wsgi.py 的文件中。如果你使用了其他名称，就要设置系统环境变量 FLASK_APP 来告诉 Flask 你要启动哪个程序。

Flask 通过读取这个环境变量值对应的模块寻找要运行的程序实例，你可以把它设置成下面这些值：

* 模块名
* Python 导入路径
* 文件目录路径

**管理环境变量**

启动 Flask 程序时通常要和两个环境变量打交道： `FLASK_APP` 和 `FLASK_ENV` 。

因为程序程序现在名字是 app.py，暂时不需要设置 `FLASK_APP `； `FLASK_ENV` 用来设置程序运行的环境，默认为 production 。在开发时，需要开启调试模式（debug mode）。调试模式可以通过将系统环境变量 `FLASK_ENV` 设为 development 来开启。调试模式开启后，当程序出错，浏览器页面上会显示错误信息；代码出现变动后，程序会自动重载。

**管理系统环境变量的 python-dotenv：**

```powershell
(env) $ pip install python-dotenv
```

当 python-dotenv 安装后，当 python-dotenv 安装后，Flask 会从项目根目录的 .flaskenv 和 .env 文件读取环
境变量并设置。

**创建这两个文件：**

```powershell
New-Item .env
New-Item .flaskenv
```

把文件名 .env 添加到 .gitignore 文件，让 Git 忽略它：

```powershell
*.pyc
*~
__pycache__
.DS_Store
.env
```

**更改 `.flaskenv` 开启调试模式：**

```powershell
"FLASK_ENV=development" >> .\.flaskenv
```

> 其实在集成开发环境中有更好的解决方案，比如 PyCharm 或 VS Code 等。

### 实验时间

1. **修改视图函数返回值**

   首先，你可以自由修改视图函数的返回值，比如：

   ```python
   @app.route('/')
   def hello():
   	return u'欢迎来到我的 Watchlist！'
   ```

   返回值作为响应的主体，默认会被浏览器作为 HTML 格式解析，所以可以添加 HTML 元素标记：

   ```python
   @app.route('/')
   def hello():
       return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
   ```

   保存修改后，只需要在浏览器里刷新页面，你就会看到页面上的内容也会随之变化。

2. **修改 URL 规则**

   **另外，也可以自由修改传入 `app.route()` 装饰器里的 URL 规则字符串，但要注意以斜线 `/` 作为开头。比如：**

   ```python
   @app.route('/home')
   def hello():
   	return 'Welcome to My Watchlist!'
   ```

   保存修改，这时刷新浏览器，则会看到一个 404 错误提示，因为视图函数的 URL 改成了 `/home` ，而我们刷新后访问的地址仍然是旧的 `/` 。把访问地址改成 http://localhost:5000/home，就会看到正确返回值。

   **一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现，比如：**

   ```python
   @app.route('/')
   @app.route('/index')
   @app.route('/home')
   def hello():
       return u'欢迎来到我的 Watchlist！'
   ```

   无论是访问 http://localhost:5000/、http://localhost:5000/home 还是 http://localhost:5000/index 都可以看到返回值。

   **所以把传入 `app.route()` 装饰器的参数称为 URL 规则，因为可以在 URL 里定义变量部分，比如：**

   ```python
   @app.route('/user/<name>')
   def user_page(name):
       return 'User: %s' % name
   ```

   无论是访问 http://localhost:5000/user/12a、http://localhost:5000/user/HEY-BLOOD 还是 `http://localhost:5000/user/哈哈哈` 都会触发该函数，通过这种方式可以在视图函数里获取到这个变量值。

3. **修改视图函数名？**

   视图函数的名字是自由定义的，和 URL 规则无关。

   除此之外，还有一个重要作用：作为代表某个路由的端点 (endpoint)，同时用来生成 URL。为了避免手写，Flask 提供了一个 `url_for` 函数来生成 URL，它接受的第一个参数就是端点值，默认为视图函数名称：

   ```python
   from flask import url_for
   
   @app.route('/test')
   def test_url_for():
       # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
       print(url_for('hello'))  # 输出：/home，离视图函数最近的 装饰器
       # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
       print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
       print(url_for('user_page', name='peter'))  # 输出：/user/peter
       print(url_for('test_url_for'))  # 输出：/test
       # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
       print(url_for('test_url_for', num=2))  # 输出：/test?num=2
       return 'Test page'
   ```

   

### 本章小结

这一章我们为程序编写了主页，同时学习了 Flask 视图函数的基本编写方式。结束前，让我们提交代码：

```powershell
$ git add .
$ git commit -m "Add minimal home page"
$ git push
```

### 进阶提示

如果你使用 Python 2.7，为了使程序正常工作，需要在脚本首行添加编码声明 `# -*- coding: utf-8-*-` ，并在包含中文的字符串前面添加 u 前缀。这在 Python 3 中并不需要。

对于 URL 变量，Flask 还支持在 URL 规则字符串里对变量设置处理器，对变量进行预处理。比如 `/user/<int:number>` 会将 URL 中的 number 部分处理成整型，同时这个变量值接收传入数字。

因为 Flask 的上下文机制，有一些变量和函数（比如 url_for 函数）只能在特定的情况下才能正确执行，比如视图函数内。我们先暂时不用纠结，后面再慢慢了解。

名字以 . 开头的文件默认会被隐藏，执行 ls 命令时会看不到它们，这时你可以使用 `ls *` 命令来列出所有文件。


