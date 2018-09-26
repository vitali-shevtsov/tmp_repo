import time
import paramiko

class UseSSH:

    def __init__(self, host, port=22, user='login', passw='passwd'):
        self.hostname = host
        self.portnum  = port
        self.username = user
        self.password = passw

    def __enter__(self):
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.session.connect(self.hostname,self.portnum,self.username,self.password)
        self.connection = self.session.invoke_shell()
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.session.close()


with UseSSH('192.168.1.1') as connection:
    connection.send("screen-length 0 temporary\n")
    time.sleep(0.5)
    router_output = connection.recv(65535)
