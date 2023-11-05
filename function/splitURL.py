import os.path

from tldextract import tldextract

# GLOBAL SETTINGS:
CURRENT_FILE = __file__
F = os.path.dirname(os.path.abspath(CURRENT_FILE))


def getSubdomain_DomainName(URL):
    extracted = tldextract.extract(URL)
    registrable_domain = extracted.registered_domain
    mld = registrable_domain.split('.')[0]
    return mld, registrable_domain


def split_URL(URL):
    domain_name, registrable_domain = getSubdomain_DomainName(URL)
    domain_suffix = registrable_domain.replace(domain_name + ".", "")
    subdomain_name = ""
    if URL.find(domain_name, 1) - 1 > 0:
        subdomain_name = URL[0: URL.find(domain_name, 1) - 1]

    # Get URL protocol:
    urlProtocol = ""
    if URL.find("://") != -1:
        urlProtocol = URL[0: URL.find("://")]

    # Get URL Path:
    URLPath = URL.replace(subdomain_name + ".", "", 1)
    URLPath = URLPath[URLPath.find(registrable_domain) + len(registrable_domain):]
    return urlProtocol, subdomain_name, domain_name, domain_suffix, URLPath


def preprocessing_URL(URL):
    URL = URL.replace("www.", "")
    URL = URL.replace(",", '%2C')
    return URL


def writeHeaderToFile(headers):
    with open(F + "../data/preprocessingURL.csv", 'w') as file:
        file.write(",".join(headers) + "\n")


def writeDataToFile(data):
    for i in range(len(data)):
        try:
            URL = data.loc[i]["domain"]
            URL = preprocessing_URL(URL)
            label = data.loc[i]["label"]
            urlProtocol, subdomain_name, domain_name, domain_suffix, URLPath = split_URL(URL)
        except Exception as e:
            print(data.loc[i]["domain"])
            print(e)
        else:
            with open(F + "../data/preprocessingURL.csv", mode="a", encoding='utf-8') as outFile:
                outFile.write(",".join(
                    [URL, urlProtocol, subdomain_name, domain_name, domain_suffix, URLPath, str(label)]) + "\n")