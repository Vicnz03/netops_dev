import paramiko

hostname = '192.168.178.200'
username = "vic"
password = 'vic123'
port = 22
command = 'show version'

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read())

finally:
    client.close()