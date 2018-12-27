#!/bin/bash
echo "+++++++++++++++++++++++++++++++++++++++++"

success() {
SCREEN=`stty -F /dev/console size 2>/dev/null`
COLUMNS=${SCREEN#* }
[ -z $COLUMNS ] && COLUMNS=80
SPA=$[$COLUMNS-7]
NORMAL='\033[0m'
string=$1
RT=$[$SPA-${#string}]
for I in `seq 1 $RT`;do
        echo -n " "
done
echo -e "[ \033[1;34mOK\033[0m  ]"
}                                     

failure() {
SCREEN=`stty -F /dev/console size 2>/dev/null`
COLUMNS=${SCREEN#* }
[ -z $COLUMNS ] && COLUMNS=80
SPA=$[$COLUMNS-7]
NORMAL='\033[0m'
string=$1
RT=$[$SPA-${#string}]
for I in `seq 1 $RT`;do
	echo -n " "
done
echo -e "[ \033[1;34mFAILED$NORMAL ]"
}

installed() {
SCREEN=`stty -F /dev/console size 2>/dev/null`
COLUMNS=${SCREEN#* }
[ -z $COLUMNS ] && COLUMNS=80
SPA=$[$COLUMNS-7]
NORMAL='\033[0m'
string=$1
RT=$[$SPA-${#string}]
for I in `seq 1 $RT`;do
	echo -n " "
done
echo -e "[ \033[1;34minstalled$NORMAL ]"
}

CHECKSO() {
local string=$1
SOF=`rpm -qa $string`
SOF1=${#SOF}
if [ $SOF1 -lt 1 ];then
	echo "waiting install $string ..."
	yum -y install $string &>/dev/null
	if [ $? -eq 0 ];then
		[ $SOF1 -lt 1 ] && echo -n "install";success "$string"
	else
		echo -n "install $string,not found $string";failure "$string"
	fi
else
	echo -n "exist $string";installed "$string"
fi
} 
 
CHECKSO gcc 
#CHECKSO make
#CHECKSO curl 
#CHECKSO curl-devel 
#CHECKSO mysql-devel
#CHECKSO 
#yum -y groupinstall "Development Tools"
