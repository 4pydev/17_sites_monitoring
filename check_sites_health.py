#!/usr/bin/env python3

import sys
from datetime import date, timedelta, datetime
import subprocess
import re
import requests
from requests.exceptions import RequestException


def load_urls4check(path):
    with open(path) as file:
        text_urls = file.read()
        urls_as_list = text_urls.split()
        return urls_as_list


def get_site_status(url):
    try:
        if requests.get(url).ok:
            return True
    except RequestException:
        return False
    else:
        return False


def get_domain_name(url):
    try:
        return re.search(r'\w+\.\w+', url).group(0)
    except AttributeError:
        return None


def get_domain_expiration_status(domain_name):
    try:
        args = ['whois', domain_name]
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        whois_msg = process.communicate()[0].decode('utf-8')
        expiry_date = re.findall(r'Registry Expiry Date: (\d{4}-\d{2}-\d{2})',
                                 whois_msg)[0]
        return True if datetime.strptime(expiry_date, '%Y-%m-%d').date() > \
                       date.today() + timedelta(days=30) \
            else False
    except TypeError:
        return False


def print_site_status(url, site_status, expiration_status):
    print("{site_url}: {site_status}\nExpiry date check: {expiry_status}\n"
          .format(site_url=url,
                  site_status="OK" if site_status else "Not OK",
                  expiry_status="OK" if expiration_status else "Not OK"))


if __name__ == '__main__':
    try:
        urls_list = load_urls4check(sys.argv[1])
        for current_url in urls_list:
            site_status = get_site_status(current_url)
            expiration_status = get_domain_expiration_status(
                                    get_domain_name(current_url))
            print_site_status(url=current_url,
                              site_status=site_status,
                              expiration_status=expiration_status)
    except IndexError:
        print("You must enter a filename.")
    except FileNotFoundError:
        print("Enter a valid filename.")
