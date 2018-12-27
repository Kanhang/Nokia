#!/bin/bash
USER=manager
PASS=nokia123
IP=---IP---
/usr/bin/expect<<EOF
spawn telnet $IP
set timeout ---timeout---
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
		">" {
exp_continue
}
	 	"#" {
} 
	}
expect eof
EOF
exit
