# SYSTEM = 'arch'
SYSTEM = 'deb'
WLAN, MON = 'wlan1', 'mon0'
AP, PASS = 'HOME', '12345678'
AP_PASS = {'Router_1': '12345678', 'Router_2': '12345678'}
TEMPFOLDER = 'tempfiles'
DUMP = f'{TEMPFOLDER}/dumpfile.pcap'
HASH = f'{TEMPFOLDER}/22000.hash'
FAKE_APS = 'functions/fake_ap.txt'
DEFAULT_PASS = 'functions/default_pass.txt'
AP_ST_LIST = f'{TEMPFOLDER}/ap-st-list.log'
DICTIONARY = '/usr/share/dict/wordlist-probable.txt'
PATH = f'{TEMPFOLDER}/hcxdumptool/./hcxdumptool'
WAIDPS = f'{TEMPFOLDER}/waidps/waidps.py'
WIFIJAMMER = f'{TEMPFOLDER}/wifijammer/wifijammer.py'
FAKEAP = f'{TEMPFOLDER}/fakeAP/fakeAP.py'
FLUXION = f'{TEMPFOLDER}/fluxion'
AIRGEDDON = f'{TEMPFOLDER}/airgeddon/airgeddon.sh'
PNL = 'functions/./pnl.sh'
BEACON = 'functions/./beacon.py'
DEAUTH = 'functions/./deauth.py'
SCAN = 'functions/./wifi-scan.py'
LAN_SCAN = 'functions/scapy-scan.py'
BRUTE_SH = f'{TEMPFOLDER}/s0i37/./wpa_brute-width.sh'
BRUTE_PY = 'functions/wpa_brute.py'
WPATMP = f'{TEMPFOLDER}/wpatmp'
TERMINATOR = "terminator -g $HOME/.config/terminator/config -e"
