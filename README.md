# Mass Bruter

Mass bruteforce network protocols

## Info

Simple POC to quickly mass bruteforce common services in a large scale of network.

It will check for default credentials on ftp, ssh, mysql, mssql...etc.

This was made for authorized penetration testing purpose only.

## How it works

1. Use `masscan`(faster than nmap) to find alive hosts with common ports from network segment.
2. Parse ips and ports from `masscan` result.
3. Craft and run `hydra` commands to automatically bruteforce supported network services on devices.

## Requirements

- `Kali linux` or any preferred linux distribution
- `Python 3.10+`

```bash
# Install required tools for the script
apt update && apt install seclists masscan hydra

# Clone the repo
git clone https://github.com/opabravo/mass-bruter
cd mass-bruter
```

## How To Use

### 1. Scan for hosts and ports with masscan

For example, target a network segment:

> Private ip range : `10.0.0.0/8`, `192.168.0.0/16`, `172.16.0.0/12` 

Scan devices and ports from `172.16.0.0/12`, then save output to `./result/masscan/masscan_<any_name>.<any_ext>`

```bash
masscan -p 3306,1433,21,22,23,445,3389,5900,6379,27017,5432,5984,11211,9200,1521 172.16.0.0/12 | tee ./result/masscan/masscan_test.txt
```

PS : To resume a previous scan:

```bash
masscan --resume paused.conf | tee -a ./result/masscan/masscan_test.txt
```

### 2. Run the script

Load masscan result then start bruteforcing:

```bash
python3 mass_bruteforce.py -q -f ~/masscan_script.txt
```

![](https://i.imgur.com/hVbIaki.png)

Fetch cracked credentials:

```bash
python3 mass_bruteforce.py -s
```

![](https://i.imgur.com/FPSMAEb.png)


## Command Options

```console
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

## Todo
- [ ] Migrate with `dpl4hydra`
- [ ] Optimize the code and functions
- [ ] MultiProcessing

Any contributions are welcomed!