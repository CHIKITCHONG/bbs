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
