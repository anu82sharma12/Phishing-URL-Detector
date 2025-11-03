import re
import tldextract
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    
    features = [
        len(url),                                      # 0
        url.count('.'),                                # 1
        url.count('/'),                                # 2
        url.count('-'),                                # 3
        url.count('@'),                                # 4
        url.count('?'),                                # 5
        "https" in url.lower(),                        # 6
        "login" in url.lower() or "secure" in url.lower(), # 7
        ext.subdomain != "",                           # 8
        len(ext.domain),                               # 9
        len(ext.suffix),                               # 10
        parsed.path.count('/'),                        # 11
        bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)), # 12 IP
        url.count('%'),                                # 13
        "bit.ly" in url or "tinyurl" in url,           # 14 shortener
        "admin" in url.lower() or "update" in url.lower(), # 15 sensitive
    ]
    return [int(f) for f in features]  # Convert bool → int
