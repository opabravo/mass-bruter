import json
import os
from collections import defaultdict


def get_masscan_files(scan_path: str) -> list:
    """Return full file paths of valid masscan result"""
    return [os.path.join(scan_path, file) for file in os.listdir(scan_path) if "masscan_" in file and os.path.isfile(os.path.join(scan_path, file))]


def get_ips_with_port(masscan_path: str) -> defaultdict:
    """Parse data from masscan result, return ips with ports in a dictionary"""
    ip_and_ports = defaultdict(set)
    if os.path.isfile(masscan_path):
        extract_ip_ports(ip_and_ports, masscan_path)
    else:
        for file in get_masscan_files(masscan_path):
            extract_ip_ports(ip_and_ports, file)
    return ip_and_ports


def extract_ip_ports(ip_and_ports: defaultdict, file_path: str) -> defaultdict:
    """Grab ips and ports from masscan result and append into dictionary"""
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            splitted = line.strip().split()
            if len(splitted) != 6:  # Check if line is valid
                continue
            port = splitted[3].split("/")[0]
            ip = splitted[5]
            ip_and_ports[ip].add(port)
    return ip_and_ports


def get_result_files(folder: str = None):
    """Return full file paths of valid result files"""
    folder = folder or "./result/bruteforce/"
    return [os.path.join(folder, file) for file in os.listdir(folder) if file.startswith("hydra_") and os.path.isfile(os.path.join(folder, file))]


def load_services() -> dict:
    """Load port and service from json"""
    with open("services.json", encoding="utf-8") as f:
        return json.load(f)


def load_excluded() -> dict:
    """Load excluded ip:port"""
    with open("settings.json", encoding="utf-8") as f:
        return json.load(f)["excluded"]


def save_excluded(excluded: dict):
    """Save excluded ip:port"""
    with open("settings.json", encoding="utf-8") as f:
        settings = json.load(f)
    settings["excluded"] = excluded
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def generate_masscan_cmd(ip: str):
    """Generate masscan cmd from services.json"""
    ports = load_services().keys()
    masscan_cmd = f"masscan -p {','.join(ports)} {ip} | tee ./result/masscan/masscan_test.txt"
    print(masscan_cmd)
