import re

from sklearn.preprocessing import MinMaxScaler
from tld import get_tld
from urllib.parse import urlparse


def process_tld(url):
    try:
        result = get_tld(url, as_object=True, fail_silently=False, fix_protocol=True)
        primary_domain = result.parsed_url.netloc
    except:
        primary_domain = None
    return primary_domain


def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    return 1 if match else 0


def httpsSecure(url):
    htp = urlparse(url).scheme
    match = str(htp)
    return 1 if match == 'https' else 0


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    return digits


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters += 1
    return letters


def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    return 1 if match else 0


def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    return 1 if match else 0


def featureExtraction(data):
    data['domain'] = data['domain'].replace('www.', '', regex=True)
    data['url_len'] = data['domain'].apply(lambda x: str(len(x)))
    data['registered_domain'] = data['domain'].apply(lambda x: process_tld(x))

    feature = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    for i in feature:
        data[i] = data['domain'].apply(lambda x: x.count(i))

    data['abnormal_url'] = data['domain'].apply(lambda x: abnormal_url(x))
    data['https'] = data['domain'].apply(lambda x: httpsSecure(x))
    data['digits'] = data['domain'].apply(lambda x: digit_count(x))
    data['letters'] = data['domain'].apply(lambda x: letter_count(x))
    data['shortening_service'] = data['domain'].apply(lambda x: shortening_service(x))
    data['having_ip_address'] = data['domain'].apply(lambda x: having_ip_address(x))
    return data




