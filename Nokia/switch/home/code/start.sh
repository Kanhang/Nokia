 #!/bin/bash
    cd /home/code/management

    nohup rabbitmq-server &
    export C_FORCE_ROOT="true"
    ps aux | grep celery | awk '{system("kill -9 " $2)}'
    nohup celery worker -A management -l info > /home/code/log.txt 2>&1  & 

    kill -9 $(pidof uwsgi)
   # /usr/bin/uwsgi --ini uwsgi.ini
   /usr/bin/uwsgi --ini uwsgi.ini & python manage.py celery beat &python manage.py celeryd -l info &
   # 不加nohup和&情况，当终止终端的时候，定时任务停止， 不会继续备份。。
    #nohup表示永远执行， 就是你重新运行start.sh，也不会删除旧任务，所以导致 重复任务。
    #& 表示后台执行， 重新运行start.sh ,不会删除旧任务。。。
   #  nohup /usr/bin/uwsgi --ini uwsgi.ini & python manage.py celery beat &python manage.py celeryd -l info & 
    nohup /usr/sbin/nginx -s reload
