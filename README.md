# Proxychains Randomizer
A quick python script that allows you to randomize your proxychains proxies using [TheSpeedX's frequently updated proxy list](https://github.com/TheSpeedX/PROXY-List)

---
![ezgif com-speed (1)](https://github.com/deadshxll/proxychains-randomizer/assets/67878277/028eac78-72a9-4d56-b3e0-ec3fb9c8ac46)

---
## How to run
Make sure you have Python 3 installed along with proxychains, obviously, this tool wont work for windows.
Run the following command:
```bash
python3 updateproxychains.py {proxy_amount}
```
---
If you prefer to be able to run this script like any other command on linux, run the following commands:
```bash
chmod +x updateproxychains.py
mv updateproxychains.py /usr/local/bin/updateproxychains
```
To run it from here you can simply just execute:
```
sudo updateproxychains {proxy_amount}
```
## What is Proxychains?
Proxychains is a utility that allows users to run any software through a proxy server, allowing them to mask the origin of network traffic, improve privacy, and circumvent certain restrictions. It is often used to anonymize network activities and maintain a level of confidentiality when connecting to the internet.

## What does this script do?
This script grabs a random list of proxies from a specified URL, tests them to make sure that they are not dead, then using the verified proxies, the script modifies the proxychains configuration file typically located at `/etc/proxychains.conf` on linux systems.

## Learn more
https://www.kali.org/tools/proxychains-ng/

https://subscription.packtpub.com/book/security/9781783289592/2/ch02lvl1sec22/setting-up-proxychains

https://www.youtube.com/watch?v=jqrd9Ba3VOc
