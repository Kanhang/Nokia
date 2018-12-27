import commands
import os, time
import re, sys, paramiko

def rename_juniper(IP, name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=IP, port=22, username='manager', password='nokia123', timeout=5)
        ssh_con = ssh.invoke_shell()
        ssh_con.send("\r\n")
        ssh_con.send("configure\r\n")
        time.sleep(1)
        output = ssh_con.recv(2048)
        if 'Configuring from terminal' in output:
            return False
        print output
        ssh_con.send("set system host-name "+ name +"\r\n")
        time.sleep(1)
        output = ssh_con.recv(2048)
        if 'Error' in output:
            return False
        print output
        ssh_con.send("commit\r\n")
        output = ssh_con.recv(2048)
        print output
        return True
    except Exception, e:
        set_name = "set system host-name " + name
        command_list = ['commit',set_name,'configure']
        if telnet_rename(IP, 'Juniper', command_list):
            return True
        else:
            return False


def rename_dell_cisco(IP, name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=IP, port=22, username='manager', password='nokia123', timeout=5)
        ssh_con = ssh.invoke_shell()
        ssh_con.send("\r\n")
        ssh_con.send("configure terminal\r\n")
        time.sleep(1)
        output = ssh_con.recv(2048)
        if 'error' in output:
            return False
        print output
        ssh_con.send("hostname " + name + "\r\n")
        output = ssh_con.recv(2048)
        print output
        ssh_con.send("end\r\n")
        output = ssh_con.recv(2048)
        print output
        ssh_con.send("write\r\n")
        output = ssh_con.recv(2048)
        print output
        return True
    except Exception, e:
        set_name = "hostname " + name
        command_list = ['write','end',set_name,'configure terminal']
        if telnet_rename(IP, 'dell', command_list):
            return True
        else:
            return False
    

    
def telnet_rename(IP, brand, command_list):
    path = '/home/switch_rename/' + IP + '.sh'
    
    if brand == 'Juniper':
        create_cmd = 'cp /home/code/management/static/files/juniper.sh ' + path
        timeout = 3
    else:
        create_cmd = 'cp /home/code/management/static/files/dell-cisco.sh ' + path
        timeout = 2
    print create_cmd
    os.system(create_cmd)
    cmd = "sed -i s/---timeout---/" + str(timeout) + "/g " + path 
    print cmd
    os.system(cmd)
    
    cmd = "sed -i s/---IP---/" + IP + "/g " + path 
    print cmd
    os.system(cmd)
    
    if brand == 'Juniper':
        command_cmd = "sed -i \'/\">\"/ a\send \"" + command_list[-1] + "\r\"\' " + path
        print command_cmd
        os.system(command_cmd)
        for command in command_list:
            if command == command_list[-1]:
                continue
            if '\n' in command:
                command = command.replace("\n","\\n")
            if '"' in command:
                command = command.replace('"','\\\\"')
    
            command_cmd = "sed -i \'/\"#\"/ a\send \"" + command + "\r\"\' " + path
            print command
            print command_cmd
            os.system(command_cmd)
    else:
        for command in command_list:
            if '\n' in command:
                command = command.replace("\n","\\n")
            if '"' in command:
                command = command.replace('"','\\\\"')
    
            command_cmd = "sed -i \'/\"#\"/ a\send \"" + command + "\r\"\' " + path
            print command
            print command_cmd
            os.system(command_cmd)
    
    output = commands.getoutput('sh ' + path)
    print output
    
    
    if 'error' in output:
        return False
    elif 'Error' in output:
        return False
    elif 'executing' in output:
        return False
    elif 'Connected' not in output:
        return False
    return True
