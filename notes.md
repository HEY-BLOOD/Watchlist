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


