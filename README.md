# django-blog

## 创建虚拟环境

```shell
> python -m venv venv
# Windows
> venv/Scripts/activate
```

## 安装项目依赖

```shell
# (venv)
pip install -r requirement.txt
```

## 项目初始化

```shell
# (venv)
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 运行

```shell
python manage.py runserver
```
打开浏览器[http://127.0.0.1:8000](http://127.0.0.1:8000)查看演示演示

# 服务器部署
