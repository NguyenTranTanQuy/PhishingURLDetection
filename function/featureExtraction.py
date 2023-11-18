import re
import socket
import whois
import Levenshtein
import os
import requests
from urllib.parse import urlparse
from os.path import splitext
from tldextract import tldextract
from datetime import datetime

CURRENT_FILE = __file__
F = os.path.dirname(os.path.abspath(CURRENT_FILE))

HINTS = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount', 'dropbox', 'themes', 'plugins', 'signin', 'view', 'invoice', 'new', 'message', 'required', 'verification']

allBrand = []
with open(F + r"/../data/allbrands.txt", "r") as file:
    for line in file:
        allBrand.append(line.strip())


def url_length(url):
    return len(url)


def get_domain_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        return parsed_url.netloc.split(":")[0]
    else:
        return ""


def hostname_length(domain):
    return len(domain)


def count_tilde(url):
    return url.count('~')


def count_exclamation(url):
    return url.count('!')


def count_at(url):
    return url.count('@')


def count_hash(url):
    return url.count('#')


def count_dollar(url):
    return url.count('$')


def count_percentage(url):
    return url.count('%')


def count_caret(url):
    return url.count('^')


def count_and(url):
    return url.count('&')


def count_star(url):
    return url.count('*')


def count_left_parenthesis(url):
    return url.count('(')


def count_right_parenthesis(url):
    return url.count(')')


def count_hyphens(url):
    return url.count('-')


def count_underscore(url):
    return url.count('_')


def count_plus(url):
    return url.count('+')


def count_equal(url):
    return url.count('=')


def count_left_curly_brace(url):
    return url.count('{')


def count_right_curly_brace(url):
    return url.count('}')


def count_left_square_bracket(url):
    return url.count('[')


def count_right_square_bracket(url):
    return url.count(']')


def count_or(url):
    return url.count('|')


def count_backslash(url):
    return url.count('\\')


def count_colon(url):
    return url.count(':')


def count_semicolon(url):
    return url.count(';')


def count_comma(url):
    return url.count(',')


def count_dot(url):
    return url.count('.')


def count_less_than(url):
    return url.count('<')


def count_greater_than(url):
    return url.count('>')


def count_question(url):
    return url.count('?')


def count_slash(url):
    return url.count('/')


def count_double_slash(url):
    if "//" in url:
        result = [x.start(0) for x in re.finditer('//', url)]
        return 1 if result[len(result) - 1] > 6 else 0
    return 0


def count_space(url):
    return url.count(' ') + url.count('%20')


def count_digits(url):
    return len(re.sub("[^0-9]", "", url))


def count_letters(url):
    return len(re.sub("[^a-zA-Z]", "", url))


def digits_ratio(url):
    return count_digits(url) / len(url)


def letters_ratio(url):
    return count_letters(url) / len(url)


def https_token(scheme):
    return 1 if scheme == 'https' else 0


def count_http_token(url_path):
    return url_path.count('http')


def tld_in_path(tld, url_path):
    return 1 if url_path.lower().count(tld) > 0 else 0


def brand_in_path(domain, url_path):
    for brand in allBrand:
        brand = brand.lower().replace(" ", "")
        url_path = url_path.lower()
        if brand in url_path and brand not in domain:
            return 1
    return 0


def tld_in_subdomain(tld, subdomain):
    return 1 if subdomain.lower().count(tld) > 0 else 0


def brand_in_domain(domain):
    return 1 if domain in allBrand else 0


def misspelling_brand_in_domain(domain):
    for brand in allBrand:
        brand = brand.lower().replace(" ", "")
        domain = domain.lower()
        if len(Levenshtein.editops(domain, brand)) < 2:
            return 1
    return 0


def puny_code(url):
    return 1 if url.startswith("http://xn--") or url.startswith("https://xn--") else 0


def char_repeat(words_raw):
    def all_same(items):
        return all(x == items[0] for x in items)
    repeat = {'2': 0, '3': 0, '4': 0, '5': 0}
    part = [2, 3, 4, 5]
    for word in words_raw:
        for char_repeat_count in part:
            for i in range(len(word) - char_repeat_count + 1):
                sub_word = word[i: i + char_repeat_count]
                if all_same(sub_word):
                    repeat[str(char_repeat_count)] += 1
    return sum(list(repeat.values()))


def count_www(words_raw):
    result = 0
    for word in words_raw:
        if word.find('www') != -1:
            result += 1
    return result


def count_com(words_raw):
    result = 0
    for word in words_raw:
        if word.find('com') != -1:
            result += 1
    return result


def port(url):
    if re.search("^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\]):([0-9]+)",url):
        return 1
    return 0


def length_word_raw(words_raw):
    return len(words_raw)


def average_word_length(words_raw):
    if len(words_raw) == 0:
        return 0
    return sum([len(word) for word in words_raw]) / len(words_raw)


def longest_word_length(words_raw):
    if len(words_raw) == 0:
        return 0
    return max([len(word) for word in words_raw])


def shortest_word_length(words_raw):
    if len(words_raw) == 0:
        return 0
    return min([len(word) for word in words_raw])


def prefix_suffix(url):
    return 1 if re.findall(r"https?://[^\-]+-[^\-]+/", url) else 0


def count_subdomain(url):
    extracted_info = tldextract.extract(url)

    combined_domain = f"{extracted_info.subdomain}.{extracted_info.domain}"

    subdomain_count = len(combined_domain.split('.'))

    return subdomain_count

# url_to_test = "https://www.baltazarpresentes.com.br/example"
# domain_to_test = "baltazarpresentes.com.br"
# result == 1 => Security threat detected!
# result == 0 => No security threat detected
# result == 2 => Error during the security check


def statistical_report(url, domain):
    url_match = re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address = socket.gethostbyname(domain)
        ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                           '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                           '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                           '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                           '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                           '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
        if url_match or ip_match:
            return 1
        else:
            return 0
    except:
        return 2


suspicious_tlds = ['fit','tk', 'gp', 'ga', 'work', 'ml', 'date', 'wang', 'men', 'icu', 'online', 'click', # Spamhaus
        'country', 'stream', 'download', 'xin', 'racing', 'jetzt',
        'ren', 'mom', 'party', 'review', 'trade', 'accountants',
        'science', 'work', 'ninja', 'xyz', 'faith', 'zip', 'cricket', 'win',
        'accountant', 'realtor', 'top', 'christmas', 'gdn', # Shady Top-Level Domains
        'link', # Blue Coat Systems
        'asia', 'club', 'la', 'ae', 'exposed', 'pe', 'go.id', 'rs', 'k12.pa.us', 'or.kr',
        'ce.ke', 'audio', 'gob.pe', 'gov.az', 'website', 'bj', 'mx', 'media', 'sa.gov.au'] # statistics


def suspicious_tld(tld):
    return 1 if tld in suspicious_tlds else 0


def count_phishing_hints(url_path):
    result = 0
    for hint in HINTS:
        result += url_path.lower().count(hint)
    return result


def abnormal_subdomain(url):
    return 1 if re.search('(http[s]?://(w[w]?|\d))([w]?(\d|-))',url) else 0

def path_extension(url_path):
    has_extension = splitext(url_path)[1] != ""
    return int(has_extension)


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


def is_domain_expired(url):
    try:
        domain_info = whois.whois(url)
        expiration_date = domain_info.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if expiration_date:
            current_date = datetime.now()
            return current_date > expiration_date
    except whois.parser.PywhoisError as e:
        return 2
    return 1


def get_domain_age(url):
    try:
        domain_info = whois.whois(url)
        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            current_date = datetime.now()
            age = current_date - creation_date
            return age.days
    except whois.parser.PywhoisError as e:
        return -1
    return 0


def check_redirects(url):
    try:
        response = requests.head(url, allow_redirects=True)
        final_url = response.url
        if url != final_url:
            return 1
        else:
            return 0
    except requests.RequestException as e:
        return 2


def words_raw_extraction(domain, subdomain, url_path):
    w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
    w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())
    w_url_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", url_path.lower())
    raw_words = w_domain + w_url_path + w_subdomain
    w_host = w_domain + w_subdomain
    raw_words = list(filter(None, raw_words))
    return raw_words, list(filter(None, w_host)), list(filter(None, w_url_path))


def featureExtraction(data):
    count = 0

    data["scheme"] = data["url"].apply(lambda x: urlparse(x).scheme)
    data['domain'] = data['url'].apply(lambda x: get_domain_from_url(x))
    data["subdomain"] = data["url"].apply(lambda x: tldextract.extract(x).subdomain)
    data["second_domain"] = data["url"].apply(lambda x: tldextract.extract(x).domain)
    data["tld"] = data["url"].apply(lambda x: tldextract.extract(x).suffix)
    data["url_path"] = data["url"].apply(lambda x: urlparse(x).path)
    data["words_raw"] = data.apply(lambda x: words_raw_extraction(x["url"], x["subdomain"], x["url_path"]), axis=1)

    data[url_length.__name__] = data['url'].apply(lambda x: url_length(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[hostname_length.__name__] = data['url'].apply(lambda x: hostname_length(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_at.__name__] = data['url'].apply(lambda x: count_at(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_hash.__name__] = data['url'].apply(lambda x: count_hash(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_dollar.__name__] = data['url'].apply(lambda x: count_dollar(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_percentage.__name__] = data['url'].apply(lambda x: count_percentage(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_and.__name__] = data['url'].apply(lambda x: count_and(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_star.__name__] = data['url'].apply(lambda x: count_star(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_exclamation.__name__] = data['url'].apply(lambda x: count_exclamation(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_caret.__name__] = data['url'].apply(lambda x: count_caret(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_left_parenthesis.__name__] = data['url'].apply(lambda x: count_left_parenthesis(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_right_parenthesis.__name__] = data['url'].apply(lambda x: count_right_parenthesis(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_hyphens.__name__] = data['url'].apply(lambda x: count_hyphens(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_underscore.__name__] = data['url'].apply(lambda x: count_underscore(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_plus.__name__] = data['url'].apply(lambda x: count_plus(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_hash.__name__] = data['url'].apply(lambda x: count_hash(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_equal.__name__] = data['url'].apply(lambda x: count_equal(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_left_curly_brace.__name__] = data['url'].apply(lambda x: count_left_curly_brace(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_right_curly_brace.__name__] = data['url'].apply(lambda x: count_right_curly_brace(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_left_square_bracket.__name__] = data['url'].apply(lambda x: count_left_square_bracket(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_right_square_bracket.__name__] = data['url'].apply(lambda x: count_right_square_bracket(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_or.__name__] = data['url'].apply(lambda x: count_or(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_backslash.__name__] = data['url'].apply(lambda x: count_backslash(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_colon.__name__] = data['url'].apply(lambda x: count_colon(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_semicolon.__name__] = data['url'].apply(lambda x: count_semicolon(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_tilde.__name__] = data['url'].apply(lambda x: count_tilde(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_comma.__name__] = data['url'].apply(lambda x: count_comma(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_dot.__name__] = data['url'].apply(lambda x: count_dot(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_less_than.__name__] = data['url'].apply(lambda x: count_less_than(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_greater_than.__name__] = data['url'].apply(lambda x: count_greater_than(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_question.__name__] = data['url'].apply(lambda x: count_question(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_slash.__name__] = data['url'].apply(lambda x: count_slash(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_double_slash.__name__] = data['url'].apply(lambda x: count_double_slash(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_space.__name__] = data['url'].apply(lambda x: count_space(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_digits.__name__] = data['url'].apply(lambda x: count_digits(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_letters.__name__] = data['url'].apply(lambda x: count_letters(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[digits_ratio.__name__] = data['url'].apply(lambda x: digits_ratio(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[letters_ratio.__name__] = data['url'].apply(lambda x: letters_ratio(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[https_token.__name__] = data['scheme'].apply(lambda x: https_token(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_http_token.__name__] = data['url_path'].apply(lambda x: count_http_token(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[tld_in_path.__name__] = data.apply(lambda x: tld_in_path(x['tld'], x['url_path']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[brand_in_path.__name__] = data.apply(lambda x: brand_in_path(x['second_domain'], x['url_path']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[tld_in_subdomain.__name__] = data.apply(lambda x: tld_in_subdomain(x['tld'], x['subdomain']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[brand_in_domain.__name__] = data.apply(lambda x: brand_in_domain(x['second_domain']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[misspelling_brand_in_domain.__name__] = data.apply(lambda x: misspelling_brand_in_domain(x['second_domain']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[puny_code.__name__] = data['url'].apply(lambda x: puny_code(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[char_repeat.__name__] = data["words_raw"].apply(lambda x: char_repeat(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_www.__name__] = data["words_raw"].apply(lambda x: count_www(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_com.__name__] = data["words_raw"].apply(lambda x: count_com(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[port.__name__] = data["url"].apply(lambda x: port(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[length_word_raw.__name__] = data["words_raw"].apply(lambda x: length_word_raw(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[average_word_length.__name__] = data["words_raw"].apply(lambda x: average_word_length(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[longest_word_length.__name__] = data["words_raw"].apply(lambda x: longest_word_length(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[shortest_word_length.__name__] = data["words_raw"].apply(lambda x: shortest_word_length(x[0]))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[prefix_suffix.__name__] = data["url"].apply(lambda x: prefix_suffix(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_subdomain.__name__] = data["url"].apply(lambda x: count_subdomain(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[statistical_report.__name__] = data.apply(lambda x: statistical_report(x['url'], x['domain']), axis=1)
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[suspicious_tld.__name__] = data["tld"].apply(lambda x: suspicious_tld(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[count_phishing_hints.__name__] = data["url_path"].apply(lambda x: count_phishing_hints(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[abnormal_subdomain.__name__] = data["url"].apply(lambda x: abnormal_subdomain(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[path_extension.__name__] = data["url_path"].apply(lambda x: path_extension(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[shortening_service.__name__] = data["url"].apply(lambda x: shortening_service(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[having_ip_address.__name__] = data["url"].apply(lambda x: having_ip_address(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[is_domain_expired.__name__] = data["url"].apply(lambda x: is_domain_expired(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[get_domain_age.__name__] = data["url"].apply(lambda x: get_domain_age(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    data[check_redirects.__name__] = data["url"].apply(lambda x: check_redirects(x))
    count += 1
    print("Completed Extraction: " + str(count) + "/65")

    return data
