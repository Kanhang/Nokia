from __future__ import absolute_import
import os
import commands
import datetime
from django.conf import settings
import shutil
from switch.backup import log_summary
from celery import shared_task
from switch.rename import rename_juniper,rename_dell_cisco
from switch.auto_config import read_excel,run_command
from switch.backup import starting_backup
from switch.models import BackUp
from abnormal.models import abnormal
from data.models import food
from brand.models import brand
import xlrd, xlwt, os, time, re
from django.conf import settings
from django.core.mail import send_mail
from django.db import connection, transaction
import random
from django.http import HttpResponse
import time
import os, time, sys, stat
#from switch.views import sort_undownloadable
# *_*coding=utf-8 *_*
@shared_task
def get_Info_telnet():
    base_path = os.getcwd()
    list= BackUp.objects.all()
    path ="/root/name/"
    for data in list:
        ip = data.IPAddress
        type=data.Type
        file="/home/code/management/static/admin/template/dee.sh"
        output = commands.getoutput("nmap -p 23 "+ip+" -n")
        resault = True
        if "Host is up" in output and "open" in output:
            print ip+" Port 23 open"
            sys.stdout.flush()
        else:
            print ip+" Port 23 closed"
            print "----------------------------------------------------------" + '\n'
            sys.stdout.flush()
            resault = False
            #return False
        if resault:
          f1 = open(file, "r")
          os.chdir(path)
          f2 = open("%s.sh" % path, "w")
          #print 'successful'
          for line in f1:
              if "xx.xx.xx.xx" in line:
                  line = line.replace("xx.xx.xx.xx", ip)
              f2.write(line)
          os.rename('%s.sh' % path, ip + ".sh")
          cmd = path + ip + '.sh'
          f1.close()
          f2.close()
          os.chmod(cmd, stat.S_IXOTH)
          output = commands.getoutput(cmd)
          #print output
          os.system('rm -rf ' + cmd)
          os.chdir(base_path)
          rear = data.Name
          model = data.Model
          vers = data.Version
          flag = True
          if "invalid" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "incorrect" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "Authorization failed." in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "Error" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "assword" not in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if flag:
              if "Networking OS" in output:
                  type = "Dell"
              if "Cisco" in output:
                  type = "Cisco"
              if "JUNOS" in output:
                  type = "Juniper"
              if type == "Cisco":
                  file1 = "/home/code/management/static/admin/template/cisver.sh"
                  e1 = open(file1, "r")
                  os.chdir(path)
                  e2 = open("%s.sh" % path, "w")
                  # print 'successful'
                  for line in e1:
                      if "xx.xx.xx.xx" in line:
                          line = line.replace("xx.xx.xx.xx", ip)
                      e2.write(line)
                  os.rename('%s.sh' % path, ip + ".sh")
                  cmd = path + ip + '.sh'
                  e1.close()
                  e2.close()
                  os.chmod(cmd, stat.S_IXOTH)
                  output1 = commands.getoutput(cmd)
                  os.system('rm -rf ' + cmd)
                  os.chdir(base_path)
                  str = "assword:"
                  if "inutes" in output1:
                      if output1.find("show version") > output1.find("inutes"):
                          str = "inutes"
                  list = output1.split(str, 1)
                  sys.stdout.flush()
                  #print list
                  vm = list[1].split(":", 1)
                  if len(vm)>=2:
                    model =((vm[1].split("\n",1))[0]).strip()
                    if "*" in list[1]:
                        vm1 = vm[1].split("*", 1)
                        vm_list = vm1[1].split(" ", vm1[1].count(" "))
                        mv_list = []
                        for i in vm_list:
                            if i:
                                mv_list.append(i)
                        vers = mv_list[3]
                    else:
                        if "Version" in output:
                            str = "Version"
                        listv = output.split(str, 1)
                        vers = ((listv[1].split(" ", 2))[1]).split()[0]
                        vers = vers.strip(",")
                  else:
                      str = "assword:"
                      if "inutes" in output:
                          if output.find("show version") > output.find("inutes"):
                              str = "inutes"
                      list = output.split(str, 1)
                      if "Catalyst" in output:
                          str = "Catalyst"
                          listvm = output.split(str, 1)
                      #listvm = list[1].split(',',2)
                          model=((listvm[1].split(" ",2))[1]).split()[0]
                      else:
                          listvm = list[1].split(',', 2)
                          model = ((listvm[1].split(" ", 2))[1]).split()[0]
                      if "Version" in output:
                          str = "Version"
                      listv = output.split(str, 1)
                      vers = ((listv[1].split(" ", 2))[1]).split()[0]
                      vers = vers.strip(",")
                      if model == "c7600rsp72043_rp" or model == "c7600s72033_rp" or model == "s72033_rp":
                          model = "c7609"
                  if list:
                      rear = list[1]
                      rear = rear[0: rear.find("#")]
                      #print "***************Cisco" + rear
                      if "The SupportAssist EULA" in rear:
                          list = rear.split("SupportAssist.", 1)
                          rear = list[1]
                  rear = rear.strip()
                  print ip + " "+ type +" "+ rear
                  print "----------------------------------------------------------" + '\n'
                  sys.stdout.flush()
                  #data.Name = rear
                  #data.Type = type
                  #data.save()

                  BackUp.objects.filter(IPAddress=ip).update(Name = rear)
                  BackUp.objects.filter(IPAddress=ip).update(Type = type)
                  BackUp.objects.filter(IPAddress=ip).update(Model = model)
                  BackUp.objects.filter(IPAddress=ip).update(Version = vers)

              if type == "Dell":
                  str = "assword:"
                  if "inutes" in output:
                      if output.find("show version") > output.find("inutes"):
                          str = "inutes"
                  list = output.split(str, 1)
                  if "Software Version:" in output:
                      str = "Software Version:"
                      list1 = output.split(str, 1)
                      vers = ((list1[1].split("\n", 1))[0]).split()[0]
                      vers = vers.strip()
                  if "System Type:" in output:
                      str = "System Type:"
                      list1 = output.split(str, 1)
                      model = ((list1[1].split("\n", 1))[0]).split()[0]
                      model = model.strip()
                  #print list
                  if list:
                      rear = list[1]
                      rear = rear[0: rear.find("#")]
                      #print "***************Cisco" + rear
                      if "The SupportAssist EULA" in rear:
                          list = rear.split("SupportAssist.", 1)
                          rear = list[1]
                  rear = rear.strip()
                  print ip + " " + type + " " + rear
                  print "----------------------------------------------------------" + '\n'
                  sys.stdout.flush()
                  #data.Name = rear
                  #data.Type = type
                  #data.save()
                  BackUp.objects.filter(IPAddress=ip).update(Name = rear)
                  BackUp.objects.filter(IPAddress=ip).update(Type = type)
                  BackUp.objects.filter(IPAddress=ip).update(Model = model)
                  BackUp.objects.filter(IPAddress=ip).update(Version = vers)

              if type == "Juniper":
                  list = output.split("@", 1)
                  if "Junos:" in output:
                      str = "Junos:"
                      list1 = output.split(str, 1)
                      vers = ((list1[1].split("\n", 1))[0]).split()[0]
                      vers = vers.strip()
                  else:
                      list1 = output.split("[", 1)
                      vers = ((list1[1].split("]", 1))[0]).split()[0]
                  if "Model:" in output:
                      str = "Model:"
                      list1 = output.split(str, 1)
                      model = ((list1[1].split("\n", 1))[0]).split()[0]
                      model = model.strip()
                  if list:
                      #print list
                      rear = list[1]
                      rear = rear[0: rear.find(">")]
                  rear=rear.strip()
                  print ip + " " + type + " " + rear
                  print "----------------------------------------------------------" + '\n'
                  sys.stdout.flush()
                  #data.Name = rear
                  #data.Type = type
                  #data.save()
                  BackUp.objects.filter(IPAddress=ip).update(Name = rear)
                  BackUp.objects.filter(IPAddress=ip).update(Type = type)
                  BackUp.objects.filter(IPAddress=ip).update(Model = model)
                  BackUp.objects.filter(IPAddress=ip).update(Version = vers)

@shared_task
def get_Name_telnet():
    os.system('rm -f /home/code/management/console_Name_ALL.txt')
    console_log=open('console_Name_ALL.txt','ab+')
    sys.stdout=console_log
    num = 0
    base_path = os.getcwd()
    list= BackUp.objects.all()
    path ="/root/name/"
    for data in list:
        ip = data.IPAddress
        type=data.Type
        file="/home/code/management/static/admin/template/dee.sh"
        num = num + 1
        print num
        print "-----------------------------------------------------"
        sys.stdout.flush()
        output = commands.getoutput("nmap -p 23 "+ip+" -n")
        resault = True
        if "Host is up" in output and "open" in output:
            print ip+" Port 23 open"
            sys.stdout.flush()
        else:
            print ip+" Port 23 closed"
            sys.stdout.flush()
            resault = False
        if resault:
          f1 = open(file, "r")
          os.chdir(path)
          f2 = open("%s.sh" % path, "w")
          #print 'successful'
          for line in f1:
              if "xx.xx.xx.xx" in line:
                  line = line.replace("xx.xx.xx.xx", ip)
              f2.write(line)
          os.rename('%s.sh' % path, ip + ".sh")
          cmd = path + ip + '.sh'
          f1.close()
          f2.close()
          os.chmod(cmd, stat.S_IXOTH)
          output = commands.getoutput(cmd)
          #print output
          os.system('rm -rf ' + cmd)
          os.chdir(base_path)
          rear = data.Name
          flag = True
          if "invalid" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "incorrect" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "Authorization failed." in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "Error" in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if "assword" not in output:
              print ip + " Authorization failed"
              print "----------------------------------------------------------" + '\n'
              sys.stdout.flush()
              flag = False
          if flag:
              if "Networking OS" in output:
                  type = "Dell"
              if "Cisco" in output:
                  type = "Cisco"
              if "JUNOS" in output:
                  type = "Juniper"
              if type == "Cisco" or type == "Dell":
                  str = "assword:"
                  if "inutes" in output:
                      if output.find("show version") > output.find("inutes"):
                          str = "inutes"
                  list = output.split(str, 1)
                  #print list
                  if list:
                      rear = list[1]
                      rear = rear[0: rear.find("#")]
                      #print "***************Cisco" + rear
                      if "The SupportAssist EULA" in rear:
                          list = rear.split("SupportAssist.", 1)
                          rear = list[1]
                          #print rear
                  rear=rear.strip()
                  print ip + " " + rear
                  print "-----------------------------------------------------" + '\n'
                  sys.stdout.flush()
                  #data.Name = rear
                  #data.save()
                  BackUp.objects.filter(IPAddress=ip).update(Name = rear)
                  



              if type == "Juniper":
                  list = output.split("@", 1)
                  if list:
                      #print list
                      rear = list[1]
                      rear = rear[0: rear.find(">")]
                      #print rear
                  rear=rear.strip()
                  print ip + " " + rear
                  print "-----------------------------------------------------" + '\n'
                  sys.stdout.flush()
                  #data.Name = rear
                  #data.save()
                  BackUp.objects.filter(IPAddress=ip).update(Name = rear)

@shared_task
def gather_abnormal():
    bk_failed_num=BackUp.objects.filter(BackupFailed="Backupfailed").count()
    offline_num= BackUp.objects.filter(Online=False).count()
    nonstandard_num=BackUp.objects.filter(Stdname=False).count()
    date =datetime.datetime.now().strftime('%Y-%m-%d')
    if abnormal.objects.filter(date=date):
        abnormal.objects.filter(date=date).update(bkfailed=bk_failed_num,offline=offline_num,nonstandard=nonstandard_num)
    else:
        abnormal.objects.create(date=date,bkfailed=bk_failed_num,offline=offline_num,nonstandard=nonstandard_num)
@shared_task
def check_standard():
    os.system('rm -f /home/code/management/console_ns_ALL.txt')
    console_log = open('console_ns_ALL.txt', 'ab+')
    sys.stdout = console_log
    list = BackUp.objects.all()
    for data in list:
        st = data.Name
        if st:
            list = st.split("_", st.count("_"))
            if len(list) == 6:
                if "" not in list:
                    BackUp.objects.filter(IPAddress=data.IPAddress).update(Stdname=True)
                else:
                    print data.IPAddress
                    print "false"
                    sys.stdout.flush()
            else:
                print data.IPAddress
                print "false"
                sys.stdout.flush()
        else:
            print data.IPAddress
            print "false"
            sys.stdout.flush()


'''@shared_task
def rename(path):
    wb = xlrd.open_workbook(filename=path)
    print "renametask"
    ws = wb.sheets()[0]    # the way xlrd acquires its worksheet
    nrow = ws.nrows
    headers = ['DU', 'Floor', 'Rack', 'U', 'Brand', 'Name', 'IP']
    lists = []
    num=0
    for row in range(1, nrow):
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value

        lists.append(r)
    log = open('/home/switch_rename/rename_log.txt','wb')
    error = 0
    ret = os.system("echo Config Start > /home/switch_rename/rename_log.txt")  # found
    print ret

    for cell in lists:
        DU = cell['DU']
        Floor = cell['Floor']
        Rack = cell['Rack']
        U = cell['U']
        Brand = cell['Brand']
        Name = cell['Name']
        IP = cell['IP']

        reg = "^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$"

        if DU == '':
            continue
        switch_name = DU + '_' + Floor + '_' + Rack + '_' + str(int(U)) + '_' + str(int(Brand)) + '_' + Name
        print switch_name
        num = num + 1
        print num
        if not re.match(reg, IP):
            log.write('Incorrect IP address ' + IP + '\n')
            error = error + 1
            continue
        numfile = open('/home/switch_rename/count.txt', 'wb')  # found
        numfile.write(str(num))
        numfile.close()
        if int(Brand) < 5:
            try:
                if not rename_dell_cisco(IP, switch_name):
                    error = error + 1
                    log.write(IP + ' Brand mismatch\n')
            except Exception, e:
                error = error +1
                log.write(IP + ' Authentication error\n')
        elif int(Brand) < 12:
            try:
                if not rename_juniper(IP, switch_name):
                    error = error + 1
                    log.write(IP + ' Brand mismatch\n')
            except Exception, e:
                error = error + 1
                log.write(IP + ' Authentication error\n')
        else:
            try:
                if not rename_dell_cisco(IP, switch_name):
                    error = error + 1
                    log.write(IP + ' Brand mismatch\n')
            except Exception, e:
                error = error + 1
                log.write(IP + ' Authentication error\n')
    log.write('finished!\n')
    if(error == 0):
        log.write('Rename Complete!')
    else:
        log.write('Total Failed: '+str(error))
    log.close()
    os.system('rm -rf /home/switch_rename/renameExcel.xlsx')
'''



@shared_task
def ping_IPAddress():
    os.system('rm -f /home/code/management/console_ping_ALL.txt')
    console_log = open('console_ping_ALL.txt', 'ab+')
    sys.stdout = console_log
    sys.stdout.flush()
    num = 0
    for data in BackUp.objects.all():
        ip = data.IPAddress
        output = commands.getoutput("nmap -p 23,22 "+ip+" -n")
        num = num + 1
        print num
        sys.stdout.flush()
        #print output
        if "22/tcp open" in output or "23/tcp open" in output:
            print ip + " Online"
            sys.stdout.flush()
            #data.Online = False
            BackUp.objects.filter(IPAddress=ip).update(Online = True)
        else:
            print ip + " Offline"
            sys.stdout.flush()
            #data.Online = True
            BackUp.objects.filter(IPAddress=ip).update(Online = False)

        #data.save()



        #ping -c 3 -W 3 10.69.40.75



'''@shared_task
def command_config(path):
    wb = xlrd.open_workbook(filename=path)
    print "configtask"
    ws = wb.sheets()[0]
    nrow = ws.nrows
    headers = ['IP', 'Brand']
    lists = []
    error = 0
    num = 0
    log = open('/home/auto_config/config_log.txt', 'a')
    for row in range(1, nrow):
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value
        lists.append(r)
        # lists include all the rows in the sheet, each row is a list
    ret = os.system("echo Config Start > /home/auto_config/config_log.txt") #found

    for cell in lists:
        IP = cell['IP']
        brand = cell['Brand']


        if IP == '':
            continue

        num = num +1
        print num
        numfile = open('/home/auto_config/count.txt', 'wb')  # wb means write only if the file exists ,then overrides it
        # verse visa, create the file
        numfile.write(str(num))
        numfile.close()

        reg = "^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$";
        if not re.match(reg, IP):
            log.write('Incorrect IP address ' + IP + '\n')
            error = error + 1
            continue


        try:
            if not read_excel(IP, path, brand):
                error = error + 1
                log.write(IP + ' failed!\n')
                print IP + ' failed!'
        except Exception, e:
            error = error + 1
            log.write(IP + ' failed!\n')
            print IP + ' failed!'

    log.write('finished!\n')
    if error > 0:
        log.write('Total Failed: '+str(error))
    else:
        log.write('Config Complete!')
    log.close()
'''

@shared_task
def cron_delete():
    path = "/root/backup"
    file_path ="/home/backup/log_summary.txt"
    if os.path.exists(file_path):
        os.remove(file_path)

    if not os.path.exists(path):
        os.mkdir("/root/backup")
    shutil.rmtree(path)
    # ''' ls = os.listdir(path)
    #for i in ls:
     #   new_path = os.path.join(path, i)
      #  if os.path.isdir(new_path):
       #     cron_delete()
        #else:
         #   os.remove(new_path)
    #'''


@shared_task
def save_brand():
    month = str(datetime.datetime.now().month)  # the Ip_address only has one record per month
    if int(month) < 10:
        month = "0" + str(month)
    year = str(datetime.datetime.now().year)
    cursorw = connection.cursor()
    cursorw.execute("select distinct(type) from brand.brand_brand;")
    arow= cursorw.fetchall()
    type_list=[]
    bk_type_list=[]
    #print "arow"
    #print arow
    for Bdata in arow:
        #print Bdata[0]
        type_list.append(Bdata[0])
    cursors = connection.cursor()
    cursors.execute("select distinct(Type),count(Type) from switch_backup group by Type;")
    rows = cursors.fetchall()
    #print "rows"    
    #print rows
    for Bdata in rows:
        bk_type_list.append(Bdata[0])
        if not brand.objects.filter(type=Bdata[0], month=year + "-" + month):
            if Bdata[0]:
                brand.objects.create(type=Bdata[0], month=year + "-" + month, num=str(Bdata[1]))
        else:
            brand.objects.filter(type=Bdata[0], month=year + "-" + month).update(type=Bdata[0], month=year + "-" + month,num=str(Bdata[1]))
    #print "type_list"
    #print type_list
    #print "bk_type_list"
    #print bk_type_list
    for Bdata in type_list:
        #print Bdata
        if Bdata not in bk_type_list:
            #print "**************"
            #print Bdata
            brand.objects.filter(type=Bdata).delete()

@shared_task
def save_data():
    month=str(datetime.datetime.now().month) #the Ip_address only has one record per month
    if int(month)<10:
       month="0"+str(month)
    year = str(datetime.datetime.now().year)
    #food.objects.all().update(num=0)
    cursor = connection.cursor()
    cursor.execute("select distinct(du) from data.data_food;")
    row=cursor.fetchall()
    food_du_list=[]
    backup_du_list=[]
    for data in row: #  prompt: Delete the row in table food  if its du is not present at backup table
        food_du_list.append(data[0]) #  total DUs
    cursor.execute("select distinct(DU),count(DU) from switch_backup group by DU;")
    row = cursor.fetchall()
    for data in row:
        backup_du_list.append(data[0])
        if not food.objects.filter(du=data[0],month=year + "-" + month):
            food.objects.create(du=data[0],month=year+"-"+ month,num=str(data[1]))
        else:
            food.objects.filter(du=data[0], month=year + "-" + month).update(du=data[0],month=year+"-"+ month,num=str(data[1]))
    for du in food_du_list:
        if du not in backup_du_list:
            (food.objects.filter(du=du)).delete()


@shared_task
def command_backup():
# try:
    os.system('rm -f /home/code/management/console_back.txt')
    console_log = open('console_back.txt', 'ab+')
    sys.stdout = console_log
    BackUp.objects.all().update(BackupFailed="")
    settings.UNDOWNLOADABLE_IP=[]
    print "backup task"
    sys.stdout.flush()
    error = 0
    num = 0
   # Backup_failure=[]
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    local_time2 = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    log = open('/home/backup/backup_log.txt', 'a+')     # add new to the file and create file if it does not exist
    ret = os.system("echo backup Start > /home/backup/backup_log.txt")  # found

    log.write(local_time + '\n')
    log.write("------------------------------------------------------------------------------"+'\n')
    qs = BackUp.objects.all()
    for data in qs:
        ip = data.IPAddress
        type = data.Type
        du = data.DU
        loc = data.Location
        num = num + 1
        print num
        sys.stdout.flush()
        numfile = open('/home/backup/count.txt', 'wb')  # found
        numfile.write(str(num))
        numfile.close()

        reg = "^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$"      # to match ip Address
        if not re.match(reg, ip):
            log.write('Incorrect IP address ' + ip + '\n')

            error = error + 1
            data = BackUp.objects.get(IPAddress=ip)
            #data.BackupFailed = "Backupfailed"
            #data.save()
            BackUp.objects.filter(IPAddress=ip).update(BackupFailed = "Backupfailed")
            continue

        try:
            if not starting_backup(ip, type, du, loc):
                error = error + 1
                data = BackUp.objects.get(IPAddress=ip)
                #data.BackupFailed = "Backupfailed"
                #data.save()
                BackUp.objects.filter(IPAddress=ip).update(BackupFailed = "Backupfailed")
                log.write(ip + ' failed!\n')
                print ip + ' failed!'
                sys.stdout.flush()
            else:
                #data.Last_backup_date = local_time2
                #data.save()
                BackUp.objects.filter(IPAddress=ip).update(BackupFailed="Backupsucceed")
                BackUp.objects.filter(IPAddress=ip).update(Last_backup_date = local_time2)
        except Exception, e:
            error = error + 1
            data = BackUp.objects.get(IPAddress=ip)
            #data.BackupFailed = "Backupfailed"
            #data.save()
            BackUp.objects.filter(IPAddress=ip).update(BackupFailed = "Backupfailed")
            log.write(ip + ' failed!\n')
            print ip + ' failed!'
            sys.stdout.flush()
    log.write("------------------------------------------------------------------------------" + '\n')
    log.write('finished!\n')

    if error > 0:
        log.write('Total Failed: ' + str(error) + '\n')
    else:
        log.write('backup Complete!\n\n')

    log.close()
    log_summary()  # closing the file to read full content
   # Backup_failure=list(set(Backup_failure))

@shared_task
def scan():
    os.system('rm -f /home/code/management/console_scan.txt')
    console_log = open('console_scan.txt', 'ab+')
    sys.stdout = console_log
    base_path = os.getcwd()
    from subnet.models import subnet
    list = subnet.objects.all()
    success_num = 0
    failed_num = 0
    repeat_num = 0
    for subdata in list:
        subnet = str(subdata.subnet)
        du = str(subdata.du)
        location = str(subdata.location)
        snmp = str(subdata.snmp_version)
        community = str(subdata.Community)
        username = str(subdata.Username)
        password = str(subdata.Password)
        authority = str(subdata.Authority)
        authenproto = " -a " + str(subdata.Authentication_protocol)
        pripro = " -x " + str(subdata.privacy_protocol)
        passphase =" -X " + str(subdata.Passphase)
        if str(subdata.Authentication_protocol) == "None" or str(subdata.Authentication_protocol) == "":
            authenproto = ""
        if str(subdata.privacy_protocol) == "None" or str(subdata.privacy_protocol) == "":
            pripro = ""
        if str(subdata.Passphase) == "None" or str(subdata.Passphase) == "":
            passphase = ""
        print "subnet " + subnet
        sys.stdout.flush()
        flag = True
        if not subnet :
            print "Please enter a IP_subnet"
            sys.stdout.flush()
            flag = False
        if not du :
            print "Please enter a du"
            sys.stdout.flush()
            flag = False
        if not location :
            print "Please enter location"
            sys.stdout.flush()
            flag = False
        if not snmp :
            print "Please enter snmp_version"
            sys.stdout.flush()
            flag = False
        if '/' not in subnet:
            print "Please enter a IP_subnet"
            sys.stdout.flush()
            flag = False
        if flag:
          list = subnet.split('/',1)
          sys.stdout.flush()
          ip = list[0]
          if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
              flag = False
          if len(list)>1:
              mask = list[1]
          if not mask:
              print "format incorrect"
              sys.stdout.flush()
              flag = False
          if mask:
              if int(mask) == 0:
                  print "mask error"
                  sys.stdout.flush()
                  flag = False
              if int(mask) < 0 or int(mask) > 32:
                  print "mask error"
                  sys.stdout.flush()
                  flag = False
              if flag:
                  num = 0
                  cmd = "nmap -host-timeout 10s -p 23 " + subnet + " -n"
                  output = commands.getoutput(cmd)
                  # print output
                  sys.stdout.flush()
                  x = output.count("for")
                  subip = output.split("for", x)
                  # print "length"+str(len(subip))
                  sys.stdout.flush()
                  for pg in subip:
                      if 'open' in pg or 'filtered' in pg:
                          flag = False
                          index = pg.find("Host")
                          ip = pg[1:index - 1]
                          num = num + 1
                          print num
                          sys.stdout.flush()
                          if "Starting Nmap" in pg:
                              continue
                          if snmp == "v2c":
                              cmd0 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " SNMPv2-MIB::sysName"
                              output0 = commands.getoutput(cmd0)
                              if "STRING: " in output0:
                                  cmd = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " SNMPv2-MIB::sysDescr"
                                  output = commands.getoutput(cmd)
                                  if "STRING: " in output:
                                      cmd2 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " DISMAN-EVENT-MIB::sysUpTimeInstance"
                                      output2 = commands.getoutput(cmd2)
                                      if "Timeticks: " in output2:
                                          sList = output0.split("STRING: ", 1)
                                          name = sList[1]
                                          if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name or ".tdlte.lab" in name:
                                              name = name[0:len(name) - 10]
                                          if "Application Software Version" in output and "Series" in output:
                                              ty = "Dell"
                                          elif "Juniper Networks" in output:
                                              ty = "Juniper"
                                          elif "Cisco" in output:
                                              ty = "Cisco"
                                          else:
                                              ty = "unknown"
                                          if ty == "Cisco":
                                              cmd1 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalDescr.1001"
                                              output1 = commands.getoutput(cmd1)
                                              if "STRING: " in output1:
                                                  list = output.split("Version", 1)
                                                  vers = ((list[1].split(",", 1))[0]).split()[0]
                                                  list1 = output1.split("STRING:", 1)
                                                  model = list1[1].strip()
                                                  if "Switch 1" in list1[1]:
                                                      list0 = output1.split(" Switch 1 -", 1)
                                                      model = (list0[1].split(" -", 1))[0]
                                                  if "odule" in list1[1]:
                                                      model = "c7609"
                                                  if "StackPort1/1" in list1[1]:
                                                      model = "WS-C3650-48TQ-S"
                                                  if "Port Container" in list1[1] or "Gigabit Ethernet Port" in list1[1]:
                                                      cmd4 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalDescr.1"
                                                      output4 = commands.getoutput(cmd4)
                                                      list4 = output4.split("Inc.", 1)
                                                      model = ((list4[1].split(" ", 2))[1]).split()[0]
                                                  list2 = output2.split(")", 1)
                                                  rundate = (list2[1].split(",", 1))[0]
                                              else:
                                                  cmd3 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalModelName.1"
                                                  output3 = commands.getoutput(cmd3)
                                                  if "STRING: " in output3:
                                                      list = output.split("Version", 1)
                                                      vers = ((list[1].split(",", 1))[0]).split()[0]
                                                      list3 = output3.split("STRING:", 1)
                                                      model = list3[1].strip()
                                                      list2 = output2.split(")", 1)
                                                      rundate = (list2[1].split(",", 1))[0]
                                                  else:
                                                      list = output.split("Version", 1)
                                                      vers = ((list[1].split(",", 1))[0]).split()[0]
                                                      model = data.Model
                                                      list2 = output2.split(")", 1)
                                                      rundate = (list2[1].split(",", 1))[0]
                                          elif ty == "Dell":
                                              list = output.split("Software Version:", 1)
                                              vers = ((list[1].split("\n", 1))[0]).split()[0]
                                              list1 = output.split("Series:", 1)
                                              model = ((list1[1].split("\n", 1))[0]).split()[0]
                                              list2 = output2.split(")", 1)
                                              rundate = (list2[1].split(",", 1))[0]
                                          elif ty == "Juniper":
                                              list = output.split("Inc.", 1)
                                              model = ((list[1].split(" ", 2))[1]).split()[0]
                                              list1 = output.split("JUNOS", 1)
                                              vers = ((list1[1].split(",", 1))[0]).split()[0]
                                              list2 = output2.split(")", 1)
                                              rundate = (list2[1].split(",", 1))[0]
                                          else:
                                              model = "unknown"
                                              vers = "unknown"
                                              rundate = "unknown"
                                              # print "ip" +ip + "name" + name
                                          if not (BackUp.objects.filter(IPAddress=ip) or (
                                                  BackUp.objects.filter(Name=name))):
                                              create = BackUp.objects.create(IPAddress=ip, Name=name, DU=du,
                                                                             Location=location, Type=ty, Online=True,
                                                                             Model=model, Version=vers,
                                                                             snmp_version=snmp,
                                                                             Community=community, Runtime=rundate)
                                              ipname = ip + " -- " + name + " -- " + ty + " -- " + model + " -- " + vers + " -- " + rundate
                                              print ipname
                                              sys.stdout.flush()
                                              success_num = success_num + 1
                                          else:
                                              BackUp.objects.filter(IPAddress=ip).update(snmp_version=snmp,
                                                                                         Community=community)
                                              repeat_num = repeat_num + 1
                                              print ip + " repeat"
                                              sys.stdout.flush()
                                      else:
                                          failed_num = failed_num + 1
                                          print ip + " failed"
                                          sys.stdout.flush()
                                  else:
                                      failed_num = failed_num + 1
                                      print ip + " failed"
                                      sys.stdout.flush()
                              else:
                                  failed_num = failed_num + 1
                                  print ip + " failed"
                                  sys.stdout.flush()

                          if snmp == "v3":
                              cmd0 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " SNMPv2-MIB::sysName"
                              output0 = commands.getoutput(cmd0)
                              if "STRING: " in output0:
                                  snmpsta = "ON"
                                  cmd = "snmpwalk -t 0.2 -v 3 -u" + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " SNMPv2-MIB::sysDescr"
                                  output = commands.getoutput(cmd)
                                  if "STRING: " in output:
                                      cmd2 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " DISMAN-EVENT-MIB::sysUpTimeInstance"
                                      output2 = commands.getoutput(cmd2)
                                      if "Timeticks: " in output2:
                                          sList = output0.split("STRING: ", 1)
                                          name = sList[1]
                                          if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name or ".tdlte.lab" in name:
                                              name = name[0:len(name) - 10]
                                          if "Application Software Version" in output and "Series" in output:
                                              ty = "Dell"
                                          elif "Juniper Networks" in output:
                                              ty = "Juniper"
                                          elif "Cisco" in output:
                                              ty = "Cisco"
                                          else:
                                              ty = "unknown"
                                          if ty == "Cisco":
                                              cmd1 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalDescr.1001"
                                              output1 = commands.getoutput(cmd1)
                                              if "STRING: " in output1:
                                                  list = output.split("Version", 1)
                                                  vers = ((list[1].split(",", 1))[0]).split()[0]
                                                  list1 = output1.split("STRING:", 1)
                                                  model = list1[1].strip()
                                                  if "Switch 1" in list1[1]:
                                                      list0 = output1.split(" Switch 1 -", 1)
                                                      model = (list0[1].split(" -", 1))[0]
                                                  if "odule" in list1[1]:
                                                      model = "c7609"
                                                  if "StackPort1/1" in list1[1]:
                                                      model = "WS-C3650-48TQ-S"
                                                  if "Port Container" in list1[1] or "Gigabit Ethernet Port" in list1[
                                                      1]:
                                                      cmd4 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalDescr.1"
                                                      output4 = commands.getoutput(cmd4)
                                                      list4 = output4.split("Inc.", 1)
                                                      model = ((list4[1].split(" ", 2))[1]).split()[0]
                                                  list2 = output2.split(")", 1)
                                                  rundate = (list2[1].split(",", 1))[0]
                                              else:
                                                  cmd3 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalModelName.1"
                                                  output3 = commands.getoutput(cmd3)
                                                  if "STRING: " in output3:
                                                      list = output.split("Version", 1)
                                                      vers = ((list[1].split(",", 1))[0]).split()[0]
                                                      list3 = output3.split("STRING:", 1)
                                                      model = list3[1].strip()
                                                      list2 = output2.split(")", 1)
                                                      rundate = (list2[1].split(",", 1))[0]
                                                  else:
                                                      list = output.split("Version", 1)
                                                      vers = ((list[1].split(",", 1))[0]).split()[0]
                                                      model = data.Model
                                                      list2 = output2.split(")", 1)
                                                      rundate = (list2[1].split(",", 1))[0]
                                          elif ty == "Dell":
                                              list = output.split("Software Version:", 1)
                                              vers = ((list[1].split("\n", 1))[0]).split()[0]
                                              list1 = output.split("Series:", 1)
                                              model = ((list1[1].split("\n", 1))[0]).split()[0]
                                              list2 = output2.split(")", 1)
                                              rundate = (list2[1].split(",", 1))[0]
                                          elif ty == "Juniper":
                                              list = output.split("Inc.", 1)
                                              model = ((list[1].split(" ", 2))[1]).split()[0]
                                              list1 = output.split("JUNOS", 1)
                                              vers = ((list1[1].split(",", 1))[0]).split()[0]
                                              list2 = output2.split(")", 1)
                                              rundate = (list2[1].split(",", 1))[0]
                                          else:
                                              model = "unknown"
                                              vers = "unknown"
                                              rundate = "unknown"
                                          # print "ip" + ip + " name" + name
                                          if not (BackUp.objects.filter(IPAddress=ip) or (
                                                  BackUp.objects.filter(Name=name))):
                                              create = BackUp.objects.create(IPAddress=ip, Name=name, DU=du,
                                                                             Location=location, Type=ty, Online=True,
                                                                             Model=model, Version=vers,
                                                                             snmp_version=snmp,
                                                                             Username=username, Password=password,
                                                                             Authority=authority,
                                                                             Authentication_protocol=subdata.Authentication_protocol,
                                                                             privacy_protocol=subdata.privacy_protocol,
                                                                             Passphase=subdata.Passphase,
                                                                             Runtime=rundate,Snmpv3=snmpsta)
                                              ipname = ip + " -- " + name + " -- " + ty + " -- " + model + " -- " + vers + " -- " + rundate
                                              print ipname
                                              sys.stdout.flush()
                                              success_num = success_num + 1
                                          else:
                                              BackUp.objects.filter(IPAddress=ip).update(snmp_version=snmp,
                                                                                         Username=username,
                                                                                         Password=password,
                                                                                         Authority=authority,
                                                                                         Authentication_protocol=subdata.Authentication_protocol,
                                                                                         privacy_protocol=subdata.privacy_protocol,
                                                                                         Passphase=subdata.Passphase,Snmpv3=snmpsta)
                                              repeat_num = repeat_num + 1
                                              print ip + " repeat"
                                              sys.stdout.flush()
                                      else:
                                          failed_num = failed_num + 1
                                          print ip + " failed"
                                          sys.stdout.flush()
                                  else:
                                      failed_num = failed_num + 1
                                      print ip + " failed"
                                      sys.stdout.flush()
                              else:
                                  failed_num = failed_num + 1
                                  print ip + " failed"
                                  sys.stdout.flush()

    print "Resault:"
    print "-----------------------------------"
    print "Success_num  " + str(success_num)
    print "Repeat_num  " + str(repeat_num)
    print "Failed_num  " + str(failed_num)
    print "-----------------------------------"
    sys.stdout.flush()

@shared_task
def delete_files():
    os.system('rm -f /home/code/management/console_delete.txt')
    console_log = open('console_delete.txt', 'ab+')
    sys.stdout = console_log
    os.system('find /root/backup -mtime +30 -name "*.txt" -exec rm -rf {} \;')
    #cmd = 'find /root/backup -mtime +30 -name "*.txt" -exec rm -rf {} \;'
    #output = commands.getoutput(cmd)
    print 'Delete Done'
    sys.stdout.flush()

@shared_task
def get_Info_snmp():
    os.system('rm -f /home/code/management/console_Info_snmp_ALL.txt')
    console_log = open('console_Info_snmp_ALL.txt', 'ab+')
    sys.stdout = console_log
    list = BackUp.objects.all()
    num = 0
    print "-----------------------------------------------------"
    sys.stdout.flush()
    for data in list:
        num = num + 1
        print num
        ip = str(data.IPAddress)
        ty = str(data.Type)
        model = str(data.Model)
        vers = str(data.Version)
        snmp = str(data.snmp_version)
        community = str(data.Community)
        username = str(data.Username)
        password = str(data.Password)
        authority = str(data.Authority)
        authenproto = " -a " + str(data.Authentication_protocol)
        pripro = " -x " + str(data.privacy_protocol)
        passphase =" -X " + str(data.Passphase)
        if str(data.Authentication_protocol) == "None" or str(data.Authentication_protocol) == "":
            authenproto = ""
        if str(data.privacy_protocol) == "None" or str(data.privacy_protocol) == "":
            pripro = ""
        if str(data.Passphase) == "None" or str(data.Passphase) == "":
            passphase = ""
        if snmp == "None":
            print ip + " snmp miss"
            print "----------------------------------------------------------" + '\n'
            sys.stdout.flush()
        if snmp == "v2c":
            flag = True
            if community == "None":
                print ip + " snmpv2 infor miss"
                print "----------------------------------------------------------" + '\n'
                sys.stdout.flush()
                flag = False
            if flag:
                cmd = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " SNMPv2-MIB::sysName"
                output0 = commands.getoutput(cmd)
                if "STRING: " in output0:
                    cmd0 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " SNMPv2-MIB::sysDescr"
                    output = commands.getoutput(cmd0)
                    if "STRING: " in output:
                        cmd2 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " DISMAN-EVENT-MIB::sysUpTimeInstance"
                        output2 = commands.getoutput(cmd2)
                        if "Timeticks: " in output2:
                            sList = output0.split("STRING: ", 1)
                            name = sList[1]
                            if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name or ".tdlte.lab" in name:
                                name = name[0:len(name) - 10]
                            if "Application Software Version" in output and "Series" in output:
                                ty = "Dell"
                            elif "Juniper Networks" in output:
                                ty = "Juniper"
                            elif "Cisco" in output:
                                ty = "Cisco"
                            else:
                                ty = "unknown"
                            if ty == "Cisco":
                                cmd1 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalDescr.1001"
                                output1 = commands.getoutput(cmd1)
                                if "STRING: " in output1:
                                    list = output.split("Version", 1)
                                    vers = ((list[1].split(",", 1))[0]).split()[0]
                                    list1 = output1.split("STRING:", 1)
                                    model = list1[1].strip()
                                    if "Switch 1" in list1[1]:
                                        list0 = output1.split(" Switch 1 -", 1)
                                        model = (list0[1].split(" -", 1))[0]
                                    if "odule" in list1[1]:
                                        model = "c7609"
                                    if "StackPort1/1" in list1[1]:
                                        model = "WS-C3650-48TQ-S"
                                    if "Port Container" in list1[1] or "Gigabit Ethernet Port" in list1[1]:
                                        cmd4 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalDescr.1"
                                        output4 = commands.getoutput(cmd4)
                                        list4 = output4.split("Inc.", 1)
                                        model = ((list4[1].split(" ", 2))[1]).split()[0]
                                    list2 = output2.split(")", 1)
                                    rundate = (list2[1].split(",", 1))[0]
                                else:
                                    cmd3 = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " ENTITY-MIB::entPhysicalModelName.1"
                                    output3 = commands.getoutput(cmd3)
                                    if "STRING: " in output3:
                                        list = output.split("Version", 1)
                                        vers = ((list[1].split(",", 1))[0]).split()[0]
                                        list3 = output3.split("STRING:", 1)
                                        model = list3[1].strip()
                                        list2 = output2.split(")", 1)
                                        rundate = (list2[1].split(",", 1))[0]
                                    else:
                                        list = output.split("Version", 1)
                                        vers = ((list[1].split(",", 1))[0]).split()[0]
                                        model = data.Model
                                        list2 = output2.split(")", 1)
                                        rundate = (list2[1].split(",", 1))[0]
                            elif ty == "Dell":
                                list = output.split("Software Version:", 1)
                                vers = ((list[1].split("\n", 1))[0]).split()[0]
                                list1 = output.split("Series:", 1)
                                model = ((list1[1].split("\n", 1))[0]).split()[0]
                                list2 = output2.split(")", 1)
                                rundate = (list2[1].split(",", 1))[0]
                            elif ty == "Juniper":
                                list = output.split("Inc.", 1)
                                model = ((list[1].split(" ", 2))[1]).split()[0]
                                list1 = output.split("JUNOS", 1)
                                vers = ((list1[1].split(",", 1))[0]).split()[0]
                                list2 = output2.split(")", 1)
                                rundate = (list2[1].split(",", 1))[0]
                            else:
                                model = "unknown"
                                vers = "unknown"
                                rundate = "unknown"
                                # print "ip" +ip + "name" + name
                            print ip + " success"
                            print "----------------------------------------------------------" + '\n'
                            sys.stdout.flush()
                            BackUp.objects.filter(IPAddress=ip).update(Name=name, Type=ty, Online=True, Model=model,
                                                                       Version=vers, Runtime=rundate)
                        else:
                            print ip + " failed"
                            print "----------------------------------------------------------" + '\n'
                            sys.stdout.flush()
                    else:
                        print ip + " failed"
                        print "----------------------------------------------------------" + '\n'
                        sys.stdout.flush()
                else:
                    print ip + " failed"
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()

        if snmp == "v3":
            flag = True
            if username == "None" or password == "None" or authority == "None":
                print ip + " snmpv3 infor miss"
                print "----------------------------------------------------------" + '\n'
                sys.stdout.flush()
                flag = False
            if flag:
                cmd0 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " SNMPv2-MIB::sysName"
                output0 = commands.getoutput(cmd0)
                if "STRING: " in output0:
                    snmpsta = "ON"
                    cmd = "snmpwalk -t 0.2 -v 3 -u" + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " SNMPv2-MIB::sysDescr"
                    output = commands.getoutput(cmd)
                    if "STRING: " in output:
                        cmd2 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " DISMAN-EVENT-MIB::sysUpTimeInstance"
                        output2 = commands.getoutput(cmd2)
                        if "Timeticks: " in output2:
                            sList = output0.split("STRING: ", 1)
                            name = sList[1]
                            if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name or ".tdlte.lab" in name:
                                name = name[0:len(name) - 10]
                            if "Application Software Version" in output and "Series" in output:
                                ty = "Dell"
                            elif "Juniper Networks" in output:
                                ty = "Juniper"
                            elif "Cisco" in output:
                                ty = "Cisco"
                            else:
                                ty = "unknown"
                            if ty == "Cisco":
                                cmd1 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalDescr.1001"
                                output1 = commands.getoutput(cmd1)
                                if "STRING: " in output1:
                                    list = output.split("Version", 1)
                                    vers = ((list[1].split(",", 1))[0]).split()[0]
                                    list1 = output1.split("STRING:", 1)
                                    model = list1[1].strip()
                                    if "Switch 1" in list1[1]:
                                        list0 = output1.split(" Switch 1 -", 1)
                                        model = (list0[1].split(" -", 1))[0]
                                    if "odule" in list1[1]:
                                        model = "c7609"
                                    if "StackPort1/1" in list1[1]:
                                        model = "WS-C3650-48TQ-S"
                                    if "Port Container" in list1[1] or "Gigabit Ethernet Port" in list1[1]:
                                        cmd4 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalDescr.1"
                                        output4 = commands.getoutput(cmd4)
                                        list4 = output4.split("Inc.", 1)
                                        model = ((list4[1].split(" ", 2))[1]).split()[0]
                                    list2 = output2.split(")", 1)
                                    rundate = (list2[1].split(",", 1))[0]
                                else:
                                    cmd3 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " ENTITY-MIB::entPhysicalModelName.1"
                                    output3 = commands.getoutput(cmd3)
                                    if "STRING: " in output3:
                                        list = output.split("Version", 1)
                                        vers = ((list[1].split(",", 1))[0]).split()[0]
                                        list3 = output3.split("STRING:", 1)
                                        model = list3[1].strip()
                                        list2 = output2.split(")", 1)
                                        rundate = (list2[1].split(",", 1))[0]
                                    else:
                                        list = output.split("Version", 1)
                                        vers = ((list[1].split(",", 1))[0]).split()[0]
                                        model = data.Model
                                        list2 = output2.split(")", 1)
                                        rundate = (list2[1].split(",", 1))[0]
                            elif ty == "Dell":
                                list = output.split("Software Version:", 1)
                                vers = ((list[1].split("\n", 1))[0]).split()[0]
                                list1 = output.split("Series:", 1)
                                model = ((list1[1].split("\n", 1))[0]).split()[0]
                                list2 = output2.split(")", 1)
                                rundate = (list2[1].split(",", 1))[0]
                            elif ty == "Juniper":
                                list = output.split("Inc.", 1)
                                model = ((list[1].split(" ", 2))[1]).split()[0]
                                list1 = output.split("JUNOS", 1)
                                vers = ((list1[1].split(",", 1))[0]).split()[0]
                                list2 = output2.split(")", 1)
                                rundate = (list2[1].split(",", 1))[0]
                            else:
                                model = "unknown"
                                vers = "unknown"
                                rundate = "unknown"
                            # print "ip" + ip + " name" + name
                            print ip + " success"
                            print "----------------------------------------------------------" + '\n'
                            sys.stdout.flush()
                            BackUp.objects.filter(IPAddress=ip).update(Name=name, Type=ty, Online=True, Model=model,
                                                                       Version=vers, Runtime=rundate,Snmpv3=snmpsta)
                        else:
                            BackUp.objects.filter(IPAddress=ip).update(Snmpv3=snmpsta)
                            print ip + " failed"
                            print "----------------------------------------------------------" + '\n'
                            sys.stdout.flush()
                    else:
                        BackUp.objects.filter(IPAddress=ip).update(Snmpv3=snmpsta)
                        print ip + " failed"
                        print "----------------------------------------------------------" + '\n'
                        sys.stdout.flush()
                else:
                    snmpsta = "OFF"
                    BackUp.objects.filter(IPAddress=ip).update(Snmpv3=snmpsta)
                    print ip + " failed"
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()
        else:
            snmpsta = "UNSET"
            BackUp.objects.filter(IPAddress=ip).update(Snmpv3=snmpsta)


@shared_task
def get_Name_snmp():
    os.system('rm -f /home/code/management/console_Name_snmp_ALL.txt')
    console_log = open('console_Name_snmp_ALL.txt', 'ab+')
    sys.stdout = console_log
    list = BackUp.objects.all()
    num = 0
    print "-----------------------------------------------------"
    sys.stdout.flush()
    for data in list:
        num = num + 1
        print num
        ip = str(data.IPAddress)
        ty = str(data.Type)
        model = str(data.Model)
        vers = str(data.Version)
        snmp = str(data.snmp_version)
        community = str(data.Community)
        username = str(data.Username)
        password = str(data.Password)
        authority = str(data.Authority)
        authenproto = " -a " + str(data.Authentication_protocol)
        pripro = " -x " + str(data.privacy_protocol)
        passphase =" -X " + str(data.Passphase)
        if str(data.Authentication_protocol) == "None" or str(data.Authentication_protocol) == "":
            authenproto = ""
        if str(data.privacy_protocol) == "None" or str(data.privacy_protocol) == "":
            pripro = ""
        if str(data.Passphase) == "None" or str(data.Passphase) == "":
            passphase = ""
        if snmp == "None":
            print ip + " snmp miss"
            print "----------------------------------------------------------" + '\n'
            sys.stdout.flush()
        if snmp == "v2c":
            flag = True
            if community == "None":
                print ip + " snmpv2 infor miss"
                print "----------------------------------------------------------" + '\n'
                sys.stdout.flush()
                flag = False
            if flag:
                cmd = "snmpwalk -t 0.2 -v 2c -c " + community + " " + ip + " SNMPv2-MIB::sysName"
                # print cmd
                output = commands.getoutput(cmd)
                # print output
                if "STRING: " in output:
                    sList = output.split("STRING: ", 1)
                    name = sList[1]
                    if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name:
                        name = name[0:len(name) - 10]
                    print ip + " " + name
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()
                    BackUp.objects.filter(IPAddress=ip).update(Name=name)
                else:
                    print ip + " failed"
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()

        if snmp == "v3":
            flag = True
            if username == "None" or password == "None" or authority == "None":
                print ip + " snmpv3 infor miss"
                print "----------------------------------------------------------" + '\n'
                sys.stdout.flush()
                flag = False
            if flag:
                cmd = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + authenproto + pripro + passphase + " " + ip + " SNMPv2-MIB::sysName"
                # print cmd
                output = commands.getoutput(cmd)
                # print output
                if "STRING: " in output:
                    sList = output.split("STRING: ", 1)
                    name = sList[1]
                    if ".cisco.com" in name or ".ltetp.net" in name or ".nokia.com" in name or ".tdlte.lab" in name:
                        name = name[0:len(name) - 10]
                    print ip + " " + name
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()
                    BackUp.objects.filter(IPAddress=ip).update(Name=name)
                else:
                    print ip + " failed"
                    print "----------------------------------------------------------" + '\n'
                    sys.stdout.flush()
