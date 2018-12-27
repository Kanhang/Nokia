# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from djcelery.models import PeriodicTask
from django.contrib import admin
import commands
import sys
from switch.backup import starting_backup
from django.db import models
from django.forms import ModelForm
from django.core.mail import send_mail
from django.conf import settings
from .models import BackUp
import os,stat,re,time
from switch.backup import log_summary

from django.utils.safestring import mark_safe
from djcelery.models import(
    TaskState, WorkerState,
    PeriodicTask, IntervalSchedule, CrontabSchedule,
    PeriodicTasks
)
from djcelery.admin import PeriodicTaskAdmin, PeriodicTaskForm
# Register your models here.
# copy the admin from djcelery, and change the information if a differentiated page view is requested

# abitarily modify the admin will trigger unexpected errors exp: cannot register tasks
# alert registered will not able to be modified because it does not allow task to be register
'''class PeriodicTaskAdmin(admin.ModelAdmin):
    form = PeriodicTaskForm
    model = PeriodicTask
    list_display = (
        'enabled',
        'name',
        '__unicode__',

    )
    search_fields = ('name', 'task')
    list_display_links = ('enabled', '__unicode__')
    ordering = ('-enabled', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask',  'enabled'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab'),
            'classes': ('extrapretty', 'wide', ),
        }),

    )
    actions = ['enable_tasks',
               'disable_tasks']
'''
def backUpselected(self,request,queryset):
    os.system('rm -f /home/code/management/console_back.txt')
    console_log=open('console_back.txt','ab+')
    sys.stdout=console_log
    #queryset.update(BackupFailed="")
    settings.UNDOWNLOADABLE_IP = []
    print "backup task"
    sys.stdout.flush()
    sys.stdout.flush()
    error = 0
    num = 0
    # Backup_failure=[]
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    local_time2 = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    log = open('/home/backup/backup_log.txt', 'a+')  # add new to the file and create file if it does not exist
    ret = os.system("echo backup Start > /home/backup/backup_log.txt")  # found

    log.write(local_time + '\n')
    log.write("------------------------------------------------------------------------------" + '\n')
    print "------------------------------------------------------------------------------" + '\n'
    sys.stdout.flush()
    qs = queryset
    for data in qs:
        ip = data.IPAddress
        type = data.Type
        du = data.DU
        loc = data.Location

        sys.stdout.flush()
        num = num + 1
        print num
        sys.stdout.flush()
        numfile = open('/home/backup/count.txt', 'wb')  # found
        numfile.write(str(num))
        numfile.close()

        reg = "^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$"  # to match ip Address
        if not re.match(reg, ip):
            log.write('Incorrect IP address ' + ip + '\n')
            print 'Incorrect IP address ' + ip + '\n'
            sys.stdout.flush()
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
                #data.BackupFailed = ""
                #data.save()
                BackUp.objects.filter(IPAddress=ip).update(Last_backup_date = local_time2)
                BackUp.objects.filter(IPAddress=ip).update(BackupFailed = "Backupsucceed")
                print ip + ' backup Complete!'
                sys.stdout.flush()
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
    print "------------------------------------------------------------------------------" + '\n'
    sys.stdout.flush()
    log.write('finished!\n')
    print 'finished!\n'
    sys.stdout.flush()

    if error > 0:
        log.write('Total Failed: ' + str(error) + '\n')
        print 'Total Failed: ' + str(error) + '\n'
        sys.stdout.flush()
    else:
        log.write('backup Complete!\n\n')
        print 'backup Complete!\n\n'
        sys.stdout.flush()

    log.close()
    log_summary()





def checkingSelectedName(self, request, queryset):
    os.system('rm -f /home/code/management/console_Name.txt')
    console_log=open('console_Name.txt','ab+')
    sys.stdout=console_log
    num = 0
    print 'Starting check switch name'
    sys.stdout.flush()
    base_path = os.getcwd()
    list = queryset
    path = "/root/name/"
    for data in list:
        ip = data.IPAddress
        type = data.Type
        file = "/home/code/management/static/admin/template/dee.sh"
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
            print "----------------------------------------------------------" + '\n'
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

def ping(self, request, queryset):
    os.system('rm -f /home/code/management/console_ping.txt')
    console_log = open('console_ping.txt', 'ab+')
    sys.stdout = console_log
    sys.stdout.flush()
    num = 0
    list=queryset
    for data in list:
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



def checkingSelectedInfo(self, request, queryset):
    os.system('rm -f /home/code/management/console_Info.txt')
    console_log = open('console_Info.txt', 'ab+')
    sys.stdout = console_log
    num = 0
    print 'Starting check switch information'
    sys.stdout.flush()
    base_path = os.getcwd()
    list = queryset
    path = "/root/name/"
    for data in list:
        ip = data.IPAddress
        type = data.Type
        file = "/home/code/management/static/admin/template/dee.sh"
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


def getInfosnmp(self, request, queryset):
    os.system('rm -f /home/code/management/console_Info_snmp.txt')
    console_log = open('console_Info_snmp.txt', 'ab+')
    sys.stdout = console_log
    list = queryset
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
                                print "list"
                                print list
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



def getNamesnmp(self, request, queryset):
    os.system('rm -f /home/code/management/console_Name_snmp.txt')
    console_log = open('console_Name_snmp.txt', 'ab+')
    sys.stdout = console_log
    list = queryset
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




class BackUpAdmin(admin.ModelAdmin):

    list_display = ('IPAddress', 'Name', 'Stdname','Type','Model','Version','DU','Location', 'Downloadable','Last_backup_date', 'Online','colored_Snmpv3','Runtime',)# 'method name' can reference to a method
    list_per_page = 50
    search_fields = ['IPAddress' , 'Name', 'Type' , 'DU' , 'Location']
    change_list_template = "my_change_list.html"
    list_filter = ['DU', 'Type', 'Model','Location', 'BackupFailed','Last_backup_date','Online','Stdname','Snmpv3']
    readonly_fields = ('Name','Type','Model','Version','Last_backup_date', 'BackupFailed','Online','Stdname','Runtime','Snmpv3',) #let field become read-only
    fieldsets = [
                (None,	{'fields':['IPAddress', 'Name', 'Stdname','Type','Model','Version','DU','Location','Last_backup_date', 'BackupFailed','Online','Snmpv3','Runtime']}),
                ('Snmp info',{'fields':['snmp_version','Community','Username','Password','Authority','Authentication_protocol','privacy_protocol','Passphase'],'classes':['collapse']})
                ]
    ordering = ('DU',)
    actions= [checkingSelectedInfo,getInfosnmp,checkingSelectedName,getNamesnmp,ping,backUpselected]

    def Downloadable(self, obj):
     ip= obj.IPAddress
     # type=obj.Type
     # du= obj.DU
     #
     # loc= obj.Location
     if not ip:
         ip=""
     # if not type:
     #     type=""
     # if not du:
     #     du=""
     # if not loc:
     #     loc=""
     # path = "/root/backup/" + loc + "/" + du + "/" + type + "/" + ip
     path = "/root/backup/" + ip
     if os.path.exists(path) and os.listdir(path):
        #if ip in settings.UNDOWNLOADABLE_IP:

         # settings.UNDOWNLOADABLE_IP.remove(ip)
         # return mark_safe('<a href="/downloadzip/{Location}/{DU}/{Type}/{IP}/">Download</a>'.format(Location=loc,DU=du,Type=type,IP=ip))
         return mark_safe('<a href="/downloadzip/{IP}/">Download</a>'.format(IP=ip))
     else:
          settings.UNDOWNLOADABLE_IP.append(ip)
          return "-"
          '''# backup=BackUp.objects.get(IPAddress=ip,Type= type,DU=du,Location=loc)
          # if backup:
          #   backup.downloadable = "Download"
          #  backup.save()
          # backup=BackUp.objects.get(IPAddress=ip, Type=type, DU=du, Location=loc)
          # backup.downloadable = "-"
          #  backup.save()'''
backUpselected.short_description="Backup selected switches"
checkingSelectedName.short_description="Get NAME for the selected by telnet"
getNamesnmp.short_description="Get NAME for the selected by snmp "
checkingSelectedInfo.short_description="Get INFO for the selected by telnet"
getInfosnmp.short_description="Get INFO for the selected by snmp"
ping.short_description="Get ONLINE for the selected "
admin.site.site_header = "BACKUP"
admin.site.index_template
admin.site.register(BackUp,BackUpAdmin)

#admin.site.unregister(PeriodicTask.interval)
admin.site.unregister(PeriodicTask) #unregister first, and then register again
admin.site.register(PeriodicTask, PeriodicTaskAdmin)


