import datetime
import sys
import time
import traceback
from api.godaddy import Godaddy
from utils.debug import e_print, i_print
from utils.nic_info import get_nic_ipv4_addr, get_nic_ipv6_addr, get_nic_list
from utils.config import Config



def try_update():
    config = Config.load()
    gd = Godaddy.load()

    domain = config['domain']
    local_records = config['records']
    local_record_names = list(map(lambda rec: rec['name'], local_records))

    records = gd.records(domain)

    for record in records:
        record_name = record['name']
        if record_name in local_record_names:
            i_print('trying ', record_name, '.', domain)
            local_record = local_records[local_record_names.index(record_name)]
            i_print('record: ', record)
            i_print('local record: ', local_record)
            record_type = record['type']
            if record_type != local_record['type']:
                e_print('remote record type does not match local record type')
                continue
            record_addr = record['data']
            record_ttl = local_record['ttl']
            if record_type == 'AAAA':
                host_addr = get_nic_ipv6_addr(local_record['nic'])
            elif record_type == 'A':
                host_addr = get_nic_ipv4_addr()
            if not host_addr:
                e_print('get host addr failed')
                continue
            i_print('record_addr: ', record_addr)
            i_print('host_addr: ', host_addr)
            if record_addr == host_addr:
                i_print('addr did not change')
            else:
                new_records = [
                    {
                        "data": host_addr,
                        "ttl": record_ttl,
                    }
                ]
                try:
                    gd.update_record(domain, record_type,
                                     record_name, new_records)
                except Exception as err:
                    e_print('update record failed, exception: ', err)
                    traceback.print_exc()
                    continue
                i_print('addr renewed')
                Config.store(config)


def select_nic():
    nic_list = get_nic_list()
    if not nic_list:
        e_print('get nic list failed')
        exit(-1)
    print("Select a nic below.")
    for i in range(len(nic_list)):
        print(i, ": ", nic_list[i])
    while True:
        try:
            choice = int(input())
            if 0 <= choice < len(nic_list):
                return nic_list[choice]
        except:
            pass
        e_print("Invalid input! Input again.")


def select_domain():
    gd = Godaddy.load()
    domain_list = gd.list(statuses=['ACTIVE', 'PENDING_DNS_ACTIVE'])
    if not domain_list:
        e_print('get domain list failed')
        exit(-1)
    print("Select a domain below.")
    for i in range(len(domain_list)):
        print(i, ': ', domain_list[i]['domain'])
    while True:
        try:
            choice = int(input())
            if 0 <= choice < len(domain_list):
                return domain_list[choice]['domain']
        except:
            pass
        e_print("Invalid input! Input again.")


def select_record(domain):
    gd = Godaddy.load()
    records = gd.records(domain)
    if not records:
        e_print('get record list failed')
        exit(-1)
    new_records = []
    for record in records:
        if record["type"] in ["AAAA", "A"]:
            new_records.append(record)
    records = new_records
    if not records:
        e_print("No records available!")
        exit(-1)
    print("Select names below.")
    for i in range(len(records)):
        print(i, ': ', records[i]['name'])
    while True:
        try:
            choice = int(input())
            if 0 <= choice < len(records):
                choice_record = records[choice]
                record_name = choice_record['name']
                record_type = choice_record['type']
                record_ttl = choice_record['ttl']
                record_nic = ''
                if record_type == 'AAAA':
                    record_nic = select_nic()
                return {
                    'name': record_name,
                    'type': record_type,
                    'ttl': record_ttl,
                    'nic': record_nic
                }
        except Exception as err:
            e_print(err)
            traceback.print_exc()
        e_print("Invalid input! Input again.")


def init_config():
    config = Config.load()
    domain = select_domain()
    config["domain"] = domain
    config['records'] = []
    records = []
    while True:
        record = select_record(domain)
        records.append(record)
        print("0: select more record.")
        print("1: no more record.")
        choice = input()
        if choice.isdigit() and choice == "0":
            pass
        else:
            break
    config['records'] = records
    Config.store(config)


def main():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    args = sys.argv
    if len(args) > 1 and args[1] == 'init':
        init_config()
        exit()
    try_update()
    print('==============================')


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as err:
            e_print(err)
            traceback.print_exc()
        time.sleep(10 * 60)
