#!/bin/bash
USER=manager
PASS=nokia123
IP=xx.xx.xx.xx
/usr/bin/expect<<EOF
spawn telnet $IP
set timeout 10

	expect {
                "username:" 
{send "$USER\r";
sleep 1
send "$PASS\r"}
                "Username:" 
{send "$USER\r";
sleep 1
send "$PASS\r"}
                "User:" 
{send "$USER\r";
sleep 1
send "$PASS\r"}
                "login:" 
{send "$USER\r";
sleep 1
send "$PASS\r"}
                "Login:" 
{send "$USER\r";
sleep 1
send "$PASS\r"}
	}

expect {
                "#" {
send "admin save xx.xx.xx.xx\r";
send "file copy cf1:\xx.xx.xx.xx ftp://root:nokia123@10.110.23.254/root/backup/subpath/NUAGE/xx.xx.xx.xx/xx.xx.xx.xx_date.txt\r";
}
}
expect {
        "Copying"
{send "exit\r"}
}
expect eof
EOF
exit
