#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import date, timedelta
import subprocess
import re
import requests
from requests.exceptions import RequestException


def load_urls4check(path):
    try:
        with open(path) as file:
            text_urls = file.read()
            urls_as_list = text_urls.split('\n')
            return urls_as_list
    except FileNotFoundError:
        return None


def is_server_respond_with_200(url):
    try:
        if requests.get(url).ok:
            return True
    except RequestException:
        print("{} - invalid URL\n".format(url))
    else:
        print("{}: not OK".format(url))
        return False


def get_domain_expiration_date(domain_name):
    args = ['whois', domain_name]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    whois_msg = process.communicate()[0].decode('utf-8')
    expiry_date = re.findall(r'Registry Expiry Date: (\d{4}-\d{2}-\d{2})',
                             whois_msg)[0]
    return expiry_date


def get_domain_name(url):
    return re.search(r'\w+\.\w+', url).group(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        urls_list = load_urls4check(sys.argv[1])
        if urls_list is not None:
            for current_url in urls_list:
                if is_server_respond_with_200(current_url):
                    current_domain_name = get_domain_name(current_url)
                    domain_expire_date = get_domain_expiration_date(
                                                        current_domain_name)
                    if domain_expire_date > str(date.today()+
                                                        timedelta(days=30)):
                        exp_date_check = "OK"
                    else:
                        exp_date_check = "Not OK"
                    print("{site_url}: OK\nExpiry date check: {expiry_date}\n"
                          .format(site_url=current_url,
                                  expiry_date=exp_date_check))
        else:
            print('Enter a valid path or filename.')
    else:
        print("You must enter a filename.")
