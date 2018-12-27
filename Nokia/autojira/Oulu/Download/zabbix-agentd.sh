#!/bin/bash
echo "++++++++++++++++++delete old_file++++++++++++++++++++++"
[ -f /root/zabbix_install.sh ] && rm -rf /root/zabbix_install.sh && echo "delete zabbix_install.sh OK"
[ -f /root/yumupdate.sh ] && rm -rf /root/yumupdate.sh && echo "delete yumupdate.sh OK"
[ -d /etc/zabbix ] && rm -rf /etc/zabbix
rm -rf /etc/init.d/zabbix_agentd
[ -d /usr/local/zabbix ] && rm -rf /usr/local/zabbix
[ -d /zabbix-2.2.2 ] && rm -rf /zabbix-2.2.2
[ -f /zabbix_install.sh ] && rm -rf /zabbix_install.sh
[ -d /expect_zabbix ] && rm -rf /expect_zabbix
pkill zabbix_agentd
sleep 3
echo "++++++++++++++++++++install zabbix3.2++++++++++++++++++++++"
cd /usr/local/src/ 
wget -P /expect_zabbix/ http://10.107.2.44/zabbix_agent/check.sh
wget -P /expect_zabbix/ http://10.107.2.56/.help/yumupdate.sh
. /expect_zabbix/yumupdate.sh
. /expect_zabbix/check.sh
groupadd zabbix
/usr/sbin/useradd -g zabbix -s /sbin/nologin zabbix
wget -P /expect_zabbix http://10.107.2.44/zabbix_agent/zabbix-3.2.0.tar.gz
cd /expect_zabbix/ && tar xf /expect_zabbix/zabbix-3.2.0.tar.gz && cd zabbix-3.2.0
./configure --prefix=/usr/local/zabbix --sysconfdir=/etc/zabbix --enable-agent && make && make install
[ $? -eq 1 ] && exit 200 
echo -e "\033[32m+++++++++++++++++++++configure start file++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m"
#[ ! -d /etc/zabbix ] && mkdir /etc/zabbix && echo "create zabbix folder OK"
#[ ! -f /etc/zabbix/zabbix_agentd.conf ] && cp /zabbix-2.2.2/conf/zabbix_agentd.conf /etc/zabbix/
IP_1=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:" | grep "10."`
sed -i 's/Server=127.0.0.1/Server=10.107.2.58/g' /etc/zabbix/zabbix_agentd.conf && echo "Server=10.107.2.58"
sed -i "s/Hostname=Zabbix server/Hostname=$IP_1/g" /etc/zabbix/zabbix_agentd.conf && echo "Hostname=$IP_1"
sed -i 's/ServerActive=127.0.0.1/ServerActive=10.107.2.58:10051/g' /etc/zabbix/zabbix_agentd.conf && echo "ServerActive=10.107.2.58"

##start  option
cp /expect_zabbix/zabbix-3.2.0/misc/init.d/fedora/core/zabbix_agentd /etc/init.d/zabbix_agentd 
sed -i "s#BASEDIR=/usr/local#BASEDIR=/usr/local/zabbix#g" /etc/init.d/zabbix_agentd && chmod +x /etc/init.d/zabbix_agentd
chkconfig zabbix_agentd on || exit 200
#/usr/local/zabbix/sbin/zabbix_agentd start || /usr/local/zabbix/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agent.conf
service zabbix_agentd start
rm -rf /expect_zabbix
echo -e "\033[34m++++++++++++++++++++++++++off iptables selinux port ntp+++++++++++++++++++++++++++\033[0m"
cat /etc/services | grep "zabbix*" &>/dev/null || echo "zabbix_agent    10050/tcp" >> /etc/services
cat /etc/services | grep "zabbix*" &>/dev/null || echo "zabbix_agent    10050/udp" >> /etc/services
service iptables stop || systemctl stop iptables.service
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 10050 -j ACCEPT
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 10051 -j ACCEPT
setenforce 0
SE=`cat /etc/selinux/config | grep "^SELINUX="` 
sed -i "s/$SE/SELINUX=disabled/g" /etc/selinux/config
ntpdate 10.107.2.44
echo ' '
echo -e "\033[31m++++++++++++++++++++++configure file+++++++++++++++++++\033[34m"
egrep -v "(^#|^$)" /etc/zabbix/zabbix_agentd.conf
echo ' '
echo -e "\033[31m++++++++++++++++++++++start zabbix-agent+++++++++++++++++++\033[34m"
service zabbix_agentd restart
echo -e "\033[31m++++++++++++++++++++++version zabbix-agent+++++++++++++++++++\033[34m"
/usr/local/zabbix/sbin/zabbix_agentd -V

