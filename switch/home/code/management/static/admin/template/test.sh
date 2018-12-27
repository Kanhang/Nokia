#!/bin/bash
USER=manager
PASS=nokia123
IP=10.57.129.76
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
send "copy running-config ftp://root:nokia123@10.110.23.86/backup/10.110.1.1.txt\r";
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
