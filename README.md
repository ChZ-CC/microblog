This is a practice Web Application written in python Flask. Visit [Microblog](https://test.chzcc.live).

Referrence Tutorial: [Miguel Grinberg's blog](https://github.com/miguelgrinberg/microblog).

### Note

#### 修正翻译 `2018-4-21`

- 修改一部分翻译。
- 日期和时间的本地化：

    代码修改：
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