# windows10项目启动
- 准备好工具python3.x和git。下载好git上的文件，进入django_blogback目录，安装虚拟环境`pip install virtualenv`命名为**env** `virtualenv env`。win系统启动虚拟机：` .\env\Scripts\activate`
- 以后部署网站就在 虚拟机上进行。方便些
- 安装需求文件`pip -install -r requirement.txt`再启动项目`python manage.py runserver`

# 服务器部署项目
https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/

### 项目源码：
**克隆项目:**
```
~# git clone https://github.com/Freen247/django_blogback.git
~# pwd
/home/django_blogback
```

#### 创建虚拟环境
**虚拟环境是个好东西**,我选择的是在django项目中创建,方便处理。
```shell
~# cd .\django_blogback\
~# virtualenv django_env
~# source /django_env/bin/activate
~# pip install -r requirement.txt
```

### NGINX

尝试运行django项目：`python manage.py runserver`
成功！
注意ALLOWED_HOSTS的值：`[‘127.0.0.1’, ‘localhost’, ‘域名’]或者[*]`

#### 安装配置 Nginx
安装nginx：
- 安装nginx依赖工具PCRE，让nginx有rewrite功能：
1. 安装PCRE依赖工具`yum -y install make zlib zlib-devel gcc-c++ libtool  openssl openssl-devel`
2. cd /usr/local/src/ && wget http://downloads.sourceforge.net/project/pcre/pcre/8.35/pcre-8.35.tar.gz && tar zxvf pcre-8.35.tar.gz && cd pcre-8.35 &&./configure && make && make install

- 下载nginx并安装：`cd /usr/local/src/ &&wget http://nginx.org/download/nginx-1.6.2.tar.gz && tar zxvf nginx-1.6.2.tar.gz && cd nginx-1.6.2 &&`
` ./configure --prefix=/usr/local/webserver/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre=/usr/local/src/pcre-8.35&& make &&  make install`
- 在/usr/local/webserver/nginx/目录x下就是我们安装好的nginx了。
修改一下/usr/local/webserver/nginx/conf/nginx.conf 配置文件，不要使用默认的那个：

```shell
[root@VM_101_141_centos ~]# cat /usr/local/webserver/nginx/conf/nginx.conf

#user  nobody;
worker_processes  1;

error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log ;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
        upstream app_server {

    # for UNIX domain socket setups
    server unix:/home/django_blogback/gunicorn.sock fail_timeout=0;

    }
    server {
        charset utf-8;
        listen       80;
        server_name  bpywithacoin.cn;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;
         # static 和 media 的地址
        location /static {#注意!!!：static后面不能有/斜杠，否则会导致静态文件404
            alias /home/django_blogback/static;
        }
        location /media {
            alias /home/django_blogback/media;
        }


        location / {
           proxy_pass http://app_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
}
}
```
#### 连接 Nginx 配置
Systemd服务文件以.service结尾，比如现在要建立nginx为开机启动，如果用yum install命令安装的，yum命令会自动创建nginx.service文件，直接用命令

`systemcel enable nginx.service`

设置开机启动即可。
在这里我是用源码编译安装的，所以要手动创建nginx.service服务文件。
开机没有登陆情况下就能运行的程序，存在系统服务（system）里，即：
`/lib/systemd/system/`
在系统服务目录创建nginx.service
`vi /lib/systemd/system/nginx.service`
```shell
[Unit]
Description=nginx
After=network.target
  
[Service]
Type=forking
ExecStart=/usr/local/webserver/nginx/sbin/nginx
ExecReload=/usr/local/webserver/nginx/sbin/nginxnginx -s reload
ExecStop=/usr/local/webserver/nginx/sbin/nginxnginx -s quit
PrivateTmp=true
  
[Install]
WantedBy=multi-user.target
```
有的的服务的目录实在etc/systemd/system/,,如果失败了k可以再试一下

上面的配置检查好之后，使用下面的命令来将这个配置跟 Nginx 建立连接，使用命令：
`ln -s /usr/local/nginx/conf/nginx nginx安装dir/nginx/sites-enabled`
测试是否配置成功：
 `/usr/local/webserver/nginx/sbin/nginx -t`

没报错的话，重启一下 Nginx：`systemctl restart nginx`

好了，重启 Nginx 之后可以登录自己配置的域名，看看自己的项目是不是已经成功的运行了呢！
### gunicorn

#### 安装和配置

`安装： pip install gunicorn`
尝试用gunicorn开启我们的项目：
`gunicorn django_blogback.wsgi:application --bind 0.0.0.0:8000`
```shell
[2019-06-30 14:26:04 +0800] [19524] [INFO] Starting gunicorn 19.9.0
[2019-06-30 14:26:04 +0800] [19524] [INFO] Listening at: http://0.0.0.0:8000 (19524)
[2019-06-30 14:26:04 +0800] [19524] [INFO] Using worker: sync
[2019-06-30 14:26:04 +0800] [19527] [INFO] Booting worker with pid: 1952
```
返回结果成功！这样我们就可以通过gunicorn开启我们的项目。
编写gunicorn_start.sh脚本，`chmod +x gunicorn_start.sh`便于nohup工具后台持续运行.
```shell
[root@VM_101_141_centos home]# cat gunicorn_start.sh
#!/bin/bash
NAME='django_blogback' #应用的名称i
DJANGODIR=/home/django_blogback #django项目的目录
SOCKFILE=/home/django_blogback/gunicorn.sock #使用这个sock来通信
USER=root #运行此应用的用户
GROUP=root #运行此应用的组
NUM_WORKERS=3 #gunicorn使用的工作进程数
DJANGO_SETTINGS_MODULE=django_blogback.settings #django的配置文件
DJANGO_WSGI_MODULE=django_blogback.wsgi #wsgi模块
LOG_DIR=/home/logs #日志目录

echo "starting $NAME as `whoami`"

#激活python虚拟运行环境
cd $DJANGODIR
source /envblog/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#如果gunicorn.sock所在目录不存在则创建
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

#启动Django

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=debug \
    --bind=unix:$SOCKFILE \
    --access-logfile=${LOG_DIR}/gunicorn_access.log
```
有一个日志文件夹和nohup日志文件需要创建：
```shell
[root@VM_101_141_centos home]# ls
django_blogback  gunicorn_start.sh  logs  nohup.log
```
LOG_DIR=/home/logs #日志目录  和 nohup.log #日志文件
#### 启动配置文件

文件配置完成之后，使用nohup的命令启动服务：
后台持续运行:`nohup ./gunicorn_start.sh > nohup.log`
成功！：
```shell
(envblog) [root@VM_101_141_centos home]# nohup ./gunicorn_start.sh > nohup.log
nohup: ignoring input and redirecting stderr to stdout
```
可能会发现这时候终端无法输入指令，直接退出就好。

### 维护、更改文件之后后续操作

之后的项目维护中：
- 如果更改了 gunicorn 的sh文件，需要重新使用nohup命令启动。

- 如果修改了 Nginx 的配置文件，先测试以配置是否成功` /usr/local/webserver/nginx/sbin/nginx -t `再重启`systemctl restart nginx`

- 如果调用了新的django类似jet、xadmin、django-mdeditor包添加组件当需要另外调用js\css样式的时候，需要运行`python manage.py collectstatic`

-如果更改models更改注册的模型，需要增删改数据库等，需要运行
`python manage.py makemigrations`和`python manage.py migrate`

有疑问欢迎
mail aboyinsky@outlook.com 
qq 1351975058
qq群 706340320