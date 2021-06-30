# madao33's blog

## 前言

本仓库的代码是基于Django3.2以及clean-blog前端模板构建的博客系统

支持的功能包括：

* markdown形式书写和展示博客
* 主页列表显示
* 最近文章和分类文章显示
* 关于作者

## 虚拟环境配置

### 创建虚拟环境

为了方便之后可以快速地部署在服务器，这里尝试使用虚拟环境搭建一个统一的环境，使用的工具是`anaconda`，虚拟环境的`python`版本为3.6如下：

```shell
conda create -n django_env python=3.6
```

### 切换虚拟环境

一般情况下`anaconda`使用的是`base`环境，为了使用虚拟环境，需要切换到虚拟环境：

```shell
conda activate django_env
```

切换环境成功的标志可以看到左侧有虚拟环境的括号，如下图所示：

![png](imgs\envlist.png)

### 安装`Django3.2`

切换到虚拟环境之后安装`django3.2`，直接在命令行中输入：

```shell
conda install django==3.2
```

> 注意这里是`==`，而之前创建虚拟环境却是`=`

确认安装成功，可以在命令行输入

```shell
python -m django --version
```

可以得到版本号为`3.2`

到这里，前期的环境搭建准备工作就准备就绪了，之后就是开始编写博客

## `blog`编写

### 创建项目

切换到项目文件夹，没有的可以直接创建一个，这里命名为`MADAO33-BLOG`，使用`cd`命令行切换到该路径下，然后创建一个`django project`，直接使用以下命令行：

```shell
django-admin startproject madao33blog
```

 这样就创建了一个名为`madao33blog`的`django`项目

可以看到当前的文件目录组成如下所示：

```shell
madao33blog/
    manage.py
    madao33blog/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

现在可以切换到`manage.py`所在的文件路径下，输入以下命令行运行`django`:

```shell
python manage.py runserver
```

然后可以在[http://127.0.0.1:8000/](http://127.0.0.1:8000/)查看到demo网页的效果

### 创建应用

使用`manage.py`创建一个应用，直接使用命令行：

```shell
python manage.py startapp blog
```

> 项目和应用程序之间有什么区别？应用程序是可以执行某些操作的 Web 应用程序，例如，Weblog 系统、公共记录数据库或小型投票应用程序。项目是特定网站的配置和应用程序的集合。一个项目可以包含多个应用程序。一个应用程序可以在多个项目中。

然后可以在`blog/views`文件中修改视图

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

然后在`blog`目录下创建一个`urls.py`文件，添加如下代码

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

同时还需要在`madao33blog/urls.py`中添加如下代码：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
]
```

这时候重新查看运行效果：

```python
python manage.py runserver
```

### 修改设置

`django`默认使用的是`sqlite`，如果使用其他的数据库需要在`madao33blog/setting.py`中修改，我觉得`sqlite`用着还行，就没有修改

时区和语言的修改，这里修改的参考是：

```python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

将语言改为中文，时区改为上海时间，即北京时间

### 创建模型

定义的模型是用来保存django项目中需要保存的数据，例如博客文章，用户信息等

```python
from django.core.exceptions import ValidationError
from django.db import models

class User(models.Model):
    """
    用户注册模型
    """

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        """
        检查用户账号和密码是否符合规范
        """
        if len(self.name) >= 100:
            raise ValidationError({"User": "Username is too long!"})
        elif len(self.password) >= 100:
            raise ValidationError({"User": "User passwrod is too long"})

class Category(models.Model):
    """
    文章分类模型
    """

    category = models.CharField(max_length=128, unique=True)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

class Article(models.Model):
    title = models.CharField(max_length=128, default='未命名标题')
    content = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    create_date = models.DateField()

    def __str__(self):
        return self.title

    def clean(self):
        """
        检查文章发布是否符合规则
        """
        if len(self.title) == 0:
            raise ValidationError({'blog': "blog's title should not be null!"})
        elif len(self.content == 0):
            raise ValidationError({'blog': "blog's content should not be null!"})
        else:
            pass 

```

### 激活模型

要将应用程序包含在`installed_apps`中，需要将其虚路径添加到配置中，可以看到`blog/apps.py`中有类`BlogConfig`，所以将`blog.apps.BlogConfig`添加到`madao33blog/setting.py`中的`INSTALLED_APPS`中：

```python
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

现在要`Django`知道包含了`blog`应用程序，运行一下命令:

```python
python manage.py makemigrations blog
```

可以获得以下输出:

```shell
Migrations for 'blog':
  blog\migrations\0001_initial.py
    - Create model Category
    - Create model User
    - Create model Article
```

然后再运行以下命令迁移数据库：

```python
python manage.py migrate
```

获得以下输出：

```shell
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying blog.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### 管理员

> Django 是在新闻编辑室环境中编写的，“内容发布者”和“公共”站点之间有非常明确的区别。站点管理员使用该系统添加新闻报道、事件、体育比分等，并将这些内容显示在公共站点上。Django 解决了创建统一界面供站点管理员编辑内容的问题。
>
> 管理员不打算供站点访问者使用。它适用于站点管理员。

首先，我们需要创建一个可以登录管理站点的用户。运行以下命令：

```shell
python manage.py createsuperuser
```

输入您想要的用户名，然后按 Enter。

```shell
Username: admin
```

然后系统会提示您输入所需的电子邮件地址：

```shell
Email address: admin@example.com
```

最后一步是输入您的密码。您将被要求输入密码两次，第二次作为对第一次的确认。

```shell
Password: **********
Password (again): *********
Superuser created successfully.
```

然后启动服务器

```shell
python manage.py runserver
```

然后转入本地域的`admin/`例如[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

为了方便地在管理页面修改`blog`应用中定义的模型，需要修改`blog/admin.py`代码以注册

```python
from django.contrib import admin

from .models import Article, User, Category

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Category)
```

