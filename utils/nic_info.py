import psutil
from .debug import d_print
from socket import AddressFamily


def get_nic_list():
    info = psutil.net_if_stats()
    d_print(info)
    nic_list = []
    for i in info:
        if i[:6] not in ["Virtua", "Loopba", "VMware"] and info[i][0]:
            nic_list.append(i)
    return nic_list


def get_nic_ipv6_addr(nic):
    info = psutil.net_if_addrs()
    d_print(info)
    for name, v in info.items():
        for item in v:
            # item[0] == AddressFamily.AF_INET and item[1] != '127.0.0.1' and item[1][:3] not in ["169", "192", "10."]
            if name == nic and item[0] == AddressFamily.AF_INET6 and item[1][0] in ["2", "3"]:
                    return item[1]
