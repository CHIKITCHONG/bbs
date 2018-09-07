# bbs论坛<br>
#### 简介
借鉴CNode风格设计的论坛,感谢CNode！<br>
前端使用了jinja、pure、bootstarp、jQuery进行开发，后端使用了flask,flask-sqlalchemy,服务器部署上使用了gunicorn+supervisor+nginx


![demo](https://github.com/CHIKITCHONG/bbs/blob/master/demo.gif)
<br>

## 展示
[论坛](193.112.171.150)<br>

## 功能介绍
#### 1. 用户登陆、注册、修改密码、修改签名
#### 2. 上传头像功能
#### 3. 导航栏、页眉、页脚（模板继承）
#### 4. 文章发表、评论功能
#### 5. markdown语法功能
#### 6. 站内信、邮件功能、@at功能
#### 7. 能防御基本的csrf攻击,跨站脚本攻击
#### 8. 权限验证功能（发表话题以及评论或删除文章需要匹配的权限）
<br>

## 如何在您的电脑部署？
#### 1.在项目目录下创建`database_secret.conf`,内容填入（举例） ：<br>
```
# database_secret.conf
# 在此设置您的数据库密码

mysql-server mysql-server/root_password password 1234
mysql-server mysql-server/root_password_again password 1234
```


#### 2.再在项目目录下创建`secret.py`,内容填入（举例） ：<br>
```
# database_secret.conf
# 设置随机字符串以及数据库登入密码、还有postfix设置

secret_key = 'dasdasd'
test_mail = '请填入您的邮箱'
admin_mail = 'bbs_club'
database_password = '1234'

```
