This is a practice Web Application written in python Flask. Visit [Microblog](https://koya.chzcc.live/explore).

Referrence Tutorial: [Miguel Grinberg's blog](https://github.com/miguelgrinberg/microblog).

---

## 简介

该应用目前实现了以下功能：

- [x] 用户注册/登录/重置密码
- [x] 发布消息/编辑个人资料/头像（gravatar）
- [x] 关注和取消关注
- [x] 支持中英双语（目前被我强制设置成了汉语）
- [ ] 全文搜索（服务器未安装elasticsearch）
- [x] 鼠标悬停弹出用户名片

用到的库和工具：

- 基础：Flask、Jinja2、python-dotenv、requests、threading
- 登录/注册验证：Flask-Login、Flask-WTF
- 数据库：Flask-SQLAlchemy、Flask-Migrate
- 时间/日期：Flask-Moment
- 语言：Flask-Babel
- CSS 框架：Flask-Bootstrap
- 邮箱服务：Flask-Mail
- Ajax：JavaScript
- 服务器部署：gunicorn（webserver）、Nginx（反向代理）、postfix（邮箱服务）、git（版本控制）、certbot（证书）、MySQL（数据库）。

---

## 章节笔记

> 未完成

---

## 提交版本备注

#### Initial Version `2018-4-1`

- 参考 Miguel 博客1-14章内容。

#### 修正翻译 `2018-4-21`

- `/explore`页面开放，无需注册可访问。
- 修改一部分翻译。
- 日期和时间的本地化：
    - `moment.js` 设置中文格式时间用 'zh-cn'，但是本地的翻译文件仅支持纯字母格式 'zh'，所以只好加了个判断句。
    
        ```
        {% block scripts %}
            {{ moment.include_moment() }}
            {% if g.locale=='zh' %}
            {% set local_lang = 'zh-cn' %}
            {% else %}
            {% set local_lang = g.locale %}
            {% endif %}
            {{ moment.locale(local_lang) }}
            <!-- Note that moment.lang is deprecated, so use moment.locale instead. 
                And 'zh' doesn't work, but 'zh-cn' does. -->
        {% endblock %}
        ```
#### 鼠标悬停 `2018-4-22`

根据 Miguel 的教程第20章，实现鼠标悬停跳出用户名片的功能。主要难题在 JavaScript 部分。需要学习。
