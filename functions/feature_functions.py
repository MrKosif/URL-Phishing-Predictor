import re

class FeatureFunctions:
    def having_ip_address(self, url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            '[0-9a-fA-F]{7}', url)  # Ipv6
        if match:
            return 1
        else:
            return 0

    def url_length(self, url):
        return len(url)

    def shortening_service(self, full_url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        full_url)
        if match:
            return 1
        else:
            return 0

    def count_at(self, base_url):
        return base_url.count('@')

    def count_comma(self, base_url):
        return base_url.count(',')

    def count_dollar(self, base_url):
        return base_url.count('$')

    def count_semicolumn(self, url):
        return url.count(';')

    def count_space(self, base_url):
        return base_url.count(' ')+base_url.count('%20')

    def count_and(self, base_url):
        return base_url.count('&')

    def count_double_slash(self, full_url):
        print(full_url)
        list=[x.start(0) for x in re.finditer('//', full_url)]
        if list[len(list)-1]>6:
            return 1
        else:
            return 0
        return full_url.count('//')

    def count_slash(self, full_url):
        return full_url.count('/')

    def count_equal(self, base_url):
        return base_url.count('=')

    def count_exclamation(self, base_url):
        return base_url.count('?')

    def count_underscore(self, base_url):
        return base_url.count('_')

    def count_hyphens(self, base_url):
        return base_url.count('-')

    def count_dots(self, hostname):
        return hostname.count('.')

    def count_colon(self, url):
        return url.count(':')

    def count_star(self, url):
        return url.count('*')

    def count_or(self, url):
        return url.count('|')

    def path_extension(self, url_path):
        if url_path.endswith('.txt'):
            return 1
        return 0

    def count_http_token(self, url_path):
        return url_path.count('http')

    def https_token(self, scheme): ### +
        if scheme == 'https':
            return 0
        return 1

    def ratio_digits(self, hostname):
        return len(re.sub("[^0-9]", "", hostname))/len(hostname)

    def count_tilde(self, full_url):
        if full_url.count('~')>0:
            return 1
        return 0

    def phish_hints(self, url_path, hints): ### +
        count = 0
        for hint in hints:
            count += url_path.lower().count(hint)
        return count

    def tld_in_path(self, tld, path):  ### +
        if path.lower().count(tld)>0:
            return 1
        return 0

    def abnormal_subdomain(self, url):
        if re.search('(http[s]?://(w[w]?|\d))([w]?(\d|-))',url):
            return 1
        return 0

    def domain_in_brand(self, path, allbrand): ### +
        count = 0
        for brand in allbrand:
            count += path.lower().count(brand)
        return count

    def count_subdomain(self, url):
        if len(re.findall("\.", url)) == 1:
            return 1
        elif len(re.findall("\.", url)) == 2:
            return 2
        else:
            return 3

