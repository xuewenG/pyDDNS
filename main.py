import sys
from api.godaddy import Godaddy
from utils.debug import *
from utils.nic_info import get_nic_ipv6_addr, get_nic_list
from utils.config import Config

config = Config.load()
gd = Godaddy(key=config['GD_KEY'], secret=config['GD_SECRET'])


def main():
    domain = config['domain']
    records_to_test = config['records']

    records = gd.records(domain)

    for record in records:
        if record['name'] in records_to_test.keys():
            i_print('record: ', record)
            record_name = record['name']
            record_ipv6_addr = record['data']
            record_type = records_to_test[record_name][1]
            record_ttl = records_to_test[record_name][2]

            host_ipv6_addr = get_nic_ipv6_addr(records_to_test[record_name][0])
            d_print(records_to_test[record_name][0], " : ", host_ipv6_addr)

            if record_ipv6_addr == host_ipv6_addr:
                i_print('addr did not change')
            else:
                new_records = [
                    {
                        "data": host_ipv6_addr,
                        "ttl": record_ttl,
                    }
                ]
                gd.update_record(domain, record_type, record_name, new_records)
                i_print('addr renewed')


def select_nic():
    nic_list = get_nic_list()
    print("Select a nic below.")
    for i in range(len(nic_list)):
        print(i, ": ", nic_list[i])
    while True:
        choice = input()
        if choice.isdigit() and 0 <= int(choice) < len(nic_list):
            return nic_list[int(choice)]
        else:
            e_print("Invalid input! Input again.")


def select_domain():
    domain_list = gd.list(statuses=['ACTIVE', 'PENDING_DNS_ACTIVE'])
    print("Select a domain below.")
    for i in range(len(domain_list)):
        print(i, ': ', domain_list[i]['domain'])
    while True:
        choice = input()
        if choice.isdigit() and 0 <= int(choice) < len(domain_list):
            return domain_list[int(choice)]['domain']
        else:
            e_print("Invalid input! Input again.")


def select_record():
    records = gd.records(config["domain"])
    new_records = []
    for record in records:
        if record["type"] in ["AAAA"]:
            new_records.append(record)
    records = new_records
    if len(records) == 0:
        e_print("No records available!")
        exit(-1)
    print("Select names below.")
    for i in range(len(records)):
        print(i, ': ', records[i]['name'])
    while True:
        choice = input()
        if choice.isdigit() and 0 <= int(choice) < len(records):
            return {records[int(choice)]['name']: [select_nic(),
                                              records[int(choice)]['type'],
                                              records[int(choice)]['ttl']]}
        else:
            e_print("Invalid input! Input again.")


def init_config():
    times = config["times"]
    if times == 0:
        domain = select_domain()
        config["domain"] = domain
        config['records'] = {}
        while True:
            record = select_record()
            config['records'] = {**config['records'], **record}
            print("0: select more record.")
            print("1: no more record.")
            choice = input()
            if choice.isdigit() and choice == "0":
                pass
            else:
                break
        Config.store(config)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            config["times"] = 0
            Config.store(config)
            exit()
    init_config()
    main()
    config["times"] = config["times"] + 1
    Config.store(config)
