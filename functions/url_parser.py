from urllib.parse import urlparse
from parso import parse

class UrlParser:
    def return_url_parts(self, url):
        url_dic = {}
        parsed_url = urlparse(url)
        protocol = parsed_url[0]
        domains = parsed_url[1]
        domain_l = domains.split(".")
        sub_domain = domain_l[0: -2]
        tld = domain_l[-1]

        url_dic["protocol"] = protocol
        url_dic["domain"] = domains
        url_dic["sub_domain"] = sub_domain
        url_dic["tld"] = tld
        url_dic["path"] = parsed_url[2]

        return url_dic



