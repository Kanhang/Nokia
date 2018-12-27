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
"assword:" 
{exit}
	}
expect {
                ">" {
send "show version | begin Model number\r"
}
                "#" {
send "show version | begin Model number\r";
send "show version | begin Model Number\r"
}
              "Authentication failed" {
exit
}
              "incorrect" {
exit
}
              "invalid" {
exit
}
}
expect {
                "JUNOS" {
send "q\r";
send "exit\r"
}
                "#" {
send "exit\r";
send "logout\r"
}
                "BOOTLDR" {
send "e\r";
send "exit\r"
}
}
expect eof
EOF
exit
