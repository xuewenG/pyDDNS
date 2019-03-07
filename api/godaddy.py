import requests
from utils.debug import *


class Godaddy:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.headers = dict()
        self.baseUrl = 'https://api.godaddy.com'
        self.headers['Accept'] = 'application/json'
        self.headers['Content-Type'] = 'application/json'
        self.headers['Authorization'] = 'sso-key ' + self.key + ':' + self.secret

    # list all domains.
    def list(self, statuses=None):
        i_print('getting domains')
        headers = self.headers
        url = self.baseUrl + '/v1/domains'
        d_print('request url: ', url)
        data = dict()
        data['statuses'] = statuses
        i_print('sending request')
        r = requests.get(url, headers=headers, params=data)
        d_print('encoded url: ', r.url)
        if r.status_code == requests.codes.ok:
            d_print('result', r.json())
            i_print('succeeded')
            return r.json()
        else:
            e_print('list domains failed')
            r.raise_for_status()

    # get the details of the domain provided
    def domain_details(self, domain):
        i_print('getting domain details')
        headers = self.headers
        url = self.baseUrl + '/v1/domains/'+ domain.upper()
        d_print('request url: ', url)
        i_print('sending request')
        r = requests.get(url=url, headers=headers)
        d_print('encoded url: ', r.url)
        if r.status_code == requests.codes.ok:
            d_print('result', r.json())
            i_print('succeeded')
            return r.json()
        else:
            e_print('get domain details failed')
            r.raise_for_status()

    # get all records of the domain provided.
    def records(self, domain):
        i_print('getting domain records')
        headers = self.headers
        url = self.baseUrl + '/v1/domains/' + domain.upper() + '/records'
        d_print('request url: ', url)
        i_print('sending request')
        r = requests.get(url=url, headers=headers)
        d_print('encoded url: ', r.url)
        if r.status_code == requests.codes.ok:
            d_print('result', r.json())
            i_print('succeeded')
            return r.json()
        else:
            e_print('get domain records failed')
            r.raise_for_status()

    def add_records(self, domain, records):
        i_print('adding records by domain')
        headers = self.headers
        url = self.baseUrl + '/v1/domains/' + domain.upper() + '/records'
        d_print('request url: ', url)
        data = records
        d_print('data: ', data)
        i_print('sending request')
        r = requests.patch(url=url, headers=headers, json=data)
        d_print('encoded url: ', r.url)
        if r.status_code == requests.codes.ok:
            d_print('succeeded')
        else:
            e_print('add records by domain failed')
            r.raise_for_status()

    # This method can only change the data and ttl of records. Name and type should be provided.
    def update_record(self, domain, type, name, records):
        i_print('updating record')
        headers = self.headers
        url = self.baseUrl + '/v1/domains/' + domain.upper() + '/records/' + type.upper() + '/' + name.upper()
        d_print('request url: ', url)
        data = records
        d_print('data: ', data)
        i_print('sending requests')
        r = requests.put(url=url, headers=headers, json=data)
        d_print('encoded url: ', r.url)
        if r.status_code == requests.codes.ok:
            i_print('succeeded')
        else:
            e_print('add records by type name failed')
            r.raise_for_status()

