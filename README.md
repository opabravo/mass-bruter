# Mass Bruter
Mass bruteforce network protocols

## Info
Simple personal script to quickly mass bruteforce common services in a large scale of network.<br>
It will check for default credentials on ftp, ssh, mysql, mssql...etc.<br>
This was made for authorized red team penetration testing purpose only.

## How it works
- Use `masscan`(faster than nmap) to find alive hosts with common ports from network segment.
- Parse ips and ports from `masscan` result.
- Craft and run `hydra` commands to automatic bruteforce devices.

## Requirements
- `Kali linux` or any preferred linux distribution
- `Python 3.10+`
- `apt update && apt install seclists masscan hydra`

## How To Use
Save masscan results under `./result/masscan/`,<br>
with the format `masscan_<name>.<ext>`, Ex: `masscan_192.168.0.0-16.txt`<br>
Private ip range : `10.0.0.0/8`, `192.168.0.0/16`, `172.16.0.0/12` <br>
Example command:
```bash
masscan -p 3306,1433,21,22,23,445,3389,5900,6379,27017,5432,5984,11211,9200,1521 172.16.0.0/12 | tee ./result/masscan/masscan_test.txt
```
Example Resume Command: 
```bash
masscan --resume paused.conf | tee -a ./result/masscan/masscan_test.txt
```
---
Command Options
```bash
┌──(root㉿root)-[~/mass-bruter]
└─# python3 mass_bruteforce.py
Usage:  [OPTIONS]

  Mass Bruteforce Script

Options:
  -q, --quick           Quick mode (Only brute telnet, ssh, ftp , mysql,
                        mssql, postgres, oracle)
  -a, --all             Brute all services(Very Slow)
  -s, --show            Show result with successful login
  -f, --file-path PATH  The directory or file that contains masscan result
                        [default: ./result/masscan/]
  --help                Show this message and exit.
```

Quick Bruteforce Example:
```bash
python3 mass_bruteforce.py -q -f ~/masscan_script.txt
```
![](https://i.imgur.com/hVbIaki.png)

Fetch cracked credentials:
```bash
python3 mass_bruteforce.py -s
```
![](https://i.imgur.com/FPSMAEb.png)


## Todo
- [ ] Migrate with `dpl4hydra`
- [ ] Optimize the code and functions
- [ ] MultiProcessing

Any contributions are welcomed!