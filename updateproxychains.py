#!/usr/bin/python3

# 
# Proxychains proxy randomizer
#
# Developer: deadshell
# https://github.com/deadshxll/proxychains-randomizer
#

import requests
import random
import socket



proxy_chain_amount = 3
proxy_list_url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"
proxy_type = "socks4" # Make sure this works with proxychains




def is_server_alive(host, port):
	try:
		s = socket.create_connection((host, port), timeout=1)
		s.close()
		return True
	except (socket.timeout, ConnectionRefusedError):
		return False

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
	"Range": "bytes=0-499"
}
def main():
	print("[*] Getting proxy list...")
	try:
		public_proxy_list = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt", headers=headers).text.split("\n")
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
	with open("/etc/proxychains.conf", "r") as file:
		lines = file.readlines()
	
	found_line = False
	for i, line in enumerate(lines):
		if "# defaults set to \"tor\"" in line:
			found_line = True
			break
	if found_line:
		with open("/etc/proxychains.conf", "w") as file:
			file.writelines(lines[:i+1])
		with open("/etc/proxychains.conf", "a") as file:
			for proxy in valid_proxies:
				proxy = proxy.split(":")
				file.write(f"socks4 {proxy[0]} {proxy[1]}\n")
			print("[+] Successfully configured proxychains with new proxies.")
			exit()
	else:
		print("[-] Make sure you have the default proxychains config in there with all the comments and stuff")
		print("[-] Failed.")
		exit()

if __name__ == "__main__":
	import os
	if os.getuid() == 0:
		main()
	else:
		print("[-] You must run this script as root so that it can modify the proxychains.conf file.")

