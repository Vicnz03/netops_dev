import napalm

hostname = '192.168.178.200'
username = "vic"
password = 'vic123'
port = 22
command = 'show version'


from netmiko import ConnectHandler
from napalm import get_network_driver
get_network_driver('ios')
driver = get_network_driver('ios')
#device = driver('192.168.178.200', 'vic', 'vic123')
#device.open()


device = driver(hostname=hostname,username=username, password=password)
device.open()

device.get_interfaces()
return_dictionary = device.cli(['show ospf neighbor', 'show ip interface brief', ])
device.close()
print(return_dictionary['show ospf neighbor'])
print(return_dictionary['show ip interface brief'])