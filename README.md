This is a practice Web Application written in python Flask. Visit [Microblog](https://test.chzcc.live).

Referrence Tutorial: [Miguel Grinberg's blog](https://github.com/miguelgrinberg/microblog).

---

## Note

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
    
