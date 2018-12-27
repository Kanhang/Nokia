# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import BackUp
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse
import xlrd, xlwt, os, time, re
from django.conf import settings
import paramiko
from django.db import transaction
from django.db import connection, transaction
import StringIO
from data.models import food
from switch.models import BackUp
from brand.models import brand
from abnormal.models import abnormal
from celery.task.control import revoke
from switch.zip import ZipUtilities
from django.db import connection, transaction
from switch.tasks import command_backup,cron_delete
#from switch.tasks import rename, command_config, command_backup,cron_delete,ping_IPAddress,get_Info,get_Name,save_data,save_brand
import commands
import json
import datetime
import copy
import traceback
from data.models import food
from pageview.models import page

# Create your views here.
# the undownloadable_ip will append on the envir_variable IP
# when backup task starts, it can modify the IPADDRESS
'''def sort_undownloadable(request):

    list = settings.UNDOWNLOADABLE_IP

    for i in range(0,len(list)):
     try:
       print list[i]
       record= BackUp.objects.get(IPAddress=list[i])
       record.undownloadable = "unavailable"

       record.save()

     except Exception , e:
       print "Error message:"+e.message
       pass
    unavalist=BackUp.objects.filter(undownloadable="unavailable")
    for k in range(0,len(unavalist)):
       if not unavalist[k].IPAddress in list:
           unavalist[k].undownloadable = "available"
           unavalist[k].save()
    return HttpResponseRedirect('/admin/switch/backup/?undownloadable=unavailable')'''

   # return HttpResponseRedirect('/admin/switch/backup/')







def convert_to_dict(obj):
  
  dict = {}
  dict.update(obj.__dict__)
  return dict

def alarm(request):
    qs = BackUp.objects.all()
    errorList=[]
    for data in qs:
        IPAddress=data.IPAddress
        name=data.Name
        brand=data.Model
        du=data.DU
        loc=data.Location
        alarm=""
        if data.BackupFailed =="Backupfailed":
            alarm=alarm+"Backupfailed\n"
        if data.Online==False:
            alarm=alarm+"Onffline\n"
        if data.Stdname==False:
            alarm=alarm+"Nonstandard\n"
        if not alarm=="":
          newData= BackUp(IPAddress=IPAddress,Name=name,Model=brand,DU=du,Location=loc,Note=alarm)
          json_str=newData.toJSON()
          dictio= json.loads(json_str)
          print dictio
          errorList.append(dictio)
    return render(request,"Alarm.html",{"errorList":errorList})

def export(request):
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_name = 'data_'+local_time+'.xls'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    wb = xlwt.Workbook(encoding="utf-8")
    sheet = wb.add_sheet(u'data')
    headers = ['IP ADDRESS', 'NAME', 'TYPE', 'DU', 'LOCATION']
    for i in range(0, len(headers)):
        sheet.write(0, i, headers[i])
    row = 1
    for k in BackUp.objects.all():
        sheet.write(row, 0, k.IPAddress)
        sheet.write(row, 1, k.Name)
        sheet.write(row, 2, k.Type)
        sheet.write(row, 3, k.DU)
        sheet.write(row, 4, k.Location)
        row = row+1
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response




'''def writePath(request):
    for data in BackUp.objects.all():
        ip = data.IPAddress
        type = data.Type
        du = data.DU
        location = data.Location
        mypath = "/root/backup/"+location+"/"+du + "/" + type + "/" + ip
        if os.path.exists(mypath):
            data.path = mypath
            print mypath
        data.save()
    return HttpResponseRedirect('/admin/switch/backup/')
'''

def downloadzip(request, IP):
    path = "/root/backup/" + IP+"/"
    utilities = ZipUtilities()
    #print "path is" + path
    if os.path.exists(path):
        #print("yes")   #mark cannot print cannot identify the path
        list = os.listdir(path)
        #print list
        for i in range(0, len(list)):
                newpath = os.path.join(path, list[i])
                filename = os.path.basename(newpath)
                utilities.toZip(newpath, filename)
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attatchment;filename= "{0}"'.format(IP+".zip")
    return response

def testo():
    testa = test.delay()
    return HttpResponse('ok')

def datetime_offset_by_month(datetime1, n):

    # create a shortcut object for one day
    one_day = datetime.timedelta(days = 1)

    # first use div and mod to determine year cycle
    q,r = divmod(datetime1.month + n, 12)

    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day

    if datetime1.month != (datetime1 + one_day).month:
        return datetime2


    if datetime1.day >= datetime2.day:
        return datetime2

    return datetime2.replace(day = datetime1.day)


def date_traverse(monstr,num):
    #print "monstr[0]                        "+ monstr
    list=monstr.split("-",1)
    year=int(list[0])
    #print "monstr[1]                         "+monstr[1]
    month=int(list[1])
    #print "month                        "+str(month)
    d1=datetime.datetime(year,month,1)

    d2=datetime_offset_by_month(d1,num)
    new_date=str(d2).split(" ",1)
    new_str=(new_date[0])[0:7]
    return new_str

def tools(request):
    return render(request,'Tools.html')
def area_chart():
    abnor={}
    abnormal_list=[]
    date_list=[]
    #today= datetime.date.today()
    #final=today+datetime.timedelta(-7)

    qs= abnormal.objects.all()
    if not qs:
        final=datetime.date.today()
        final = final.strftime('%Y-%m-%d')
    else:
        for data in qs:
            date_list.append(data.date)
        value = max(date_list, key=lambda x: (x))
        #print value
        final = datetime.datetime.strptime(value, '%Y-%m-%d')
        final = final.strftime('%Y-%m-%d')
        #print "final******   "+final
    hope=""
    for i in range(0,6):
        if not abnormal.objects.filter(date=final):
             abnormal.objects.create(date=final,offline='0',bkfailed='0',nonstandard='0')
        #print final
        final=datetime.datetime.strptime(final,'%Y-%m-%d')+datetime.timedelta(-1)
        final = final.strftime('%Y-%m-%d')
        hope=final
    #print hope+"final"
    #print "final"+hope
    qs= abnormal.objects.filter(date__gte=final)
    temp_dict={}
    for data in qs:
        #print data
        temp_dict["period"]= data.date
        temp_dict['offline']=data.offline
        temp_dict['backupfailed']=data.bkfailed
        temp_dict['n-stdname']=data.nonstandard
        abnormal_list.append(temp_dict)
        temp_dict=copy.deepcopy(abnor)

    #print abnormal_list
    return abnormal_list

def transfer_page(request):
    page_obj=page.objects.get(id=1)
    page_obj.refresh_count+=1
    page_obj.save()
    return HttpResponseRedirect("http://10.110.23.254")
def index(request):
    sum= BackUp.objects.all().count()
    success=BackUp.objects.filter(BackupFailed="Backupsucceed").count()
    online=BackUp.objects.filter(Online="True").count()
    big_list=line_chart()
    type_list=bar_chart()
    total=formatting(big_list)
    final_list=total[0]
    ykeys=total[1]
    labels=total[2]
    total_type=type_formatting(type_list)
    final_type=total_type[0]
    ykeys_type=total_type[1]
    labels_type=total_type[2]
    dulist=pie_chart()
    abnormal_list=area_chart()
    table=data_table()
    
    page_obj = page.objects.get(id=1)
    page_obj.page_index_count = page_obj.page_index_count  + int(1)
    page_obj.save()
    
    return render(request, 'index.html', {'total':sum, 'success':success,
                                         'online':online,'list': json.dumps(final_list),
                                         'ykeys':json.dumps(ykeys),
                                         'labels':json.dumps(labels),'dulist':json.dumps(dulist),
                                         'final_type': json.dumps(final_type), 'ykeys_type': json.dumps(ykeys_type),
                                         'labels_type': json.dumps(labels_type),'abnormal_list':json.dumps(abnormal_list),
                                          'data_table':table,
                                          })

def type_formatting(big_list):
    labels = []
    for list in big_list:
        for sub_list in list:
            if not sub_list[1] in labels:
                labels.append(sub_list[1])
    #print labels
    seq = ['y', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'z']
    ykeys = seq[0:len(labels) + 1]
    #print ykeys
    final_list = []
    ykeys_to_labels = {}
    for k in range(1, len(ykeys)):
        ykeys_to_labels[ykeys[k]] = labels[k - 1]
    #print "ykeys_to_labels"
    #print ykeys_to_labels
    labels_to_ykeys = {}
    for key in ykeys_to_labels:
        labels_to_ykeys[ykeys_to_labels[key]] = key
    #print "labels_to_ykeys"
    #print labels_to_ykeys
    # build a reversed dict
    default_dict = {}
    for k in range(0, len(ykeys)):
        default_dict[ykeys[k]] = 0
    #print "default_dict"
    #print default_dict
    temp_dict = copy.deepcopy(default_dict)
    # dict is an object. Simply initiate it to another value  wont create the new object,but only update the attrivute of object
    for list in big_list:
        for sub_list in list:
            temp_dict['y'] = sub_list[0]
            if labels_to_ykeys[sub_list[1]]:
                if sub_list[2]:
                    temp_dict[labels_to_ykeys[sub_list[1]]] = sub_list[2]
       # print "temp_dict"
        #print temp_dict
        final_list.append(temp_dict)
        #print final_list
        temp_dict = copy.deepcopy(default_dict)
    #print "final_list"
    #print final_list
    final_list.sort(reverse=False)
    total=[]
    total.append(final_list)
    ykeys=ykeys[1:len(ykeys)]
    total.append(ykeys)
    total.append(labels)
    return total




def formatting(big_list):
    labels = []
    for list in big_list:
        for sub_list in list:
            if not sub_list[1] in labels:
                labels.append(sub_list[1])
    #print labels
    seq = ['y', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'z']
    ykeys = seq[0:len(labels) + 1]
    #print ykeys
    final_list = []
    ykeys_to_labels = {}
    for k in range(1, len(ykeys)):
        ykeys_to_labels[ykeys[k]] = labels[k - 1]
    #print "ykeys_to_labels"
    #print ykeys_to_labels
    labels_to_ykeys = {}
    for key in ykeys_to_labels:
        labels_to_ykeys[ykeys_to_labels[key]] = key
    #print "labels_to_ykeys"
    #print labels_to_ykeys
    # build a reversed dict
    default_dict = {}
    for k in range(0, len(ykeys)):
        default_dict[ykeys[k]] = 0
    #print "default_dict"
    #print default_dict
    temp_dict = copy.deepcopy(default_dict)
    # dict is an object. Simply initiate it to another value  wont create the new object,but only update the attrivute of object
    for list in big_list:
        for sub_list in list:
            temp_dict['y'] = sub_list[0]
            if labels_to_ykeys[sub_list[1]]:
                temp_dict[labels_to_ykeys[sub_list[1]]] = int(sub_list[2])
       # print "temp_dict"
        #print temp_dict
        final_list.append(temp_dict)
        #print final_list
        temp_dict = copy.deepcopy(default_dict)
    #print "final_list"
    #print final_list
    total=[]
    total.append(final_list)
    ykeys=ykeys[1:len(ykeys)]
    total.append(ykeys)
    total.append(labels)
    return total
def line_chart():
    qs = food.objects.all()
    date_list = []
    for data in qs:
        date_list.append(str(data.month))

    date_list= list(set(date_list)) # no repeat data
    #To obtain the latest month

    value = max(date_list, key=lambda x: (x))
    value = value.split("-", 1)
    d1 = datetime.datetime(int(value[0]), int(value[1]), 1)
    d2 = datetime_offset_by_month(d1, -12)
    cursor = connection.cursor()
    d2 = str(d2).split(" ", 1)
    final = (d2[0])[0:7]
    if min(date_list) < final:
        food.objects.filter(month=min(date_list)).delete()
        date_list.remove(min(date_list))

    while min(date_list) > final:
        cursor.execute("select distinct(DU),count(DU) from switch_backup group by DU;")
        row = cursor.fetchall()
        for data in row:
            food.objects.create(du=data[0],month=final)
        final = date_traverse(final, 1)

    qs = food.objects.all()
    #date_list = []
    #for data in qs:
        #date_list.append(str(data.month))
    lista = []  # first No i2n range represents No. of dus and  second No in range means month, which is a fix value
    # print list
    sublist = []
    tempdata=""
    biglist=[]
    count=0

    cursor.execute("select distinct(month) from data.data_food;")
    row= cursor.fetchall()
    #print row
    for data in row:

        qs = food.objects.filter(month=data[0])
        for data in qs:

            #print data
            count = str(data).count(' ')
            sublist = str(data).split(' ', count)
            #print sublist
            del sublist[3]
            #print sublist
            lista.append(sublist)
        #print lista
        biglist.append(lista)
        lista=[]

    #print biglist
    return biglist

def data_table():
    data_table=[]
    data_list=[]
    cursor = connection.cursor()
    cursor.execute("select distinct(DU) from switch_backup group by DU;")
    row= cursor.fetchall()
    for data in row:
        #print data[0]
        if data[0]:
            data_list=[]
            data_list.append(data[0])
            total = BackUp.objects.filter(DU=data[0]).count()
            #print "total"
            #print total
            data_list.append(total)
            online= BackUp.objects.filter(DU=data[0],Online=True).count()
            #print "online"
            #print online
            data_list.append(online)
            backup= BackUp.objects.filter(DU=data[0],BackupFailed="Backupsucceed").count()
            #print "backup"
            #print backup
            data_list.append(backup)
            ise= backup
            data_list.append(backup)
            nonstd=BackUp.objects.filter(DU=data[0],Stdname=True).count()
            #print "nonstd"
            #print nonstd
            data_list.append(nonstd)
            data_table.append(data_list)
    #print data_table
    return data_table





    #("select distinct(DU), count(Online) from switch_backup where Online = 1 group by DU;")
    #"select distinct(DU),count(DU), from switch_backup group by DU;"
    return data_table
def bar_chart():
    qs = brand.objects.all()
    date_list = []
    for data in qs:
        date_list.append(str(data.month))

    date_list = list(set(date_list))  # no repeat data
    # To obtain the latest month

    value = max(date_list, key=lambda x: (x))
    value = value.split("-", 1)
    d1 = datetime.datetime(int(value[0]), int(value[1]), 1)
    d2 = datetime_offset_by_month(d1, -12)
    cursor = connection.cursor()
    d2 = str(d2).split(" ", 1)
    final = (d2[0])[0:7]
    if min(date_list) < final:
        #   print "min"+min(date_list)
        #  print "min"+str(food.objects.filter(month=min(date_list)))
        brand.objects.filter(month=min(date_list)).delete()
        date_list.remove(min(date_list))
        # for data in food.objects.all():
        #     print data
        # to create tons of empty date
    # print "date_list"
    # print date_list
    while min(date_list) > final:
        cursor.execute("select distinct(Type),count(Type) from switch_backup group by Type;")
        row = cursor.fetchall()
        for data in row:
            if data[0]:
                brand.objects.create(type=data[0], month=final)
        final = date_traverse(final, 1)

    qs = brand.objects.all()
    # date_list = []
    # for data in qs:
    # date_list.append(str(data.month))
    lista = []  # first No i2n range represents No. of dus and  second No in range means month, which is a fix value
    # print list
    sublist = []
    tempdata = ""
    biglist = []
    count = 0

    cursor.execute("select distinct(month) from brand.brand_brand;")
    row = cursor.fetchall()
    # print row
    for data in row:

        qs = brand.objects.filter(month=data[0])
        for data in qs:
            # print data
            count = str(data).count(' ')
            sublist = str(data).split(' ', count)
            #print sublist

            lista.append(sublist)
        # print lista
        biglist.append(lista)
        lista = []
    #print "fsafashofasfousufhashi"
    #print biglist
    return biglist


# def line_chart():
#     qs = food.objects.all()
#     date_list = []
#     for data in qs:
#         date_list.append(str(data.month))
#     # To obtain the latest month
#     value = max(date_list, key=lambda x: (x))
#
#     value = value.split("-", 1)
#
#     d1 = datetime.datetime(int(value[0]), int(value[1]), 1)
#     d2 = datetime_offset_by_month(d1, -13)
#
#     d2 = str(d2).split(" ", 1)
#     final = (d2[0])[0:7]
#     # print final   # 13months before the latest one
#     if min(date_list) < final:
#         #   print "min"+min(date_list)
#         #  print "min"+str(food.objects.filter(month=min(date_list)))
#         food.objects.filter(month=min(date_list)).delete()
#         date_list.remove(min(date_list))
#         for data in food.objects.all():
#             print data
#     while min(date_list) > final:
#         food.objects.create(month=final)
#         final = date_traverse(final, 1)
#     qs = food.objects.all()
#     date_list = []
#     for data in qs:
#         date_list.append(str(data.month))
#     list = []  # first No in range represents No. of dus and  second No in range means month, which is a fix value
#     # print list
#     sublist = []
#     for data in qs:
#         count = str(data).count(' ')
#         sublist = str(data).split(' ', count)
#         # print sublist
#         list.append(sublist)
#     return list

def pie_chart():
    du_list=[]
    #for data in BackUp.objects.all():
    #   if not data.du in du_list:
    #      du_list.append(data.du)
    cursor = connection.cursor()
    cursor.execute("select distinct(DU),count(DU) from switch_backup group by DU;")
    row = cursor.fetchall()

    for data in row:

        temp={"label":data[0],"value":int(data[1])}
        du_list.append(temp)
    return du_list



def switch_rename(request):
    if request.GET.get('num'):
        num = request.GET.get('num')
        return render(request, 'switch_rename.html', {'num': num})
    elif request.GET.get('error'):
        error = request.GET.get('error')
        id = request.GET.get('id')
        return render(request, 'switch_rename.html', {'error': error, 'id': id})
    else:
        return render(request, 'switch_rename.html')


def auto_config(request):
    if request.GET.get('num'):
        num = request.GET.get('num')
        return render(request, 'auto_config.html', {'num': num})
    elif request.GET.get('error'):
        error = request.GET.get('error')
        id = request.GET.get('id')
        return render(request, 'auto_config.html', {'error': error, 'id': id})
    else:
        return render(request, 'auto_config.html')


def readlogFile(filename, chunk_size=512):
    with open(filename, 'r') as f:
        while True:
            c = f.read(chunk_size)
            c = c.replace('\n', '\r\n')
            if c:
                yield c
            else:
                break


def crontab_task(request):
    return render(request, "crontab.html")


def import_excel(request):
    return render(request, "import_excelFile.html")


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def backupTemplate(request):
    filename = "static/admin/Excel/backupTemplate.xlsx"
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=backTemplate.xlsx'
    response['Content-Length'] = os.path.getsize(filename)
    return response
def renameTemplate(request):
    filename = "/home/code/management/static/files/renameTemplate.xlsx"
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=renameTemplate.xlsx'
    response['Content-Length'] = os.path.getsize(filename)
    return response


def configTemplate(request):
    filename = "/home/code/management/static/files/Auto-Config.xlsx"
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=Auto-Config.xlsx'
    response['Content-Length'] = os.path.getsize(filename)
    return response



# switchname
def log(request):
    filename = "/home/switch_rename/rename_log.txt"
    response = StreamingHttpResponse(readlogFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=rename_log.txt'
    response['Content-Length'] = os.path.getsize(filename)
    return response

def home(request):
    return HttpResponseRedirect('http://switch-manager.com')


# config
def config_log(request):
    filename = "/home/auto_config/config_log.txt"
    response = StreamingHttpResponse(readlogFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=config_log.txt'
    response['Content-Length'] = os.path.getsize(filename)
    return response


def satistic(request):
    myFile = request.FILES.get("excel", None)
    wb = xlrd.open_workbook(filename=None, file_contents=myFile.read())
    ws = wb.sheets()[0]

    path = '/home/switch_rename/renameExcel.xlsx'
    destination = open(path, 'wb+')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()

    num = 0
    nrow = ws.nrows
    headers = ['DU', 'Floor', 'Rack', 'U', 'Brand', 'Name', 'IP']
    lists = []
    for row in range(1, nrow):
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value

        lists.append(r)
    for cell in lists:
        DU = cell['DU']
        Floor = cell['Floor']
        Rack = cell['Rack']
        U = cell['U']
        Brand = cell['Brand']
        Name = cell['Name']
        IP = cell['IP']


        if DU == '':
            continue

        num = num + 1

    return HttpResponseRedirect('/switch_rename/?num=' + str(num))


def rename_switch(request):

    num = request.GET.get('num')
    path = '/home/switch_rename/renameExcel.xlsx'
    rename_task = rename.delay(path)
    return HttpResponseRedirect('/switch_rename/?error='+str(num) + '&id=' + rename_task.id)


def backup_upload(request):
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/admin/switch/backup/')

    if not request.FILES:
        return HttpResponseRedirect('/importExcel/')
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
    ws = wb.sheets()[0]
    nrow = ws.nrows # acquire total rows
    headers = ['IP_ADDRESS','NAME',  'SWITCH_TYPE', 'DU', 'LOCATION']
    lists = []
    positions=[]
    ip_list = [] #variable (lists) only contains the total rows -1's data
    for row in range(1, nrow):
        flag = False
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value
            r[key] = str(r[key])
            r[key] = r[key].replace(" ", '')
            if key == 'IP_ADDRESS':
                ip_list.append(r[key])
        # determine if the excel file per se has the same row of data
        #for rist in lists:
        #   if not lists:
        #       pass
        #  else:
        #      if rist['IP_ADDRESS'] == r['IP_ADDRESS'] and rist['DU'] == r['DU']:
        #          flag = True
        #if not flag:
        lists.append(r)
    #print lists
    count=0
    total=len(lists)
    success=0
    failure=0
    wrong_ip=[]
    repetitive_ip=[]
    repetitive=0
    for ip in ip_list:
        # To match if it is qualified for an ip_address
        if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
             pos = ip_list.index(ip)+1 + 1
             #print "ip is" + ip
             wrong_ip.append(ip)
             #print str(pos) +"th row data 's ip address is not correct"
             #print "lists_pos"+ str(pos-count-2)+ "length"+str(len(lists))
             lists.remove(lists[pos-count-2])
             count= count+1

    #print lists
    for wrong in wrong_ip:
        ip_list.remove(wrong)
    #print "ip_list"+str(ip_list)
    position=0
    sum=0
    for ip in ip_list: #ip_list contains all correct but repetitive ips
         for object in BackUp.objects.all(): #  looping each data in database in order to find if
             if object.IPAddress==ip:    #it matches with any of ip in ip_list. If found, appends to the list
                 repetitive=repetitive+1 # lists contains all dicts  but may be repetitive with data in database
                 repetitive_ip.append(ip)
    #print "--------------"
    repetitive_ip_excel=[]
    for i in range(0,len(ip_list)):
        for j in range(0, len(ip_list)):
            if i == j:
                pass
            else:
                if ip_list[i] == ip_list[j]:
                 if ip_list[i] not in repetitive_ip_excel:
                    repetitive_ip_excel.append(ip_list[i])

    # print "repetitive_ip_excel"+str(repetitive_ip_excel)
    # print "------before--------"
    #print "lists" + str(lists)
    #print "--------------"
    for data in repetitive_ip_excel:
        for dict in lists:
             if dict: # determine if dict is empty if empty cannot locate dict["IP_ADRESS"] then key error
                if dict["IP_ADDRESS"] == data:
     #               print dict
                    repetitive=repetitive+1
                    dict.clear()


    #print "----after----------"
    #rint "lists"+str(lists)
    #print "--------------"
    for dict in lists:  # looping the dict in the lists lists contains all ip
        for key in dict:
            if key == "IP_ADDRESS":
                for data in repetitive_ip:
                    if dict[key] == data:  # dict[key]=ip
                        sum = sum + 1
      #                  print "position" + str(position+2 ) + "  sum" + str(sum) + " ip" + str(dict[key])
                        positions.append(position)
                        #lists.remove(lists[position])
        position = position + 1
    #print "lenth:"+str(len(lists))
    #print "positions:"+str(positions)
    for p in positions:
       #print "poisition:"+str(p)
        lists.insert(p+1,{})
        del lists[p]

    #print "total is "+ str(total)
    #print"wrong is "+str(count)
    #print wrong_ip
    success = total-count-repetitive
    if success < 0:
        success=0
    #print lists
    sum=0
    for list in lists:
        if not list:
         sum=sum+1
    #print "sum"+str(sum)
    empty={}
    while empty in lists:
        lists.remove(empty)
    #print"**************************************"
    #print lists


    # return render(request, 'import_excelFile.html', {'total': total,'wrong':count,'success':success,'wrong_ip':wrong_ip,'repetitive':repetitive,"repetitive_ip":repetitive_ip})
    #return HttpResponseRedirect('/importExcel/')

    sqllist = []
    for cell in lists:
        #for header in headers:
        userlist = []

        IP_ADDRESS = cell['IP_ADDRESS']
        NAME=cell['NAME']
        SWITCH_TYPE = cell['SWITCH_TYPE']
        DU = cell['DU']
        LOCATION=cell['LOCATION']
        sql = BackUp(IPAddress=IP_ADDRESS,Name=NAME, Type=SWITCH_TYPE, DU=DU, Location=LOCATION)
        same_exist = BackUp.objects.filter(IPAddress=IP_ADDRESS, DU=DU)
        if not same_exist:
            sqllist.append(sql)
    BackUp.objects.bulk_create(sqllist)
    # return HttpResponseRedirect('/admin/switch/backup/') # repetitive data is met should alert an info in the front-page
    return render(request, 'import_excelFile.html', {'total': total,'wrong':count,'success':success,'wrong_ip':wrong_ip,'repetitive':repetitive,"repetitive_ip":repetitive_ip,"repetitive_ip_excel":repetitive_ip_excel})
    # to eliminate repetitive ip
    #for i in lists:
     #   for j in lists:
      #      if lists[j]['IP_ADDRESS']==lists[i]['IP_ADDRESS']:







def upload_command(request):
    file = request.FILES.get("excel", None)
    path = '/home/auto_config/commandExcel.xlsx'
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    num = 0
    wb = xlrd.open_workbook(filename=path)
    ws = wb.sheets()[0]
    nrow = ws.nrows
    headers = ['IP', 'Brand']
    lists = []
    for row in range(1, nrow):
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value
        lists.append(r)
    for cell in lists:
        IP = cell['IP']
        brand = cell['Brand']

        if IP == '':
            continue

        num = num + 1
    return HttpResponseRedirect('/auto_config/?num=' + str(num))


def delete(request):
    ret = cron_delete.delay()
    return HttpResponseRedirect('/admin/switch/backup/')
def get_brand(request):
    ret= save_brand.delay()
    return HttpResponseRedirect('/admin/switch/backup/')
def get_data(request):
    ret = save_data.delay()
    return HttpResponseRedirect('/admin/switch/backup/')

def getInfo(request):
    getInfo_task=get_Info.delay()
    return HttpResponseRedirect('/admin/switch/backup/?&id=' + getInfo_task.id)
def getName(request):
    getName_task= get_Name.delay()
    return HttpResponseRedirect('/admin/switch/backup/?&id=' + getName_task.id)
def subnet(request):
    return render(request, 'scan_ip_subnet.html')
def scan(request):
    error=""
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/admin/switch/backup/')
        error = "Please enter a IP_subnet"

        return render(request, 'scan_ip_subnet.html', {'error': error}, )
    subnet= request.POST.get("subnet")
    community = request.POST.get("community")
    username = request.POST.get("username")
    password = request.POST.get("password")
    authority = request.POST.get("authority")
    authenproto = request.POST.get("authenproto")
    pripro = request.POST.get("pripro")
    passphase=request.POST.get("passphase")
    DU=request.POST.get("du")
    Location=request.POST.get("loc")
    if not (subnet and DU and Location):
        error = "Please fill all the mandatory fields"
        return render(request, 'scan_ip_subnet.html', {'error': error}, )
    if not community :
        if not(username and password and authority):
            error="Please fill all the mandatory fields"
            return render(request, 'scan_ip_subnet.html', {'error': error}, )
    if community :
        version= "v2c"
    if username:
        version ="v3"
    list=[]

    if not subnet :
        error = "Please enter a IP_subnet"
        return render(request, 'scan_ip_subnet.html', {'error': error}, )
    error = "format incorrect"
    if '/' not in subnet:
        return render(request, 'scan_ip_subnet.html',{'error': error},)
    if not request.POST.get('community'):
        error=""
    list = subnet.split('/',1)

    ip = list[0]
    if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
        error = "format incorrect"
        return render(request, 'scan_ip_subnet.html',{'error': error},)
    num = list[1]
    if not num:
        error = "format incorrect"
        return render(request, 'scan_ip_subnet.html', {'error': error}, )

    if int(num) < 0 or int(num) > 32:

        error = "format incorrect"
        return render(request, 'scan_ip_subnet.html', {'error': error}, )

    total = 0
    success_num=0
    fail_num=0
    no_response=0
    no_response_list=[]
    success_ip_list=[]
    fail_ip_list=[]
    ipname=""
    cmd ="nmap -host-timeout 10s -p 23 "+subnet+" -n"
    output = commands.getoutput(cmd)
    #print output
    x = output.count("for")
    subip = output.split("for",x)
    #print "length"+str(len(subip))
    for pg in subip:
     if 'open' in pg or 'filtered' in pg:
        flag=False
        index = pg.find("Host")
        ip=pg[1:index-1]
        #print ip
        if "Starting Nmap" in pg:
            continue
        if version =="v2c":
            total = total + 1
            cmd0 = "snmpwalk -t 0.2 -v 2c -c "+community+" "+ip+" SNMPv2-MIB::sysName"
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
                            list2 = output2.split(") ", 1)
                            rundate = (list2[1].split(",", 1))[0]
                        elif ty == "Juniper":
                            list = output.split("Inc.", 1)
                            model = ((list[1].split(" ", 2))[1]).split()[0]
                            list1 = output.split("JUNOS", 1)
                            vers = ((list1[1].split(",", 1))[0]).split()[0]
                            list2 = output2.split(") ", 1)
                            rundate = (list2[1].split(",", 1))[0]
                        else:
                            model = "unknown"
                            vers = "unknown"
                            rundate = "unknown"
                            # print "ip" +ip + "name" + name
                            ipname = ip + " -- " + name + " -- " + ty + " -- " + model + " -- " + vers + " -- " + rundate
                        # print ipname
                        if not (BackUp.objects.filter(IPAddress=ip) or (BackUp.objects.filter(Name=name))):
                            create = BackUp.objects.create(IPAddress=ip, Name=name, DU=DU, Location=Location, Type=ty,
                                                           Online=True, Runtime=rundate, Model=model, Version=vers,
                                                           snmp_version=version, Community=community)
                            # print create

                            success_num = success_num + 1
                            success_ip_list.append(ipname)
                        else:
                            BackUp.objects.filter(IPAddress=ip).update(Type=ty, Model=model, Version=vers,
                                                                       Runtime=rundate,
                                                                       snmp_version=version, Community=community)
                            fail_num = fail_num + 1
                            fail_ip_list.append(ipname)
                    else:
                        no_response = no_response + 1
                        no_response_list.append(ip)
                else:
                    no_response = no_response + 1
                    no_response_list.append(ip)
            else:
                no_response=no_response+1
                no_response_list.append(ip)



        if version == "v3":
            total = total + 1
            ap=""  #authentication protocol
            pp=""  #privacy protocol
            passface="" #passphase

            if authenproto:
                ap=" -a "+authenproto
            if  pripro:
                pp=" -x "+pripro
            if passphase:
               passface=" -X "+ passphase
            cmd0 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l "+authority + ap  + pp + passface+ " "+ip+" SNMPv2-MIB::sysName"
            output0 = commands.getoutput(cmd0)
            if "STRING: " in output0:
                snmpsta = "ON"
                cmd = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + ap + pp + passface + " " + ip + " SNMPv2-MIB::sysDescr"
                output = commands.getoutput(cmd)
                if "STRING: " in output:
                    cmd2 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + ap + pp + passface + " " + ip + " DISMAN-EVENT-MIB::sysUpTimeInstance"
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
                            cmd1 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + ap + pp + passface + " " + ip + " ENTITY-MIB::entPhysicalDescr.1001"
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
                                    cmd4 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + ap + pp + passface + " " + ip + " ENTITY-MIB::entPhysicalDescr.1"
                                    output4 = commands.getoutput(cmd4)
                                    list4 = output4.split("Inc.", 1)
                                    model = ((list4[1].split(" ", 2))[1]).split()[0]
                                list2 = output2.split(")", 1)
                                rundate = (list2[1].split(",", 1))[0]
                            else:
                                cmd3 = "snmpwalk -t 0.2 -v 3 -u " + username + ' -A "' + password + '"' + " -l " + authority + ap + pp + passface + " " + ip + " ENTITY-MIB::entPhysicalModelName.1"
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
                        ipname = ip + " -- " + name + " -- " + ty + " -- " + model + " -- " + vers + " -- " + rundate
                        # print ipname
                        if not (BackUp.objects.filter(IPAddress=ip) or (BackUp.objects.filter(Name=name))):
                            create = BackUp.objects.create(IPAddress=ip, Name=name, DU=DU, Location=Location, Type=ty,
                                                           Online=True, Runtime=rundate, Model=model, Version=vers,
                                                           snmp_version=version, Username=username, Password=password,
                                                           Authority=authority, Authentication_protocol=authenproto,
                                                           privacy_protocol=pripro, Passphase=passphase,Snmpv3=snmpsta)
                            # print create
                            success_num = success_num + 1
                            success_ip_list.append(ipname)
                        else:
                            BackUp.objects.filter(IPAddress=ip).update(Type=ty, Model=model, Version=vers,
                                                                       Runtime=rundate,
                                                                       snmp_version=version, Username=username,
                                                                       Password=password, Authority=authority,
                                                                       Authentication_protocol=authenproto,
                                                                       privacy_protocol=pripro, Passphase=passphase,Snmpv3=snmpsta)
                            fail_num = fail_num + 1
                            fail_ip_list.append(ipname)
                    else:
                        no_response = no_response + 1
                        no_response_list.append(ip)
                else:
                    no_response = no_response + 1
                    no_response_list.append(ip)
            else:
                no_response=no_response+1
                no_response_list.append(ip)


    return render(request, 'scan_ip_subnet.html', {'total': total,"success_num":success_num,
                                                   "fail_num":fail_num,
                                                   "success_ip_list" : success_ip_list,
                                                   "fail_ip_list":fail_ip_list
                                                   ,"no_response":no_response,
                                                   "no_response_list":no_response_list}, )


def ping(request):
    ping_IPAddress.delay()
    return HttpResponseRedirect('/admin/switch/backup/')

def email(request):
    send_email.delay()
    return HttpResponseRedirect('/admin/switch/backup/')

def backup(request):
    num = request.GET.get('num')

    print "startBackUpFile"
    backup_task = command_backup.delay()
    #sort_undownloadable()
    return HttpResponseRedirect('/admin/switch/backup/')


def config(request):
    num = request.GET.get('num')
    path = '/home/auto_config/commandExcel.xlsx'
    print "startConfigFile"
    config_task = command_config.delay(path)
    
    return HttpResponseRedirect('/auto_config/?error=' + str(num) + '&id=' + config_task.id)


# config pinpoint
def check_result(request):
    total_num = request.GET.get('num')
    print "total_num is"+total_num
    try:
        log = open("/home/auto_config/config_log.txt", 'rb')
    except Exception, e:
        check_dict = {'log': 'error'}
        return JsonResponse(check_dict)
    lines = log.readlines()
    if len(lines) < 2:
        try:
            num = open("/home/auto_config/count.txt", 'rb')
            
            progress = num.readline() + '/' + total_num  # lookhere
           
            check_dict = {'progress': progress}
            print progress
            num.close()
            return JsonResponse(check_dict)
        except Exception, e:
            check_dict = {'log': 'Error'}
            return JsonResponse(check_dict)
    else:
        if 'finished' in lines[-2]:
            print lines
            last_line = lines[-1]
            print last_line
            check_dict = {'log': last_line}
            return JsonResponse(check_dict)
        else:
            try:
                num = open("/home/auto_config/count.txt", 'rb')
                progress = num.readline() + '/' + total_num
                check_dict = {'progress': progress}
                num.close()
                return JsonResponse(check_dict)
            except Exception, e:
                check_dict = {'log': 'Error'}
                return JsonResponse(check_dict)


# rename
def check_progress(request):
    total_num = request.GET.get('num')
    print "total_num is"+total_num
    try:   
        log = open("/home/switch_rename/rename_log.txt", 'rb')
    except Exception, e:
        check_dict = {'error_log': '1'}
        return JsonResponse(check_dict)
    lines = log.readlines()
    if len(lines) < 2:
        try:
            num = open("/home/switch_rename/count.txt", 'rb')
        
            progress = num.readline() + '/' + total_num  # lookhere
            print progress
            check_dict = {'progress': progress}
            num.close()
            return JsonResponse(check_dict)
        except Exception, e:
            check_dict = {'error_log': '1'}
            return JsonResponse(check_dict)
    else: 
        if 'finished' in lines[-2]: 
            print lines
            last_line = lines[-1]
            print last_line
            check_dict = {'error_log': last_line}
            return JsonResponse(check_dict)
        else:
            try:
                num = open("/home/switch_rename/count.txt", 'rb')  # find scount
                progress = num.readline() + '/' + total_num
                check_dict = {'progress': progress}
                num.close()
                return JsonResponse(check_dict)
            except Exception, e:
                check_dict = {'error_log': '1'}
                return JsonResponse(check_dict)
                
def stop_task(request):
    id = request.GET.get('id')
    url = request.GET.get('url')
    revoke(id, terminate=True)
    
    return HttpResponseRedirect(url)

def setStr():

    return str
