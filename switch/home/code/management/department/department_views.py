# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import StringIO
import time

import xlrd
import xlwt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import department


# Create your views here.
def export(request):
    local_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_name = 'department_' + local_time + '.xls'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    wb = xlwt.Workbook(encoding="utf-8")
    sheet = wb.add_sheet(u'data')
    headers = ['Tribe_name', 'Tribe', 'Squad-groups', 'Squad', 'LabOps', 'LabOrder', 'LabSupport']
    for i in range(0, len(headers)):
        sheet.write(0, i, headers[i])
    row = 1
    for k in department.objects.all():
        sheet.write(row, 0, k.Tribe_name)
        sheet.write(row, 1, k.Tribe)
        sheet.write(row, 2, k.Squad_groups)
        sheet.write(row, 3, k.Squad)
        sheet.write(row, 4, k.LabOps)
        sheet.write(row, 5, k.LabOrder)
        sheet.write(row, 6, k.LabSupport)
        row = row + 1
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def department_import_excel(request):

    return render(request, "department_import_excelFile.html")


def department_upload(request):
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/admin/department/department/')

    if not request.FILES:
        return HttpResponseRedirect('/departmentimportExcel/')
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
    ws = wb.sheets()[0]
    nrow = ws.nrows  # acquire total rows
    headers = ['Tribe_name', 'Tribe', 'Squad-groups', 'Squad', 'LabOps', 'LabOrder', 'LabSupport']
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
        DU = cell['Tribe_name']
        Tribe = cell['Tribe']
        Squad_groups = cell['Squad-groups']
        Squad = cell['Squad']
        LabOps = cell['LabOps']
        LabOrder = cell['LabOrder']
        LabSupport = cell['LabSupport']
        sql = department(Tribe_name=DU, Tribe=Tribe, Squad_groups=Squad_groups, Squad=Squad, LabOps=LabOps, LabOrder=LabOrder,
                         LabSupport=LabSupport)
        sqllist.append(sql)
    department.objects.bulk_create(sqllist)

    return HttpResponseRedirect('/admin/department/department')
