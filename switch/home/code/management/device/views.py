# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.

import StringIO
import time

import xlrd
import xlwt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import device

from device.tasks import ping_DeviceIPAddress



def pingdevice(request):

    ret = ping_DeviceIPAddress.delay()

    return HttpResponseRedirect('/admin/device/device/')

# Create your views here.
def export(request):
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_name = 'device_' + local_time + '.xls'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    wb = xlwt.Workbook(encoding="utf-8")
    sheet = wb.add_sheet(u'data')
    headers = ['IPAddress', 'Device_type', 'Status', 'Location', 'Tribe_name', 'Update_time']
    for i in range(0, len(headers)):
        sheet.write(0, i, headers[i])
    row = 1
    for k in device.objects.all():
        sheet.write(row, 0, k.IPAddress)
        sheet.write(row, 1, k.Device_type)
        sheet.write(row, 2, k.Status)
        sheet.write(row, 3, k.Location)
        sheet.write(row, 4, k.Tribe_name)
        sheet.write(row, 5, k.Update_time)
        row = row + 1
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def device_import_excel(request):

    return render(request, "device_import_excelFile.html")


def device_upload(request):
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/admin/device/device/')

    if not request.FILES:
        return HttpResponseRedirect('/deviceimportExcel/')
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
    ws = wb.sheets()[0]
    nrow = ws.nrows  # acquire total rows
    headers = ['IPAddress', 'Device_type', 'Status', 'Location', 'Tribe_name', 'Update_time']
    lists = []
    for row in range(1, nrow):
        flag = False
        r = {}
        for col in range(0, len(headers)):
            key = headers[col]
            r[key] = ws.cell(row, col).value
            r[key] = str(r[key])
        lists.append(r)
    sqllist = []
    for cell in lists:
        IPAddress = cell['IPAddress']
        Device_type = cell['Device_type']
        Status = cell['Status']
        Location = cell['Location']
        DU = cell['Tribe_name']
        Update_time = cell['Update_time']

        sql = device(IPAddress=IPAddress, Device_type=Device_type,Location=Location, Tribe_name=DU)
        sqllist.append(sql)
    device.objects.bulk_create(sqllist)

    return HttpResponseRedirect('/admin/device/device')
