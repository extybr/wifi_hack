from flask import Flask, render_template, send_from_directory, request
from re import match
from functions import Type, Path, TEMPFOLDER

SYSTEM = ''
if Path('/etc/debian_version').exists():
    SYSTEM = 'deb'
    from functions.manager_deb import *
elif Path('/etc/arch-release').exists():
    SYSTEM = 'arch'
    from functions.manager_arch import *
    checking_installed_programs()
else:
    exit('not supported')

TEMPLATE = {'deb': 'index_deb.html',
            'arch': 'index_arch.html'}

root_path = Path().cwd()
template_path = Path(root_path) / 'template'
app = Flask(__name__, template_folder=template_path)
mkdir()


def msg_post(length: int, name: str) -> str:
    message = (f'<div><form method="post"><br><label for="name-{name}">'
               f'{name.capitalize()}: </label>'
               f'<input id="name-{name}" name="{name}" type="text" '
               f'maxlength="{length}"> <button type="submit">submit</button>'
               f'</br></form></div></h2></html>')
    return message


@app.errorhandler(404)
def not_found(error: Type[Exception]) -> str:
    if str(error)[:3] == '404':
        html = ('<html><h2>This page is missing, but you can follow '
                'these links:</h2>')
        return html + pages()


@app.errorhandler(500)
def bad_argument(error: Type[Exception]) -> str:
    if str(error)[:3] == '500':
        html = "<h2><font color='red'>Invalid arguments</font></h2>"
        return html


def pages() -> str:
    html = '<ul><b>'
    for url in app.url_map.iter_rules():
        html += f"<li><p><h3><a href='{url}'>{url}</a></h3></p></li>"
    return html + "</b></ul></html>"


@app.route('/index')
@app.route('/')
def index():
    return render_template(TEMPLATE[SYSTEM])


@app.route('/template/<path:path>')
def send_template(path):
    return send_from_directory(template_path, path)


@app.route('/help')
def md_help() -> str:
    with open('template/help.md', 'r', encoding='utf-8') as text:
        man = text.read()
    return f"<h1><font color='blue'><pre>{man}</pre></font></h1>"


@app.route('/mac_change')
def mac_change() -> str:
    return change_mac(mac='00:11:22:33:44:55')


@app.route('/txpower_change')
def txpower() -> str:
    return change_power()


@app.route('/channel_change/<channel>', methods=['GET', 'POST'])
def ch(channel: str) -> str:
    if request.method == 'POST':
        channel = f"{request.form['ch']}"
    return change_channel(channel)


@app.route('/airmon-ng_check')
def airmon_check() -> str:
    return get_airmon_check()


@app.route('/airmon-ng_check_kill')
def airmon_check_kill() -> str:
    return set_airmon_check_kill()


@app.route('/airmon-ng_wlan_mode_monitor')
def airmon_mode_monitor() -> str:
    return set_airmon_mode_monitor()


@app.route('/wlan_mode_monitor')
def wlan_mode_monitor() -> str:
    return set_wlan_mode_monitor()


@app.route('/wlan_set_type_monitor')
def wlan_set_type_monitor() -> str:
    return set_wlan_set_type_monitor()


@app.route('/add_mon_type_monitor')
def add_mon_type_monitor() -> str:
    return set_add_mon_type_monitor()
    
    
@app.route('/add_wlanXmon_type_monitor')
def add_wlanXmon_type_monitor() -> str:
    return set_add_wlanXmon_type_monitor()


@app.route('/wlan_mode_managed')
def mode_managed() -> str:
    return set_mode_managed()


@app.route('/virtual_interface_delete')
def delete_interface() -> str:
    return set_del_mon_interface()


@app.route('/tempfiles_delete')
def delete_tempfiles() -> str:
    path = Path(TEMPFOLDER)
    ext = ['kismet', 'hash', 'pcap', 'cap', 'csv', 'netxml', 'log', 'conf']
    return set_del_tempfiles(path, ext)


@app.route('/airodump-ng')
def airodump() -> str:
    return set_airodump()


@app.route('/airodump_channel_36-177')
def airodump_channel_36_177() -> str:
    return set_airodump_channel_36_177()


@app.route('/airodump_manufacturer_uptime_wps')
def airodump_manufacturer_uptime_wps() -> str:
    return set_airodump_manufacturer_uptime_wps()


@app.route('/airbase_fake_ap')
def airbase_fake_ap() -> str:
    return set_airbase_fake_ap()


@app.route('/mdk3_fake_ap')
def mdk3_fake_ap() -> str:
    return set_mdk3_fake_ap()

    
@app.route('/mdk4_fake_ap')
def mdk4_fake_ap() -> str:
    return set_mdk4_fake_ap()


@app.route('/scapy_beacon')
def scapy_beacon() -> str:
    return set_scapy_beacon()


@app.route('/mdk4_deauthentication_all_channel')
def mdk4_deauthentication() -> str:
    return set_mdk4_deauthentication()


@app.route('/aireplay_deauthentication_all_channel')
def aireplay_deauthentication() -> str:
    return set_aireplay_deauthentication()


@app.route('/scapy_deauthentication_all_channel')
def scapy_deauthentication() -> str:
    return set_scapy_deauthentication()


@app.route('/aireplay_inject')
def aireplay_inject() -> str:
    return set_aireplay_inject()


@app.route('/wifite-reaver')
def wifite() -> str:
    return set_wifite()


@app.route('/wifiphisher')
def wifiphisher() -> str:
    return set_wifiphisher()


@app.route('/waidps')
def waidps() -> str:
    return set_waidps()


@app.route('/wifijammer')
def wifijammer() -> str:
    return set_wifijammer()


@app.route('/fake-ap')
def fake_ap() -> str:
    return set_fake_ap()


@app.route('/fluxion')
def fluxion() -> str:
    return set_fluxion()


@app.route('/pyrit_striplive')
def pyrit_striplive() -> str:
    return set_pyrit_striplive()


@app.route('/airgeddon_attack')
def airgeddon() -> str:
    return set_airgeddon()


@app.route('/hcxdumptool_attack')
def hcxdumptool() -> str:
    return set_hcxdumptool()


@app.route('/hcxpcapngtool_hash')
def hcxpcapngtool() -> str:
    return set_hcxpcapngtool()


@app.route('/start_hashcat_mask')
def hashcat_mask() -> str:
    return set_hashcat_mask()


@app.route('/start_hashcat_dict')
def hashcat_dict() -> str:
    return set_hashcat_dict()


@app.route('/start_kismet')
def kismet() -> str:
    return set_kismet()


@app.route('/start_horst')
def horst() -> str:
    return set_horst()


@app.route('/start_tshark')
def tshark() -> str:
    return set_tshark()


@app.route('/start_wireshark')
def wireshark() -> str:
    return set_wireshark()


@app.route('/start_script_sniffer')
def sniffer() -> str:
    return set_sniffer()


@app.route('/start_script_airoscapy')
def airoscapy() -> str:
    return set_airoscapy()


@app.route('/tshark_wlan_beacon')
def tshark_wlan_beacony() -> str:
    return set_tshark_wlan_beacon()


@app.route('/tcpdump_pnl')
def tcpdump_pnl() -> str:
    return set_tcpdump_pnl()


@app.route('/scapy_wifi_scan')
def scapy_wifi_scan() -> str:
    return set_scapy_scan()


@app.route('/tcpdump_eapol')
def tcpdump_eapol() -> str:
    return set_tcpdump_eapol()


@app.route('/scapy-lan-scan')
def lan_scan() -> str:
    return set_scapy_lan_scan()


@app.route('/nmap-lan-scan')
def nmap_scan() -> str:
    return set_nmap_lan_scan()


@app.route('/mac_to_wpspin/<address>', methods=['GET', 'POST'])
def mac_to_wpspin(address: str) -> str:
    pattern_1 = r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'
    pattern_2 = r'^([0-9a-fA-F][0-9a-fA-F]-){5}([0-9a-fA-F][0-9a-fA-F])$'
    pattern_3 = r'^([0-9a-fA-F][0-9a-fA-F]){6}$'
    message = ('<html><h2>Example Format: <font color="green">123456789DF0'
               '</font><p>Example Format: <font color="green">'
               '01:23:45:67:89:AB</font></p><p>Example Format: '
               '<font color="green">01-23-45-67-bc-89</font></p>')
    message += msg_post(17, 'mac')
    if request.method == 'POST':
        address = f"{request.form['mac']}"
    result = any([match(i, address) for i in (pattern_1, pattern_2, pattern_3)])
    if not result:
        return message
    mac = address.replace(':', '').replace('-', '')
    wpspin = get_mac_to_wpspin(mac)
    return (f"<h2>Mac: <font color='blue'>{address}</font>. "
            f"WPSPIN: <font color='blue'>{wpspin}</font></h2>")


@app.route('/name_to_mac/<name>', methods=["GET", "POST"])
def name_to_mac(name: str) -> str:
    if request.method == "POST":
        name = f"{request.form['ap']}"
    elif name == '<name>':
        message = ('<html><h2>Example: <font color="green">ESSID</font>'
                   '<p>Example: <font color="green">ASUS-777</font></p>')
        message += msg_post(50, 'ap')
        return message
    return get_name_to_mac(name.strip())


@app.route('/NetworkManager_stop')
def network_manager_stop() -> str:
    return network_manager_start_stop(0)


@app.route('/NetworkManager_start')
def network_manager_start() -> str:
    return network_manager_start_stop(1)


@app.route('/NetworkManager_read_or_change_conf/<choice>')
def network_manager_read_change(choice: str) -> str:
    return network_manager_read_change_conf(choice)


@app.route('/wpa_supplicant_stop')
def wpa_supplicant_stop() -> str:
    return set_wpa_supplicant_start_stop(0)


@app.route('/wpa_supplicant_start')
def wpa_supplicant_start() -> str:
    return set_wpa_supplicant_start_stop(1)


def status(service: str) -> str:
    color = 'grey'
    if 'inactive' in service:
        color = 'red'
    elif 'active' in service:
        color = 'green'
    return color


@app.route('/NetworkManager_wpa_supplicant_status')
def nm_wpa_supplicant_status() -> str:
    result_nm = get_network_manager_status()
    result_wss = get_wpa_supplicant_status()
    color_nm = status(result_nm)
    color_wss = status(result_wss)
    stat = (f'<h2>NetworkManager status: <font color="{color_nm}">'
            f'{result_nm}</font></h2>')
    stat += (f'<h2><p>WPA SUPPLICANT status: <font color="{color_wss}">'
             f'{result_wss}</font></p></h2>')
    return stat


@app.route("/iwconfig-inxi")
def iwconfig_inxi() -> str:
    return get_iwconfig_inxi()
    

@app.route("/iwconfig-hciconfig")
def iwconfig_hciconfig() -> str:
    return get_iwconfig_hciconfig()


@app.route("/route-netstat")
def route_netstat() -> str:
    return get_route_netstat()


@app.route("/ifconfig")
def ifconfig() -> str:
    return get_ifconfig()


@app.route("/ip_a")
def ip() -> str:
    return get_ip()


@app.route("/iptables")
def iptables() -> str:
    return get_iptables()


@app.route("/iw_dev_wlan_link")
def iw_dev_wlan_link() -> str:
    return get_iw_dev_wlan_link()


@app.route("/lspci_lsusb")
def lspci_lsusb() -> str:
    return get_lspci_lsusb()


@app.route("/rfkill_list")
def rfkill() -> str:
    return get_rfkill_list()
    
    
@app.route("/iw_reg_get")
def iw_reg_get() -> str:
    return get_iw_reg_get()


@app.route("/iw-wlan-info")
def iw_wlan_info() -> str:
    return get_iw_wlan_info()


@app.route("/iw-dev-info")
def iw_dev_info() -> str:
    return get_iw_dev_info()


@app.route("/iw-list")
def iw_list() -> str:
    return get_iw_list()


@app.route("/iwlist-channel")
def iwlist_channel() -> str:
    return get_iwlist_channel()


@app.route("/iwlist-scan")
def iwlist_scan() -> str:
    return get_iwlist_scan()


@app.route("/iw_scan_main")
def iw_scan_main() -> str:
    return get_iw_scan()


@app.route("/iwlist_wlan_scan_ssid")
def iwlist_wlan_scan_ssid() -> str:
    return get_iwlist_wlan_scan_ssid()


@app.route("/cat_proc_net_dev")
def cat_proc_net_dev() -> str:
    return get_cat_proc_net_dev()


@app.route("/ls_sys_class_net")
def ls_sys_class_net() -> str:
    return get_ls_sys_class_net()


@app.route("/nmcli")
def nmcli() -> str:
    return get_networks()
    

@app.route("/wpa_cli")
def wpa_cli() -> str:
    return get_wpa_cli_scan()


@app.route("/wifi-home-connect")
def connect_wifi() -> str:
    return connecting_wifi()


@app.route("/wifi-ap-to-ap-connect")
def connect_ap_to_ap_wifi() -> str:
    return connecting_aps_wifi()


@app.route("/create-ap")
def create_ap() -> str:
    return set_create_ap()
    

@app.route("/ap-up", methods=['GET', 'POST'])
def ap_up() -> str:
    ap, password = '', ''
    message = ("<html><h2>Enter the access point name <font color='brown'>AP</font> and "
               "<font color='brown'>password</font>")
    message += '<html><h2>' + msg_post(30, 'ap')[:-67] + msg_post(30, 'password')[29:]
    if request.method == 'POST':
        ap = f"{request.form['ap']}"
        password = f"{request.form['password']}"
    if not ap or len(password) < 8:
        return message
    return set_ap_up(ap, password)


@app.route("/ap-down")
def ap_down() -> str:
    return set_ap_down()
    

@app.route("/http_server/<port>", methods=['GET', 'POST'])
def http_server(port: str) -> str:
    message = ("<html><h2>Set port from <font color='brown'>0</font> to "
               "<font color='brown'>65535</font>")
    message += msg_post(5, 'port')
    if request.method == 'POST':
        port = f"{request.form['port']}"
    if not str(port).isdigit() or int(port) < 0 or int(port) > 65535:
        return message
    return start_http_server(port)


@app.route("/ps_uptime")
def ps_uptime() -> str:
    return get_ps_uptime()


@app.route("/ls")
def ls() -> str:
    return get_ls()


@app.route("/free_port/<port>", methods=['GET', 'POST'])
def get_proc(port: str) -> str:
    message = ("<html><h2>Set port from <font color='brown'>0</font> to "
               "<font color='brown'>65535</font>")
    message += msg_post(5, 'port')
    if request.method == 'POST':
        port = f"{request.form['port']}"
    if not str(port).isdigit() or int(port) < 0 or int(port) > 65535:
        return message
    processes = get_pids(int(port))[1]
    if not processes:
        return ("<h2><font color='green'>No processes found on this port: "
                f"</font>{port}</h2>")
    processes.insert(0, 'Process: Pid')
    pids = ''
    for process in processes:
        pids += '<p>' + process + '</p>'
    return f"<h2><font color='blue'>{pids}</font></h2>"


@app.route("/system_connections")
def system_connections() -> str:
    return get_system_connections()


@app.route("/dmesg_wlan")
def dmesg_wlan() -> str:
    return get_dmesg_wlan()


@app.route("/single_brute_ap/<essid>", methods=['GET', 'POST'])
def single_brute_ap(essid: str) -> str:
    message = ('<html><h2>Enter the name of the Access Point<p>'
                   'Example Format: <font color="green">ASUS-007</font></p>')
    message += msg_post(50, 'ap')
    if request.method == "POST":
        essid = f"{request.form['ap']}"
    elif request.path == '/single_brute_ap/<essid>':  
        return message
    if not essid:
        return message
    return set_single_brute_ap(essid, wpa_equals_wps=True)


@app.route("/multi_brute_ap/<level>", methods=['GET', 'POST'])
def multi_brute_ap(level: str) -> str:
    pattern = r'\d\d-\d\d'
    message = ('<html><h2>Signal level interval<p>Example Format: '
               '<font color="green">00-30</font></p><p>Example Format: '
               '<font color="green">55-57</font></p><p>Example: '
               '<a href="/multi_brute_ap/30-33">multi_brute_ap/30-33</a></p>')
    message += msg_post(7, 'level')
    if request.method == "POST":
        level = f"{request.form['level']}"
    result = match(pattern, level)
    if result and (int(level[:2]) < int(level[-2:])):
        return set_multi_brute_ap(level)
    return message


@app.route("/brute_width_ap")
def brute_width_ap() -> str:
    return set_brute_width_ap()
