import requests
import psutil
from socket import AddressFamily
from .debug import d_print


def is_target_nic(name):
    prefix_list = ["Virtua", "Loopba", "VMware", "docker", "veth"]
    name_list = ["lo", "wg0"]
    for prefix in prefix_list:
        if name.startswith(prefix):
            return False
    return name not in name_list


def get_nic_list():
    info = psutil.net_if_stats()
    nic_list = []
    for i in info:
        if is_target_nic(i) and info[i][0]:
            nic_list.append(i)
    return nic_list


def get_nic_ipv6_addr(nic):
    info = psutil.net_if_addrs()
    for name, v in info.items():
        for item in v:
            # item[0] == AddressFamily.AF_INET and item[1] != '127.0.0.1' and item[1][:3] not in ["169", "192", "10."]
            if name == nic and item[0] == AddressFamily.AF_INET6 and item[1][0] in ["2", "3"]:
                return item[1]


def get_nic_ipv4_addr():
    try:
        url = 'https://api.ipify.org/?format=json'
        r = requests.get(url)
        return r.json()['ip']
    except Exception:
        pass
