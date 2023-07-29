# dynamically extract the ip address of the raspberry pi from eth0 interface
import netifaces as ni
rpi_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
print(rpi_ip)  # should print "139.91.96.156"