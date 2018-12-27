#!/bin/bash
USER=manager
PASS=nokia123
IP=xx.xx.xx.xx
/usr/bin/expect<<EOF
spawn telnet $IP
set timeout 20

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
"assword:" 
{exit}
	}

expect {
                "#" {
send "write\r";
sleep 1
send "copy running-config ftp://root:HZnokia123!@10.110.23.254/backup/xx.xx.xx.xx/xx.xx.xx.xx_date.txt\r";
}
   "Authentication failed" {
exit
}
}
expect {
        "copied"
{send "exit\r"}
}

expect eof
EOF
exit
