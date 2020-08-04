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



## 第 3 章：模板

页面需要在用户访问时根据程序逻辑动态生成。访问一个地址通常会返回一个包含各类信息的 HTML 页面。包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板，这些变量替换和逻辑计算工作的过程被称为渲染，Flask 通过模板渲染引擎——Jinja2 来完成。

按照默认的设置，Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，所以在程序 `app.py` 的同级目录 (项目根目录) 新建 templates 文件夹：

```powershell
mkdir directory
```

### 模板基本语法

在社交网站上，每个人都有一个主页，借助 Jinja2 就可以写出一个通用的模板，例如：

```jinja2
<h1>{{ username }}的个人主页</h1>
{% if bio %}
	<p>{{ bio }}</p> {# 这里的缩进只是为了可读性，不是必须的 #}
{% else %}
	<p>自我介绍为空。</p>
{% endif %} {# 大部分 Jinja 语句都需要声明关闭 #}
```

Jinja2 的语法和 Python 大致相同，在模板里，需要添加特定的定界符将 Jinja2 语句和变量标记出来。

模板中使用的变量需要在渲染的时候传递进去，下面是三种常用的定界符：

* {{ ... }} 用来标记变量。
* {% ... %} 用来标记语句，比如 if 语句，for 语句等。
* {# ... #} 用来写注释。

### 编写主页模板

在 templates 目录下创建一个 index.html 作为主页模板。主页需显示电影条目列表和个人信息，代码如下：

```jinja2
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>{{ name }}'s Watchlist</title>
</head>

<body>
    <h2>{{ name }}'s Watchlist</h2>
    {# 使用 length 过滤器获取 movies 变量的长度 #}
    <p>{{ movies|length }} Titles</p>
    <ul>
        {% for movie in movies %} {# 迭代 movies 变量 #}
        <li>{{ movie.title }} - {{ movie.year }}</li> {# 等同于 movie['title'] #}
        {% endfor %} {# 使用 endfor 标签结束 for 语句 #}
    </ul>
    <footer>
        <small>&copy; 2018 <a href="https://github.com/HEY-BLOOD/watchlist">BLOOD's Watchlist</a></small>
    </footer>
</body>

</html>
```

为了方便对变量进行处理，Jinja2 提供了一些过滤器，语法形式如下：

```jinja2
{{ 变量|过滤器 }}
```

左侧是变量，右侧是过滤器名。比如 `index.html` 模板中使用 `length` 过滤器来获取 `movies` 的长度，类似 Python 里的 `len()` 函数。

> 提示 访问 http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters 查看所有可用的过滤器。

### 准备虚拟数据

为了模拟页面渲染，需要先创建一些虚拟数据，用来填充页面内容，在 app.py 中定义：

```python
name = 'BLOOD'
movies = [
{'title': 'My Neighbor Totoro', 'year': '1988'},
{'title': 'Dead Poets Society', 'year': '1989'},
{'title': 'A Perfect World', 'year': '1993'},
{'title': 'Leon', 'year': '1994'},
{'title': 'Mahjong', 'year': '1996'},
{'title': 'Swallowtail Butterfly', 'year': '1996'},
{'title': 'King of Comedy', 'year': '1999'},
{'title': 'Devils on the Doorstep', 'year': '1999'},
{'title': 'WALL-E', 'year': '2008'},
{'title': 'The Pork of Music', 'year': '2012'},
]
```

### 渲染主页模板

使用 flask 模块中的 `render_template()` 函数可以把模板渲染出来，必须传入的参数为模板文件名（相对于 templates 根目录的文件路径），这里即 'index.html' 。为了让模板正确渲染，我们还要把模板内部使用的变量通过关键字参数传入这个函数，如下所示：
app.py：返回渲染好的模板作为响应

```python
from flask import Flask, render_template

# ...

@app.route('/')
def index():
	return render_template('index.html', name=name, movies=movies)
```

为了更好的表示这个视图函数的作用，我们把原来的函数名 `hello` 改为 `index` ，意思是“索引”，即主页。

这里传入模板的 `name` 是字符串， `movies` 是列表，但能够在模板里使用的不只这两种 Python 数据结构，你也可以传入元组、字典、函数等。

`render_template()` 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句，返回渲染好的模板内容。

现在访问 http://localhost:5000/ 看到的程序主页如下图所示：


<h2>BLOOD's Watchlist</h2>
<p>10 Titles</p>
<ul>
<li>My Neighbor Totoro - 1988</li> 
<li>Dead Poets Society - 1989</li> 
<li>A Perfect World - 1993</li> 
<li>Leon - 1994</li>  
<li>Mahjong - 1996</li>    
<li>Swallowtail Butterfly - 1996</li> 
<li>King of Comedy - 1999</li>
<li>Devils on the Doorstep - 1999</li> 
<li>WALL-E - 2008</li> 
<li>The Pork of Music - 2012</li> 
</ul>
<footer>
    <small>&copy; 2020 <a href="https://github.com/HEY-BLOOD/watchlist">BLOOD's Watchlist</a></small>
</footer>

### 本章小结

这一章编写了一个简单的主页。结束前，提交代码：

```powershell
$ git add .
$ git commit -m "Add index page"
$ git push
```

### 进阶提示

使用 [Faker](https://github.com/joke2k/faker) 可以实现自动生成虚拟数据，它支持丰富的数据类型，比如时间、人名、地名、随机字符等等……

除了过滤器，Jinja2 还在模板中提供了一些测试器、全局函数可以使用；以及更丰富的控制结构支持。
更多内容则可以访问 [Jinja2 文档](https://jinja.palletsprojects.com/en/2.11.x/templates/) 学习。



## 第 4 章：静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

在 Flask 中，我们需要创建一个 static 文件夹来保存静态文件，它应该和程序模块、templates 文件夹在同一目录层级，所以我们在项目根目录创建它：

```powershell
mkdir static
```

### 生成静态文件 URL

在 HTML 文件里，引入这些静态文件需要给出资源所在的 URL。为了更加灵活，这些文件的 URL 可以通过 Flask 提供的 `url_for()` 函数来生成。

对于静态文件，需要传入的端点值是static ，同时使用 filename 参数来传入相对于 static 文件夹的文件路径。

假如在 static 文件夹的根目录下面放了一个 foo.jpg 文件，下面的调用可以获取它的 URL：

```jinja2
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

花括号部分的调用会返回 `/static/foo.jpg` 。

> 提示 在 Python 脚本里， `url_for()` 函数需要从 flask 包中导入，而在模板中则可以直接使用，因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。

### 添加 Favicon

Favicon（favourite icon） 是显示在标签页和书签栏的网站头像。你需要准备一个ICO、PNG 或 GIF 格式的图片，大小一般为 16×16、32×32、48×48 或 64×64 像素 [ICO图标在线生成](http://www.ico51.cn/)。把这个图片放到 static 目录下，然后像下面这样在 HTML 模板里引入它：

templates/index.html：引入 Favicon

```jinja2
<head>
	...
	<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>
```

保存后刷新页面，即可在浏览器标签页上看到这个图片。

### 添加图片

为了让页面不那么单调，来添加两个图片：一个是显示在页面标题旁边的头像，另一个是显示在页面底部的龙猫动图。我们在 static 目录下面创建一个子文件夹 images，把这两个图片都放到这个文件夹里：

```powershell
$ cd static
$ mkdir images
```

创建子文件夹并不是必须的，这里只是为了更好的组织同类文件。同样的，如果你
有多个 CSS 文件，也可以创建一个 css 文件夹来组织他们。下面我们在页面模板
中添加这两个图片，注意填写正确的文件路径：

templates/index.html：添加图片

```jinja2
<h2>
	<img alt="Avatar" src="{{ url_for('static', filename='images/avatar.png') }}">{{ name }}'s Watchlist
</h2>
...
<img alt="Walking Totoro" src="{{ url_for('static', filename='images/totoro.gif') }}">
<footer>...</footer>
```

### 添加 CSS

虽然添加了图片，但页面还是非常简陋，因为我们还没有添加 CSS 定义。下面在static 目录下创建一个 CSS 文件 style.css，内容如下：
static/style.css：定义页面样式

```css
/* 页面整体 */
body {
    margin: auto;
    max-width: 580px;
    font-size: 14px;
    font-family: Helvetica, Arial, sans-serif;
}

/* 页脚 */
footer {
    color: #888;
    margin-top: 15px;
    text-align: center;
    padding: 10px;
}

/* 头像 */
.avatar {
    width: 40px;
}

/* 电影列表 */
.movie-list {
    list-style-type: none;
    padding: 0;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
}

.movie-list li {
    padding: 12px 24px;
    border-bottom: 1px solid #ddd;
}

.movie-list li:last-child {
    border-bottom: none;
}

.movie-list li:hover {
    background-color: #f8f9fa;
}

/* 龙猫图片 */
.totoro {
    display: block;
    margin: 0 auto;
    height: 100px;
}
```

接着在页面的 <head> 标签内引入这个 CSS 文件：

```jinja2
<head>
	...
	<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
```

最后要为对应的元素设置 class 属性值，以便和对应的 CSS 定义关联起来：
templates/index.html：添加 class 属性

```jinja2
<h2>
	<img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">{{ name }}'s Watchlist
</h2>
...
<ul class="movie-list">
    ...
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}">
```

### 本章小结

主页现在基本成型了，接下来会慢慢完成程序的功能。结束前，提交代码：

```powershell
$ git add .
$ git commit -m "Add static files"
$ git push
```

### 进阶提示

* 如果对 CSS 很头疼，可以借助前端框架来完善页面样式，比如 [Bootstrap](https://getbootstrap.com/)、[Semantic-UI](http://semantic-ui.com/)、[Foundation](https://get.foundation/) 等。它们提供了大量的 CSS 定义和动态效果，使用起来非常简单。
* 扩展 Bootstrap-Flask 可以简化在 Flask 项目里使用 [Bootstrap 4](https://github.com/greyli/bootstrap-flask) 的步骤。

