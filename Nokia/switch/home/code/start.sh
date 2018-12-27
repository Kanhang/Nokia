 #!/bin/bash
    cd /home/code/management

    nohup rabbitmq-server &
    export C_FORCE_ROOT="true"
    ps aux | grep celery | awk '{system("kill -9 " $2)}'
    nohup celery worker -A management -l info > /home/code/log.txt 2>&1  & 

    kill -9 $(pidof uwsgi)
   # /usr/bin/uwsgi --ini uwsgi.ini
   /usr/bin/uwsgi --ini uwsgi.ini & python manage.py celery beat &python manage.py celeryd -l info &
   # ����nohup��&���������ֹ�ն˵�ʱ�򣬶�ʱ����ֹͣ�� ����������ݡ���
    #nohup��ʾ��Զִ�У� ��������������start.sh��Ҳ����ɾ�����������Ե��� �ظ�����
    #& ��ʾ��ִ̨�У� ��������start.sh ,����ɾ�������񡣡���
   #  nohup /usr/bin/uwsgi --ini uwsgi.ini & python manage.py celery beat &python manage.py celeryd -l info & 
    nohup /usr/sbin/nginx -s reload
