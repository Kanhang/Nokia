"""management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from switch import views as switch_views
from switch import models as switch_models
from switch import backup as switch_backup
from department import department_views as department_views
from device import views as device_views
from pageview import views as pv_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', switch_views.index, name='index'),
    url(r'^transfer_page/$', switch_views.transfer_page, name='transfer_page'),
    url(r'^switch_rename/$', switch_views.switch_rename, name='switch_rename'),
    url(r'^auto_config/$', switch_views.auto_config, name='auto_config'),
    url(r'^stop_task/$', switch_views.stop_task, name='stop_task'),
    url(r'^backupTemplate/$', switch_views.backupTemplate, name='backupTemplate'),
    url(r'^backup/$', switch_views.backup, name='backup'),
    url(r'^satistic/$', switch_views.satistic, name='satistic'),
    url(r'^upload/$', switch_views.backup_upload, name='upload'),


    url(r'^departmentupload/$', department_views.department_upload, name='departmentupload'),
    url(r'^departmentimportExcel/$', department_views.department_import_excel, name='departmentimportExcel'),
    url(r'^departmentexport/$', department_views.export, name='departmentexport'),



    url(r'^deviceupload/$', device_views.device_upload, name='deviceupload'),
    url(r'^deviceimportExcel/$', device_views.device_import_excel, name='deviceimportExcel'),
    url(r'^deviceexport/$', device_views.export, name='deviceexport'),
    url(r'^pingdevice/$', device_views.pingdevice, name='pingdevice'),


    url(r'^crontab_task/$', switch_views.crontab_task, name='crontab_task'),
    url(r'^importExcel/$', switch_views.import_excel, name='importExcel'),




    url(r'^execute_rename/$', switch_views.rename_switch, name='execute_rename'),
    url(r'^renameTemplate/$', switch_views.renameTemplate, name='renameTemplate'),
    url(r'^check_progress/$', switch_views.check_progress, name='check_progress'),
    url(r'^log/$', switch_views.log, name='log'),
    url(r'^configTemplate/$', switch_views.configTemplate, name='configTemplate'),
    url(r'^check_result/$', switch_views.check_result, name='check_result'),
    url(r'^config/$', switch_views.config, name='config'),
    url(r'^upload_command/$', switch_views.upload_command, name='upload_command'),
    url(r'^config_log/$', switch_views.config_log, name='config_log'),
    url(r'^log_summary/$', switch_backup.transmit, name='log_summary'),
    url(r'^delete/$', switch_views.cron_delete, name='delete'),
    url(r'^export/$', switch_views.export, name='export'),
url(r'^dashboard/$', pv_views.dashboard,name='dashboard'),
    url(r'^home/$', switch_views.home),
    url(r'^subnet/$', switch_views.subnet,name='subnet'),
    url(r'^scan/$', switch_views.scan, name='scan'),
   url(r'^downloadzip/(?P<IP>[\s\S]+)/', switch_views.downloadzip),

    url(r'^alarm/$', switch_views.alarm, name='alarm'),
      url(r'^tools/$', switch_views.tools, name='tools'),
    # url(r'^downloadzip/(?P<Location>[\s\S]+)/(?P<DU>[\s\S]+)/(?P<Type>[\s\S]+)/(?P<IP>[\s\S]+)/', switch_views.downloadzip),
]
#  remember and focus on this url , the reg is to match any symbol