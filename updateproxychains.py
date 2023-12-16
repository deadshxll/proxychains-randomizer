#!/usr/bin/python3

# 
# Proxychains proxy randomizer
#
# Developer: deadshell
# https://github.com/deadshxll/proxychains-randomizer
#
#
# Usage: sudo python3 updateproxychains.py amount_of_proxies(default=3)
# Example:
# 	sudo python3 updateproxychains.py 2
#
#

import requests
import random
import socket
import sys


proxy_chain_amount = 3
proxy_list_url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"
proxy_type = "socks4" # Make sure this works with proxychains

config_location = "/etc/proxychains.conf"



if len(sys.argv) >= 1:
	try:
		proxy_chain_amount = max(1, min(int(sys.argv[1]), 10))
	except ValueError:
		print("[-] Proxy chain amount must be a number.")
		exit()

def is_server_alive(host, port):
	try:
		s = socket.create_connection((host, port), timeout=1)
		s.close()
		return True
	except (socket.timeout, ConnectionRefusedError):
		return False

def main():
	print("[*] Getting proxy list...")
	try:
		headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
			"Range": "bytes=0-499"
		}
		public_proxy_list = requests.get(proxy_list_url, headers=headers).text.split("\n")
	except requests.exceptions.RequestException as e:
		print("[-] Failed to get proxy list. Exiting.")
		exit()

	random.shuffle(public_proxy_list)
	print (f"[*] Getting '{proxy_chain_amount}' random valid proxies from list...")
	valid_proxies = []
	for proxy in public_proxy_list:
		ip = proxy.split(":")
		alive = is_server_alive(ip[0], ip[1])
		if alive:
			valid_proxies.append(proxy)
		if len(valid_proxies) >= proxy_chain_amount:
			break

	print("[+] Using the following proxies for the proxychain configuration:")
	for proxy in valid_proxies:
		proxy = proxy.split(":")
		print(f"-> '{proxy[0]}:{proxy[1]}'")
	
	print("\n[*] Updating the configuration...")
	with open('/etc/proxychains.conf' , 'r') as f:
		lines = f.readlines()

	proxylist_start_index = lines.index('[ProxyList]\n') + 1
	lines = lines[:proxylist_start_index]

	with open('/etc/proxychains.conf' , 'w') as f:
		f.writelines(lines)

	with open(config_location, "a") as file:
		for proxy in valid_proxies:
			proxy = proxy.split(":")
			file.write(f"{proxy_type} {proxy[0]} {proxy[1]}\n")
		print("[+] Successfully configured proxychains with new proxies.")
		exit()

if __name__ == "__main__":
	import os
	if os.getuid() == 0:
		main()
	else:
		print("[-] You must run this script as root so that it can modify the proxychains.conf file.")

