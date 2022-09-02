from urllib.parse import urlparse
import requests
import time
from bs4 import BeautifulSoup

class Rank:
    def return_url_parts(self, url):
        url_dic = {}
        parsed_url = urlparse(url)
        protocol = parsed_url[0]
        domains = parsed_url[1]
        domain_l = domains.split(".")
        sub_domain = domain_l[0: -2]
        root_domain = domain_l[-2]
        tld = domain_l[-1]

        url_dic["protocol"] = protocol
        url_dic["domain"] = domains
        url_dic["sub_domain"] = sub_domain
        url_dic["root_domain"] = root_domain
        url_dic["tld"] = tld

        return url_dic

    def rank_datas(self, domain, trial):
        alt_list = []

        main_atr = None
        while main_atr is None:
            try:
                page = requests.post("https://www.checkpagerank.net/index.php", {
                "name": domain})
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find(class_="container results")
                main_atr = results.find_all("div", class_="col-lg-12")
            except:
                time.sleep(5)
        
        alt_list.append(main_atr[4].text.strip())
        alt_list.append(main_atr[5].text.strip())
        alt_atr = results.find_all("div", class_="col-md-5")
        
        for page in alt_atr:
            alt_list.append(page.text.strip())
        extra_atr = results.find_all("div", class_="col-sm-11")
        for page in extra_atr:
            alt_list.append(page.text.strip())

        column_list = []
        value_list = []
        for param in alt_list:
            parameter = param.split(": ")[0]
            value = param.split(": ")[-1]
            value_list.append(value)
        
        if value_list[3] == "Page Authority:" and trial == 0:
            return -1
        
        if len(value_list) == 32:
            value_list.pop()
            value_list.pop()
            return value_list

        else:
            return  value_list