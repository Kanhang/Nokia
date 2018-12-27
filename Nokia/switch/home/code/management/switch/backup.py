import commands
import time
from django.utils.safestring import mark_safe
import os, time, sys, stat
import re, sys, paramiko
from openpyxl import Workbook
from openpyxl import load_workbook
from .models import BackUp
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render_to_response


def starting_backup(ip, type ,du , loc):
    console_log = open('console_back.txt', 'ab+')
    sys.stdout = console_log
    print "--------------------------------------------------------------------------------------" + '\n'
    print "Starting check switch information"
    sys.stdout.flush()
    if type=="" or ip=="" :
        print "Information miss"
        sys.stdout.flush()
        return False

    else:
        print "Checking infor success"
        sys.stdout.flush()
    print "Starting check switch status"
    sys.stdout.flush()
    output = commands.getoutput("nmap -p 23 "+ip+" -n")
    #print output
    if "Host is up" in output and "open" in output:
        print ip+" Port 23 open"
        sys.stdout.flush()
    else:
        print ip+" Port 23 closed"
        sys.stdout.flush()
        return False
    print "Starting Backup process"
    sys.stdout.flush()
    path = "/root/backup/" +ip
    mkdir(path)
    os.system("chmod 777 -R /root/backup")
    file1 = locate_file(type)
    #print file1
    file2 = path
    test = "/home/code/management/static/admin/template/"
    arr = os.listdir(test)
    #print arr
    if replace_str(file1, ip, file2):
        return True
    else:
        return False


def locate_file(type):
    if type == 'Cisco':
        file1 = "/home/code/management/static/admin/template/cisco-backup.sh"
    elif type == 'Juniper':
        file1 = "/home/code/management/static/admin/template/juniper-backup.sh"
    elif type == 'Dell':
        file1 = "/home/code/management/static/admin/template/dell-backup.sh"
    return file1


def replace_str(file1, ip, file2):
    console_log = open('console_back.txt', 'ab+')
    sys.stdout = console_log
    base_path = os.getcwd()
    #print "base_directory: " + base_path
    f1 = open(file1, "r")
    #print "file2:" + file2
    os.chdir(file2)
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    #print "local_time" + local_time
    f2 = open("%s.sh" % file2, "w")
    #print 'successful'
    for line in f1:
            if "xx.xx.xx.xx" in line:
                line = line.replace("xx.xx.xx.xx", ip)
            if "date" in line:
                line = line.replace("date", local_time)
            f2.write(line)
    os.rename('%s.sh' % file2, ip+".sh")
    cmd = file2 + '/' + ip + '.sh'
    f1.close()
    f2.close()
    os.chmod(cmd, stat.S_IXOTH)
    print "begin execute..."
    sys.stdout.flush()    
    output = commands.getoutput(cmd)
    print output
    sys.stdout.flush()
    os.system('rm -rf ' + cmd)
    os.chdir(base_path)
    if 'error' in output:
        print ip + " Authorization failed"
        sys.stdout.flush()
        return False
    elif 'Error' in output:
        print ip + " Authorization failed"
        sys.stdout.flush()
        return False
    elif 'executing' in output:
        print ip + " executing error"
        sys.stdout.flush()
        return False
    elif 'Authorization failed.' in output:
        print ip + " Authorization failed"
        sys.stdout.flush()
        return False
    elif 'invalid' in output:
        print ip + " Authorization failed"
        sys.stdout.flush()
        return False
    elif 'Transfer complete' not in output:    # nested if sentences to determine the key words
        if 'successfully copied' not in output:
            if 'copied' not in output:
                return False
    return True



def log_summary():
    path = "/home/backup/backup_log.txt"
    with open(path, 'rb+') as f:
        lines = f.readlines()
    print ("log_summary")
    log = open('/home/backup/log_summary.txt', 'ab+') #  b is the way to input number
    for line in lines:
        print line
        log.write(line)
    log.write("\n")
    log.close()


def mkdir(path):
    console_log = open('console_back.txt', 'ab+')
    sys.stdout = console_log
    path = path.strip()

    existed = os.path.exists(path)

    if not existed:
        os.makedirs(path)
        print 'creating backup path...'
        print 'Path created'
        sys.stdout.flush()
        return True
    else:
        print 'creating backup path...'
        print 'Path existed'
        sys.stdout.flush()
'''
1.add all logs to get the biggest one and read the biggest one
2.create 7 areas day1 :  day2 : if day1 is null write into day2  weak points hard to maintainance
def add_log(file):
    for not file.read()

'''

def transmit(request):
    f = open('/home/backup/log_summary.txt', 'rb+')

    lines = f.readlines()
    str = ""
    for line in lines:
        str += line
        str += "<br>"

    return render(request,"log_summary.html",{"string": mark_safe(str)}) #prevent from auto-escape