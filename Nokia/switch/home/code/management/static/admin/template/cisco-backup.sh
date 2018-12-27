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
                "#" {
send "copy running-config tftp://10.110.23.254\r"}
              "Authentication failed" {
exit
}
              "invalid" {
exit
}
}
expect {
        "Address"
{send "10.110.23.254\r"}
       }
expect {
        "Destination"
{send "xx.xx.xx.xx/xx.xx.xx.xx_date.txt\r"}
}
expect {
        "copied"
{send "exit\r"}
}
	
expect eof
EOF
exit
