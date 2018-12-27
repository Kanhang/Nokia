#!/bin/bash
USER=manager
PASS=nokia123
IP=xx.xx.xx.xx
/usr/bin/expect<<EOF
spawn telnet $IP
set timeout 20
sleep 1
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
	">" {
send " show configuration |display set |save xx.xx.xx.xx.txt\r";
send "ftp 10.110.23.254 source xx.xx.xx.xx\r"}
  "incorrect" {
exit
}          
         }
sleep 1
expect {
        "Name" 
{send "root\r"}
       }
expect {
        "Password"
{send "HZnokia123!\r"}
       }
sleep 1
expect {
       "ftp>"
{send "put xx.xx.xx.xx.txt /root/backup/xx.xx.xx.xx/xx.xx.xx.xx_date.txt\r"}
}
expect {
       "complete"
{send "exit\r"}
}
expect {
        ">" {
send " exit\r";}
            }	
expect eof
EOF
exit
