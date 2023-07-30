import os.path
from flask import Flask, render_template, send_from_directory
from functions import Type
from functions.manager import *

root_path = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(root_path, 'template')
css_path = os.path.join(template_path, 'css')
img_path = os.path.join(template_path, 'img')
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


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(css_path, path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(img_path, path)


@app.route('/mac_change')
def mac_change() -> str:
    return change_mac()


@app.route('/txpower_change')
def txpower() -> str:
    return change_power()


@app.route('/channel_change/<int:channel>', methods=['GET'])
def ch(channel: int) -> str:
    if channel < 1 or channel > 13:
        return "<h2><font color='brown'>Set channel from 1 to 13</font></h2>"
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


@app.route('/wlan_mode_managed')
def mode_managed() -> str:
    return set_mode_managed()


@app.route('/virtual_interface_delete')
def delete_interface() -> str:
    return set_del_mon_interface()


@app.route('/airodump-ng')
def airodump() -> str:
    return set_airodump()


@app.route('/airbase_fake_ap')
def airbase_fake_ap() -> str:
    return set_airbase_fake_ap()


@app.route('/mdk3_fake_ap')
def mdk3_fake_ap() -> str:
    return set_mdk3_fake_ap()


@app.route('/mdk3_deauthentication_all_channel')
def mdk3_deauthentication() -> str:
    return set_mdk3_deauthentication()


@app.route('/aireplay_deauthentication_all_channel')
def aireplay_deauthentication() -> str:
    return set_aireplay_deauthentication()


@app.route('/pyrit_striplive')
def pyrit_striplive() -> str:
    return set_pyrit_striplive()


@app.route('/hcxdumptool_attack')
def hcxdumptool() -> str:
    return set_hcxdumptool()


@app.route('/hcxpcapngtool_hash')
def hcxpcapngtool() -> str:
    return set_hcxpcapngtool()


@app.route('/start_hashcat')
def hashcat() -> str:
    return set_hashcat()


@app.route('/mac_to_wpspin/<address>', methods=['GET'])
def mac_to_wpspin(address: str) -> str:
    if address == '<address>':
        return '<h2>Example Format: 123456789DF0</h2>'
    return get_mac_to_wpspin(address)


@app.route('/name_to_mac/<name>', methods=['GET'])
def name_to_mac(name: str) -> str:
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


@app.route("/iwconfig", methods=["GET"])
def iwconfig() -> str:
    return get_iwconfig()


@app.route("/ifconfig", methods=["GET"])
def ifconfig() -> str:
    return get_ifconfig()


@app.route("/iw-wlan-info", methods=["GET"])
def iw_wlan_info() -> str:
    return get_iw_wlan_info()


@app.route("/iw-dev-info", methods=["GET"])
def iw_dev_info() -> str:
    return get_iw_dev_info()


@app.route("/iw-list", methods=["GET"])
def iw_list() -> str:
    return get_iw_list()


@app.route("/iwlist-scan", methods=["GET"])
def iwlist_scan() -> str:
    return get_iwlist_scan()


@app.route("/iwlist_wlan_scan_ssid", methods=["GET"])
def iwlist_wlan_scan_ssid() -> str:
    return get_iwlist_wlan_scan_ssid()


@app.route("/nmcli", methods=["GET"])
def nmcli() -> str:
    return get_networks()


@app.route("/wifi-ap-connect", methods=["GET"])
def connect_wifi() -> str:
    return connecting_wifi()


@app.route("/ps", methods=["GET"])
def ps() -> str:
    return get_ps()


@app.route("/ls", methods=["GET"])
def ls() -> str:
    return get_ls()


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    return get_uptime()


@app.route("/free_port/<int:port>", methods=['GET'])
def get_proc(port: int) -> str:
    proc = get_pids(port)[1]
    if not proc:
        return ("<h2><font color='green'>No processes found on this port: "
                f"</font>{port}</h2>")
    return f"<h2><font color='blue'><pre>{proc}</pre></font></h2>"
