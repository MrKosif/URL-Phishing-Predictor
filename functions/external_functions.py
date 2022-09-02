import whois
import time
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import numpy as np

class ExternalFunctions:

    def expiration_date_len(self, domain):
        try:
            res = whois.query(domain)
            expiration_date = res.expiration_date
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            # Some domains do not have expiration dates. The application should not raise an error if this is the case.
            if expiration_date:
                if type(expiration_date) == list:
                    expiration_date = min(expiration_date)
                return abs((expiration_date - today).days)
            else:
                return 0
        except:
            return -1

    def creation_date_len(self, domain):
        try:
            res = whois.query(domain)
            creation_date = res.creation_date
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            # Some domains do not have expiration dates. The application should not raise an error if this is the case.
            if creation_date:
                if type(creation_date) == list:
                    creation_date = min(creation_date)
                return abs((creation_date - today).days)
            else:
                return 0
        except:
            return -1


        v1 = -1
        v2 = -1
        try:
            host = whois.query(domain)
            hostname = host.domain_name
            expiration_date = host.expiration_date
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            if type(hostname) == list:
                for host in hostname:
                    if re.search(host.lower(), domain):
                        v1 = 0
                v1= 1
            else:
                if re.search(hostname.lower(), domain):
                    v1 = 0
                else:
                    v1= 1  
            if expiration_date:
                if type(expiration_date) == list:
                    expiration_date = min(expiration_date)
                return abs((expiration_date - today).days)
            else:
                v2= 0
        except:
            v1 = 1
            v2 = -1
            return v1, v2
        return v1, v2

    def whois_registered_domain(self, domain):
        try:
            hostname = whois.query(domain).domain_name
            if type(hostname) == list:
                for host in hostname:
                    if re.search(host.lower(), domain):
                        return 0
                return 1
            else:
                if re.search(hostname.lower(), domain):
                    return 0
                else:
                    return 1     
        except:
            return 1

    def registrant_country(self, domain):
        res = whois.query(domain)
        country = res.registrant_country
        if country == None:
            print(f" Country -> {country}")
            country = "Unknown"
        return country

    def registrar(self, domain):
        res = whois.query(domain)
        registrar = res.registrar
        if registrar == None:
            print(f"Registrar -> {registrar}")
            registrar = "Unknown"
        return registrar