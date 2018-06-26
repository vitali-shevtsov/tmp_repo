# -*- coding: utf-8 -*-

import paramiko
import threading
import os.path
import subprocess
import time
import sys
import re


#Checking IP address file and content validity
def ip_is_valid():
    ip_address_is_valid = True
    ip_file = "ssh_ip"
    global ip_list

    try:
        selected_ip_file = open(ip_file, 'r')
        selected_ip_file.seek(0)
        ip_list = selected_ip_file.readlines()
        selected_ip_file.close()

    except IOError:
        print "\n* File %s does not exist! Please check and try again!\n" % ip_file

    for ip in ip_list:
        a = ip.split('.')

        if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
            pass
        else:
            print '\n* There was an INVALID IP address! Please check and try again!\n'
            ip_address_is_valid = False
    return ip_address_is_valid


#Checking user file validity
def user_is_valid():
    user_file_is_valid = True
    global user_file
    user_file = "ssh_user"

    if os.path.isfile(user_file) == True:
        pass
    else:
        print "\n* File %s does not exist! Please check and try again!\n" % user_file
        user_file_is_valid = False
    return  user_file_is_valid


#Checking command file validity
def cmd_is_valid():
    cmd_file_is_valid = True
    global cmd_file

    cmd_file = 'cmd_file'
    if os.path.isfile(cmd_file) == True:
        print "\n* Sending command(s) to device(s)...\n"
    else:
        print "\nFile %s does not exist! Please check and try again!\n" % cmd_file
        cmd_file_is_valid = False
    return cmd_file_is_valid


#Open SSHv2 connection to devices
def open_ssh_conn(ip):
    #Change exception message
    try:
        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0]
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Connect to the device using username and password
        session.connect(ip, username = username, password = password)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()
        
        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Setting terminal length for entire output - disable pagination
        connection.send("screen-length 0 temporary\n")
        time.sleep(1)

        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line)
            time.sleep(1)
        
        #Closing the user file
        selected_user_file.close()
        
        #Closing the command file
        selected_cmd_file.close()
        
        #Checking command output for syntax errors
        router_output = connection.recv(65535)
        
        if re.search(r"Unrecognized command found at", router_output):
            print "* There was at least one syntax error on device %s" % ip
            
        else:
            print "\nDONE for device %s" % ip
            
        #Test for reading command output
        print router_output + "\n"
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print "* Invalid username or password. \n* Please check the username/password file or the device configuration!"
        print "* Closing program...\n"


#Creating threads
def create_threads():
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = open_ssh_conn, args = (ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

#Calling threads creation function
if ip_is_valid() and user_is_valid() and cmd_is_valid():
    create_threads()

#End of program
