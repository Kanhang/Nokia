import commands
import datetime
import os
import sys

from celery import shared_task

from device.models import device


@shared_task
def ping_DeviceIPAddress():
    os.system('rm -f /home/code/management/console_ping_Device.txt')
    console_log = open('console_ping_Device.txt', 'ab+')
    sys.stdout = console_log
    sys.stdout.flush()
    num = 0
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    for data in device.objects.all():
        ip = data.IPAddress
        print ip
        output = commands.getoutput("ping -c 2 -w 2 " + ip)
        num = num + 1
        print num
        sys.stdout.flush()
        print output
        if "0% packet loss" in output:
            print ip + " Online"
            sys.stdout.flush()
            # data.Online = False
            device.objects.filter(IPAddress=ip).update(Status=True)
            device.objects.filter(IPAddress=ip).update(Update_time=date)
        else:
            print ip + " Offline"
            sys.stdout.flush()
            # data.Online = True
            device.objects.filter(IPAddress=ip).update(Status=False)
