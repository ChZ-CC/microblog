# 安装

进入到 microblog 目录中接着使用如下的命令创建一个虚拟环境:

```
$ python -m venv flask
```

上面的命令行在 flask 文件夹中创建一个完整的 Python 环境。

如果你使用 Python 3.4 以下的版本(包括 python 2.7)，你需要在创建虚拟环境之前下载以及安装 virtualenv.py 。

```
$ sudo easy_install virtualenv  # Mac OS
$ sudo apt-get install python-virtualenv    # linux like ubuntu
$ virtualenv flask  # 在 flask 文件夹中创建一个完整的 Python 环境。
```

安装 flask 包。

```
flask/bin/pip install flask
flask/bin/pip install flask-login
flask/bin/pip install flask-openid
flask/bin/pip install flask-mail
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install sqlalchemy-migrate
flask/bin/pip install flask-whooshalchemy
flask/bin/pip install flask-wtf
flask/bin/pip install flask-babel
flask/bin/pip install guess_language
flask/bin/pip install flipflop
flask/bin/pip install coverage
```

建基本的文件结构:

```
mkdir app
mkdir app/static
mkdir app/templates
mkdir tmp
```

# Chapter 12: Dates and Times

参考文章：https://www.cnblogs.com/franknihao/p/7374964.html

代码修改：

```
{% block scripts %}
    {{ super() }}
    {{ moment.include_moment() }}
    {{ moment.locale('zh-cn') }}
    <!-- moment.lang is deprecated, use moment.locale instead. 
        And 'zh' doesn't work, but 'zh-cn' does. -->
{% endblock %}
```

> 问题是，13章的翻译只支持 'zh' 这样纯字母的简称，'zh-cn' 是不可以的。于是又增加了判断句。

```
    {{ moment.include_moment() }}
    {% if g.locale=='zh' %}
    {% set local_lang = 'zh-cn' %}
    {% else %}
    {% set local_lang = g.locale %}
    {% endif %}
    {{ moment.locale(local_lang) }}
```

# Chapter 13: Babel 多语言支持

1. 安装：`(venv) $ pip install flask-babel`
2. 初始化、配置、标记需要翻译的文本。
3. 提取需要翻译的文本：`(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .`
4. 生成翻译目录：`pybabel init -i messages.pot -d app/translations -l es`
5. 翻译`messages.po`。
6. 编译：`(venv) $ pybabel compile -d app/translations`

增加新的翻译内容时：重复以上 2. 3.步，然后 update。

```
(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .
(venv) $ pybabel update -i messages.pot -d app/translations
```

创建flask command：

1. `cli.py`
2. `microblog.py` 中 import：`from app import cli`

```
(venv) $ flask translate init <language-code>   # 初始化某个翻译语言
(venv) $ flask translate update                 # 更新：包括 extract 和 update 两个操作。
(venv) $ flask translate compile                # 编译，将翻译文件<.po>编译为<.mo>文件。更新翻译文本之后需要编译并重启应用。
```

# Chapter 14: 实时翻译功能

## 微软翻译

(venv) $ export MS_TRANSLATOR_KEY=your-ms-translator-key

**config file**

`.env` 保存flask 应用所需的配置信息，特别是需要保密的信息。

使用：

`from dotenv import load_dotenv` 
`load_dotenv(os.path.join(basedir, '.env'))`

**不要加入版本控制。**
**FLASK_APP 和 FLASK_DEBUG** 不能再 .env 中配置，它们需要在 application 实例创建之前设置。

> 2018-5-3 改为百度翻译，重写了 translate 方法。

# Chapter 16: 全文搜索引擎 elasticsearch

**安装 elasticsearch**

brew 安装还是挺慢的，花了我一个多小时。所以下载安装包是个不错的选择。

```
CCdeMac:~ ChZ$ brew install elasticsearch
Updating Homebrew...
==> Downloading https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.3.tar.gz
######################################################################## 100.0%
==> Caveats
Data:    /usr/local/var/lib/elasticsearch/elasticsearch_ChZ/
Logs:    /usr/local/var/log/elasticsearch/elasticsearch_ChZ.log
Plugins: /usr/local/var/elasticsearch/plugins/
Config:  /usr/local/etc/elasticsearch/

To have launchd start elasticsearch now and restart at login:
  brew services start elasticsearch
Or, if you don't want/need a background service you can just run:
  elasticsearch
==> Summary
🍺  /usr/local/Cellar/elasticsearch/6.2.3: 112 files, 30.8MB, built in 79 minutes 55 seconds
```

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.deb.sha512
shasum -a 512 -c elasticsearch-6.2.4.deb.sha512 
sudo dpkg -i elasticsearch-6.2.4.deb


# Chapter 17: linux 部署

## 安全：

/etc/ssh/sshd_config: Disable root logins. Disable password logins.

```
PermitRootLogin no
PasswordAuthentication no
```

**ufw**

```
$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
$ sudo ufw --force enable
$ sudo ufw status
```

## 所需环境

```
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install mysql-server postfix supervisor nginx git
```

## Git flask应用的代码

Git push 从本地环境提交代码到 GitHub 网址：

```
CCdeMac:~ ChZ$ cd microblog
CCdeMac:microblog ChZ$ git init
Initialized empty Git repository in /Users/corawang/microblog/.git/
CCdeMac:microblog ChZ$ echo "This is a practice of flask. Code source from [Miguel Grinberg](https://github.com/miguelgrinberg/microblog)." > README
CCdeMac:microblog ChZ$ touch .gitignore
CCdeMac:microblog ChZ$ vim .gitignore
CCdeMac:microblog ChZ$ git add .                # 添加当前目录下的所有文件
CCdeMac:microblog ChZ$ git status               # 查看
CCdeMac:microblog ChZ$ git add .gitignore       # 添加一个文件
CCdeMac:microblog ChZ$ git rm -r --cache logs/  # 从缓存中删除目录
CCdeMac:microblog ChZ$ git rm --cache config.pyc    # 从缓存中删除文件
CCdeMac:microblog ChZ$ git commit -m "first version. chapter 1 to 14."
                                                # 创建新的提交，-m 备注信息
CCdeMac:microblog ChZ$ git remote add origin git@github.com:ChZ-CC/microblog.git
CCdeMac:microblog ChZ$ git remote rm origin     # 如果上一步填错了，需要修改 remote 目录，先删除再添加。
CCdeMac:microblog ChZ$ git push origin master   # 提交本地更新到 Git 网站。
CCdeMac:microblog ChZ$ git pull origin master   # 获取远程代码
```

**远程提交需要配置 ssh 秘钥和 gitconfig。**

将本地秘钥`~/.ssh/id_rsa.pub`添加到 git 账号。然后在本地配置 git 账号。

**创建 .env 文件**

```
SECRET_KEY=52cb883e323b48d78a0a36e8e951ba4a
MAIL_SERVER=localhost
MAIL_PORT=25
DATABASE_URL=mysql+pymysql://microblog:<db-password>@localhost:3306/microblog
MS_TRANSLATOR_KEY=<your-translator-key-here>
```

SECRET_KEY可以用 python 生成，`python3 -c "import uuid; print(uuid.uuid4().hex)`。

**创建 python 的虚拟环境，安装所需的package**

```
$ python3 -m venv venv
$ source venv/bin/activate

(venv) $ pip install -r requirements.txt
(venv) $ pip install gunicorn pymysql       # 新增的两个。
(venv) $ pip freeze > requirements.txt
```

**配置 FLASK_APP**
`$ echo "export FLASK_APP=microblog.py" >> ~/.profile`

**编译翻译文件**
`(venv) $ flask translate compile`

## 配置 MySql
```
mysql> create database microblog character set utf8 collate utf8_bin;
mysql> create user 'microblog'@'localhost' identified by '<db-password>';
mysql> grant all privileges on microblog.* to 'microblog'@'localhost';
mysql> flush privileges;
mysql> quit;

(venv) $ flask db upgrade
```

## 配置 Gunicorn 和 Supervisor

`(venv) $ gunicorn -b localhost:8000 -w 4 microblog:app`     # 用 gunicorn 启动应用

配置`/etc/supervisor/con.d/microblog.conf`: Supervisor configuration. 让应用自动启动。

```
[program:microblog]
command=/home/ubuntu/microblog/venv/bin/gunicorn -b localhost:8000 -w 4 microblog:app
directory=/home/ubuntu/microblog
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

`$ sudo supervisorctl reload`     # 重新启动应用


## 配置 Nginx

```
$ mkdir certs
$ openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem             
$ sudo rm /etc/nginx/sites-enabled/default
```

### /etc/nginx/sites-enabled/microblog: Nginx configuration.

```
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /home/ubuntu/microblog/certs/cert.pem;
    ssl_certificate_key /home/ubuntu/microblog/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/microblog_access.log;
    error_log /var/log/microblog_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/ubuntu/microblog/app/static;
        expires 30d;
    }
}
```

nginx 常用命令：

```
$ sudo service nginx reload     # 重启 Nginx 服务
$ sudo nginx -s reload
$ sudo nginx -s start
$ sudo nginx -t
$ sudo nginx -s quit
```

### 配置真实的 domain 和真实的 SSL 证书

需要：
1. 真实的 domain name；
2. domain name 添加 DNS 解析到自己的服务器； （`ping test.chzcc.live` 能找到服务器 IP 说明成功。）
3. 使用 certbot 为 domain 生成证书。

**安装 certbot**

```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot
```

**为配置文件添加真是 domain 和 location**

```
    # listen on port 80 (http)
    listen 80;
    server_name test.chzcc.live;
    location ~ /.well-known {
        root /var/www/chzcctest;
    }
```

> 更新配置文件后，记得要 reload，`sudo service nginx reload`。
> 但是好像跟这里的设置没有关系。？？

**为域名生成证书，然后将生成的 pem 文件路径添加到 Nginx config 中。**

```
$ sudo certbot certonly --webroot -w /var/www/chzcctest/ -d test.chzcc.live
```

更进一步的认证：`$ openssl dhparam -out /path/to/dhparam.pem 2048`
然后添加 cert 证书和 dhparam 证书到 Nginx 的配置文件中。

```
    ssl_certificate /etc/letsencrypt/live/test.chzcc.live/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/test.chzcc.live/privkey.pem;
    ssl_dhparam /home/ccxjj/dhparam.d/param.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:!DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security max-age=15768000;
```

**证书更新**

`$ sudo certbot renew` 证书的有效期是90d，到期需要更新。应该将它添加排程任务。


## postfix 的配置

参考文章：[Ubuntu上的安装配置/digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-16-04)

```
sudo apt-get update
sudo apt install mailutils
> 选择：Internet Site
> 输入：domain name "chzcc.live"
```

配置文件：`sudo vim /etc/postfix/main.cf`，default: see "postconf -d" output。修改配置文件后执行`sudo systemctl restart postfix` 命令**重启 postfix 服务**。

```
myorigin = $mydomain   #specifies the domain that appears in mail that is posted on this machine
myhostname = mail.chzcc.live    #The internet hostname of this mail system.
mydomain =                      #The internet domain name of this mail system. 默认是 myhostname 去掉第一个点前部分，即 chzcc.live。
inet_interfaces = loopback-only #仅作为发送邮件服务器
mydestination = $myhostname, localhost.$mydomain, $mydomain #The list of domains that are delivered via the $local_transport mail delivery transport.
relay_domains = $mydestination  #What destination domains (and subdomains thereof) this system will relay mail to. 默认为空。将本机邮件转发到哪些地址。
```

好复杂的哟。几番尝试之后，我的配置是这样的(仅改动的地方)：

```/etc/postfix/main.cf
myhostname = mail.chzcc.live
mydomain = chzcc.live
myorigin = $mydomain
relayhost =
mydestination = $myhostname, localhost.$mydomain, $mydomain
inet_interfaces = loopback-only
```

> 碰了好多次壁，配置参数好多，邮箱服务又复杂，至今没搞清楚。这样可以成功，仅此而已。其中 relayhost 如果设置值的话邮件就发送不成功，timeout。

**域名的 MX 解析**

参考文章：[添加 SPF 记录/digitalocean](https://www.digitalocean.com/community/tutorials/how-to-use-an-spf-record-to-prevent-spoofing-improve-e-mail-reliability)——用于防止其他人使用你的域名乱发邮件。

- 添加一个 A 记录，将服务器地址指向`mail.chzcc.live`。
- 添加一个 MX 记录，将`mail.chzcc.live`指向`chzcc.live`。
- 然后添加一个 TXT 记录，如："v=spf1 mx -all"(Allows the domain's MX hosts to send mail for the domain, and prohibits all other hosts.)。可以使用`nslookup -qt=txt chzcc.live`查看它的 TXT 记录。

**测试** SMTP 服务：

`echo "This is the body of the email" | mail -s "This is the subject line" your_email_address`

上面所有步骤完成之后，就可以发邮件了。

刚开始发出的邮件地址是 ccxjj@localhost.localdomain，于是试图通过修改配置改变它。无果。然后修改了服务器的 hostname，`sudo hostname chzcc.live`，然后就成功了。

**flask 应用发送验证邮件**

```.env 配置如下
MAIL_SERVER=localhost
MAIL_PORT=25
```

邮件的发送者可以任意指定".+@chzcc.live"。没有尝试把后面的域名改掉还能不能行。以后再试吧。

```
class Config(object):
    ...
    ADMINS = ['system@chzcc.live']
    ...
```

### 后期常用命令

```
(venv) $ git pull                              # download the new version
(venv) $ sudo supervisorctl stop microblog     # stop the current server
(venv) $ flask db upgrade                      # upgrade the database
(venv) $ flask translate compile               # upgrade the translations
(venv) $ sudo supervisorctl start microblog    # start a new server
```

# Chapter 20: Some JavaScript Magic 

> 实现“鼠标悬停呈现名片信息”的功能。


# Chapter 21: Notification


# Chapter 22: Background jobs

**Install rq and redis**

```
pip install rq
pip freeze > requirements.txt
```

- install redis on Mac: `brew install redis`

```
To have launchd start redis now and restart at login:
  brew services start redis
Or, if you don't want/need a background service you can just run:
  redis-server /usr/local/etc/redis.conf
==> Summary
🍺  /usr/local/Cellar/redis/4.0.9: 13 files, 2.8MB
```

- install redis on Ubuntu: [Doc: Quick start](https://redis.io/topics/quickstart)

```
ccxjj@chzcc:~$ wget http://download.redis.io/redis-stable.tar.gz
ccxjj@chzcc:~$ tar xvzf redis-stable.tar.gz
ccxjj@chzcc:~$ cd redis-stable
ccxjj@chzcc:~/redis-stable$ make
ccxjj@chzcc:~/redis-stable$ make test
ccxjj@chzcc:~/redis-stable$ sudo cp src/redis-server /usr/local/bin/
ccxjj@chzcc:~/redis-stable$ sudo cp src/redis-cli /usr/local/bin/
ccxjj@chzcc:~/redis-stable$ redis-server
32675:C 03 May 23:56:16.596 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
32675:C 03 May 23:56:16.596 # Redis version=4.0.9, bits=64, commit=00000000, modified=0, pid=32675, just started
32675:C 03 May 23:56:16.596 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
32675:M 03 May 23:56:16.597 * Increased maximum number of open files to 10032 (it was originally set to 1024).
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 4.0.9 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 32675

```

**设置为后台运行**

- 将`redis-stable/redis.conf`中的“daemonize no”修改为“daemonize yes”。
- 然后执行`redis-server ~/redis-stable/redis.conf`
- 验证：执行`redis-cli ping`，返回`PONG`。用 ps 命令查看 Redis 进程：`ps -aux | grep redis`

### HowTo use rq

**An example task**

```tasks.py
import time

def example(seconds):
    print('Starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('Task completed')
```

**Running RQ worker**
在虚拟环境下，执行命令`(venv)$ rq worker microblog-tasks`。他将监听分发到'microblog-tasks'这个列队/queue的所有任务/job。

想要多个 worker，运行多个`rq worker`即可，将他们连接到同一个列队/queue。queue 中出现 job 时，任意一个空闲 worker 会接手执行它。生产环境中 worker 数量至少跟 CUP 核数一样多。
RQ docs: http://python-rq.org/docs/workers/

**Exacuting tasks**

另一起个 terminal，进入`(venv)$`，在 shell session 中运行：

```
>>> from redis import Redis
>>> import rq
>>> queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
>>> job = queue.enqueue('app.tasks.example', 23)
>>> job.get_id()
'c651de7f-21a8-4068-afd5-8b982a6f6d32'
>>> job.is_finished
False
```

- `rq.Queue`对象是一个任务列表，参数'microblog-tasks'是 queue 的名字，参数 connection 是一个 Redis 连接对象。
- `queue.enqueue`将任务添加到列表中。运行完这一句之后，另一个终端上的`rq worker`就开始执行任务，这边则可以继续执行其他命令，如job.get_id()、job.is_finished。

### Linux 部署

添加一个 supervisor configuration：

```
[program:microblog-tasks]
command=/home/ccxjj/microblog/venv/bin/rq worker microblog-tasks
numprocs=1
directory=/home/ccxjj/microblog
user=ccxjj
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```



# Chapter 23: Application Programming Interfaces(APIs)

**6 Principles enumerated by Dr. Fielding**

- **Client-Server:** 客户端和服务器端明确分离。即，客户端和服务器端分别在独立的进程/processes中，通过传输协议/transport进行通信（通常是 TCP 网络基础上的 HPPT 协议）。

- **Layered System:** 当客户端需要与服务器通信时，它将与一个intermediary/中介连接，而不是跟实际的服务器连接。同样的，服务器端也是从一个 intermediary 接受请求，而不是直接来自客户端。这是 REST 的一个重要特征，因为允许添加中介结点/intermediary nodes，这让 APP 架构师可以设计大型、复杂的网络，他们可以通过使用负载均衡/load balancers、缓存/caches、代理服务器/proxy servers等工具/手段来满足大批量的请求。

- **Cache:** This principle extends the layered system, by indicating explicitly that it is allowed for the server or an intermediary to cache responses to requests that are received often to imporve system performance. 最常见的一个 implementation/实现 是各个 web 浏览器的缓存。
一个 API 要实现，目标服务器需要用 cache controls 来指明某个 response 是否可以被中介缓存。需要注意，因为部署在生产环境中的 APIs 要加密，缓存机制通常不在中介结点上实现，除非这个结点 terminates the SSL connection，或者可以进行加密和解密。

- **Code On Demand:** 这是一个可选规则：服务器向客户端返回可执行的代码。

- **Stateless:** 这是 REST purists 和 Pragmatists 之间的两大争议点之一。它要求一个 REST API 不应该保存任何客户端的状态。也就是，所有 web 开发中用来记住用户以便 navigate through the pages of the application 的机制，都不可以用。在无状态/stateless API 中所有的请求都需要包含服务器端所需的信息，用于识别/identify和认证/authenticate客户端，以及执行请求/carry out the request的信息。
这么做的原因是，无状态 server 非常容易 scale，你只需一个负载均衡器/a load balancer 上跑起多个 server 实例。如果服务器端储存客户端信息的话，会让事情变得很麻烦。

- **Uniform Interface:** 最后，最重要、最多讨论/most debated、最模糊记载/most vaguely documented REST 原则是 Uniform interface。四个方面：
    - unique resource identifiers: 例如 URL `/api/user/<user-id>` 这里 user-id 是数据库的user表中的主键/primary key指定给用户的编号/识别符/identifier。**URL 对应的是资源。**
    - resource representations: HTTP 协议中的 content negotiation 机制来实现。content-type，常用 json，可以其他。
    - self-descriptive messages: 请求和响应必须包含所有信息。典型例子，HTTP 请求方式中用 GET/POST/PUT/PATCH/DELETE 等指明客户端想要服务器完成什么操作。**HTTP request method 对应的是动作。**
    - hypermedia: 这个要求是最受争议，最少被实现的。

### 要实现的 routes 如下

```
HTTP Method    Resource URL                 Notes
GET            /api/users/<id>              Return a user.
GET            /api/users                   Return the collection of all users.
GET            /api/users/<id>/followers    Return the followers of this user.
GET            /api/users/<id>/followed     Return the users this user is following.
POST           /api/users                   Register a new user account.
PUT            /api/users/id                Modify a user.
```
