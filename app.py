from flask import Flask, render_template, send_from_directory
from re import match
from functions import Type, Path, TEMPFOLDER
from functions.manager import *

root_path = Path().cwd()
template_path = Path(root_path) / 'template'
app = Flask(__name__, template_folder=template_path)


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
    return render_template('index.html')


@app.route('/template/<path:path>')
def send_template(path):
    return send_from_directory(template_path, path)


@app.route('/help')
def md_help():
    with open('template/help.md', 'r', encoding='utf-8') as text:
        man = text.read()
    return f"<h1><font color='blue'><pre>{man}</pre></font></h1>"


@app.route('/mac_change')
def mac_change() -> str:
    return change_mac()


@app.route('/txpower_change')
def txpower() -> str:
    return change_power()


@app.route('/channel_change/<channel>', methods=['GET'])
def ch(channel) -> str:
    if not str(channel).isdigit() or int(channel) < 1 or int(channel) > 13:
        return ("<h2>Set channel from <font color='brown'>1</font> to "
                "<font color='brown'>13</font></h2>")
    return change_channel(int(channel))


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


@app.route('/wlan_mode_managed')
def mode_managed() -> str:
    return set_mode_managed()


@app.route('/virtual_interface_delete')
def delete_interface() -> str:
    return set_del_mon_interface()


@app.route('/tempfiles_delete')
def delete_tempfiles() -> str:
    path = Path(TEMPFOLDER)
    ext = ['kismet', 'hash', 'log', 'pcap', 'cap', 'csv', 'netxml']
    return set_del_tempfiles(path, ext)


@app.route('/airodump-ng')
def airodump() -> str:
    return set_airodump()


@app.route('/airbase_fake_ap')
def airbase_fake_ap() -> str:
    return set_airbase_fake_ap()


@app.route('/mdk3_fake_ap')
def mdk3_fake_ap() -> str:
    return set_mdk3_fake_ap()


@app.route('/mdk4_deauthentication_all_channel')
def mdk4_deauthentication() -> str:
    return set_mdk4_deauthentication()


@app.route('/aireplay_deauthentication_all_channel')
def aireplay_deauthentication() -> str:
    return set_aireplay_deauthentication()


@app.route('/wifite-reaver')
def wifite() -> str:
    return set_wifite()


@app.route('/wifiphisher')
def wifiphisher() -> str:
    return set_wifiphisher()


@app.route('/waidps')
def waidps() -> str:
    return set_waidps()


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


@app.route('/mac_to_wpspin/<address>', methods=['GET'])
def mac_to_wpspin(address: str) -> str:
    pattern_1 = r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'
    pattern_2 = r'^([0-9a-fA-F][0-9a-fA-F]-){5}([0-9a-fA-F][0-9a-fA-F])$'
    pattern_3 = r'^([0-9a-fA-F][0-9a-fA-F]){6}$'
    message = ('<h2>Example Format: <font color="green">123456789DF0</font>'
               '<p>Example Format: <font color="green">01:23:45:67:89:AB'
               '</font></p><p>Example Format: <font color="green">'
               '01-23-45-67-bc-89</font></p></h2>')
    result = any([match(i, address) for i in (pattern_1, pattern_2, pattern_3)])
    if not result:
        return message
    mac = address.replace(':', '').replace('-', '')
    wpspin = get_mac_to_wpspin(mac)
    return (f"<h2>Mac: <font color='blue'>{address}</font>. "
            f"WPSPIN: <font color='blue'>{wpspin}</font></h2>")


@app.route('/name_to_mac/<name>')
def name_to_mac(name: str) -> str:
    if name == '<name>':
        return ('<h2>Example: <font color="green">ESSID</font>'
                '<p>Example: <font color="green">ASUS-777</font></p></h2>')
    return get_name_to_mac(name)


@app.route('/NetworkManager_stop')
def nm_stop() -> str:
    return network_manager_stop()


@app.route('/NetworkManager_start')
def nm_start() -> str:
    return network_manager_start()


@app.route('/NetworkManager_status')
def nm_status():
    result = get_network_manager_status()[135:163]
    color = 'grey'
    if 'dead' in result:
        color = 'red'
    elif 'running' in result:
        color = 'green'
    return (f'<h2>NetworkManager status: <font color="{color}">'
            f'{result}</font></h2>')


@app.route('/NetworkManager_read_conf')
def nm_read() -> str:
    return network_manager_read_conf()


@app.route('/wpa_supplicant_stop')
def wpa_supplicant_stop() -> str:
    return set_wpa_supplicant_stop()


@app.route('/wpa_supplicant_start')
def wpa_supplicant_start() -> str:
    return set_wpa_supplicant_start()


@app.route('/wpa_supplicant_status')
def wpa_supplicant_status():
    result = get_wpa_supplicant_status()[135:164]
    color = 'grey'
    if 'dead' in result:
        color = 'red'
    elif 'running' in result:
        color = 'green'
    return (f'<h2>WPA SUPPLICANT status: <font color="{color}">'
            f'{result}</font></h2>')


@app.route("/iwconfig")
def iwconfig() -> str:
    return get_iwconfig()


@app.route("/ifconfig")
def ifconfig() -> str:
    return get_ifconfig()


@app.route("/ip_a")
def ip() -> str:
    return get_ip()


@app.route("/iw_dev_wlan_link")
def iw_dev_wlan_link() -> str:
    return get_iw_dev_wlan_link()


@app.route("/lspci_lsusb")
def lspci_lsusb() -> str:
    return get_lspci_lsusb()


@app.route("/rfkill_list")
def rfkill() -> str:
    return get_rfkill_list()


@app.route("/hciconfig")
def hciconfig() -> str:
    return get_hciconfig()


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


@app.route("/iwlist_wlan_scan_ssid")
def iwlist_wlan_scan_ssid() -> str:
    return get_iwlist_wlan_scan_ssid()


@app.route("/nmcli")
def nmcli() -> str:
    return get_networks()


@app.route("/wifi-home-connect")
def connect_wifi() -> str:
    return connecting_wifi()


@app.route("/wifi-ap-to-ap-connect")
def connect_ap_to_ap_wifi() -> str:
    return connecting_aps_wifi()


@app.route("/http_server")
def http_server() -> str:
    return start_http_server()


@app.route("/ps")
def ps() -> str:
    return get_ps()


@app.route("/ls")
def ls() -> str:
    return get_ls()


@app.route("/uptime")
def uptime() -> str:
    return get_uptime()


@app.route("/free_port/<port>", methods=['GET'])
def get_proc(port) -> str:
    if not str(port).isdigit() or int(port) < 0 or int(port) > 65535:
        return ("<h2>Set port from <font color='brown'>0</font> to "
                "<font color='brown'>65535</font></h2>")
    processes = get_pids(int(port))[1]
    if not processes:
        return ("<h2><font color='green'>No processes found on this port: "
                f"</font>{port}</h2>")
    processes.insert(0, 'Process: Pid')
    pids = ''
    for process in processes:
        pids += '<p>' + process + '</p>'
    return f"<h2><font color='blue'>{pids}</font></h2>"
