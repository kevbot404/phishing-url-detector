import re
from urllib.parse import urlparse


def normalize_url(url):
    """
    Make urlparse() correctly recognize URLs that don't contain
    http:// or https://.
    """
    url = str(url).strip()

    if not url:
        return ""

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url

    return url


def get_url_length(url):
    return len(url)


def get_domain(url):
    parsed = urlparse(normalize_url(url))
    return parsed.netloc


def get_domain_length(url):
    return len(get_domain(url))


def is_domain_ip(url):
    domain = get_domain(url)

    domain = domain.split(":")[0]

    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    return int(bool(re.match(pattern, domain)))


def get_no_of_subdomain(url):
    domain = get_domain(url)
    domain = domain.split(":")[0]

    parts = domain.split(".")

    # example.com -> 0
    # sub.example.com -> 1
    return max(0, len(parts) - 2)


def has_obfuscation(url):
    suspicious_chars = ["@", "%"]

    return int(
        any(char in url for char in suspicious_chars)
    )


def get_no_of_obfuscated_char(url):
    return sum(
        1
        for char in url
        if char == "%" or char == "@"
    )


def get_obfuscation_ratio(url):
    if len(url) == 0:
        return 0

    return get_no_of_obfuscated_char(url) / len(url)


def get_no_of_letters(url):
    return sum(char.isalpha() for char in url)


def get_letter_ratio(url):
    if len(url) == 0:
        return 0

    return get_no_of_letters(url) / len(url)


def get_no_of_digits(url):
    return sum(char.isdigit() for char in url)


def get_digit_ratio(url):
    if len(url) == 0:
        return 0

    return get_no_of_digits(url) / len(url)


def get_no_of_equals(url):
    return url.count("=")


def get_no_of_question_marks(url):
    return url.count("?")


def get_no_of_ampersands(url):
    return url.count("&")


def get_no_of_other_special_chars(url):
    special_chars = "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    return sum(
        1
        for char in url
        if char in special_chars
    )


def get_special_char_ratio(url):
    if len(url) == 0:
        return 0

    return get_no_of_other_special_chars(url) / len(url)


def is_https(url):
    return int(
        urlparse(normalize_url(url)).scheme.lower() == "https"
    )

def calculate_entropy(url):
    import math

    if len(url) == 0:
        return 0

    freq = {}
    for char in url:
        freq[char] = freq.get(char, 0) + 1

    entropy = 0
    for count in freq.values():
        p = count / len(url)
        entropy -= p * math.log2(p)

    return entropy


def get_tokens(url):
    return re.split(r"[^a-zA-Z0-9]", url)


def get_subdomain(domain):
    parts = domain.split(".")
    if len(parts) > 2:
        return ".".join(parts[:-2])
    return ""


def get_tld(domain):
    parts = domain.split(".")
    if len(parts) > 1:
        return parts[-1]
    return ""


def get_query_param_count(url):
    parsed = urlparse(url)
    if not parsed.query:
        return 0
    return len(parsed.query.split("&"))


POPULAR_TLDS = {
    "com",
    "org",
    "net",
    "edu",
    "gov",
    "io",
    "co",
    "us",
    "uk",
    "ca",
    "de",
    "fr",
    "jp",
    "au",
    "in",
    "br",
    "mx",
    "ru",
    "cn",
    "es",
    "it",
    "nl",
    "se",
    "no",
    "fi",
    "dk",
    "ch",
    "at",
    "be",
    "pt",
    "pl",
    "cz",
    "gr",
    "tr",
    "kr",
    "za",
    "nz",
    "sg",
    "hk",
    "tw",
    "my",
    "th",
    "ph",
    "id",
    "vn",
    "ar",
    "cl",
    "co",
    "pe",
    "ve",
    "ng",
    "ke",
    "gh",
    "eg",
    "ma",
    "dz",
    "tn",
    "sa",
    "ae",
    "il",
    "tr",
}


def get_tld_popularity(tld):
    if tld in POPULAR_TLDS:
        return 1
    return 0


SUSPICIOUS_EXTENSIONS = {
    "exe",
    "dll",
    "bat",
    "cmd",
    "scr",
    "ps1",
    "vbs",
    "js",
    "jar",
    "zip",
    "rar",
    "7z",
    "tar",
    "gz",
    "msi",
    "apk",
    "bin",
    "sh",
    "py",
    "php",
    "asp",
    "aspx",
    "cgi",
    "pl",
    "rb",
}


def has_suspicious_file_extension(url):
    parsed = urlparse(url)
    path = parsed.path
    if not path:
        return 0
    ext = path.split(".")[-1].lower()
    return int(ext in SUSPICIOUS_EXTENSIONS)


def extract_features_dict(url):
    normalized_url = normalize_url(url)
    parsed = urlparse(normalized_url)
    domain = parsed.netloc.split(":")[0]
    subdomain = get_subdomain(domain)
    suffix = get_tld(domain)
    path = parsed.path
    has_ip = is_domain_ip(url)
    tokens = get_tokens(url)
    query_param_count = get_query_param_count(normalized_url)
    digit_count = get_no_of_digits(url)
    numeric_percentage = (digit_count / len(url)) * 100 if len(url) > 0 else 0
    tld_popularity = get_tld_popularity(suffix)
    suspicious_file_extension = has_suspicious_file_extension(normalized_url)

    features = {
        "url_length": len(url),
        "has_ip_address": has_ip,
        "dot_count": url.count("."),
        "https_flag": int(url.startswith("https")),
        "url_entropy": calculate_entropy(url),
        "token_count": len(tokens),
        "subdomain_count": len(subdomain.split(".")) if subdomain else 0,
        "query_param_count": query_param_count,
        "tld_length": len(suffix),
        "path_length": len(path),
        "has_hyphen_in_domain": int("-" in domain),
        "number_of_digits": digit_count,
        "tld_popularity": tld_popularity,
        "suspicious_file_extension": suspicious_file_extension,
        "domain_name_length": len(domain),
        "percentage_numeric_chars": numeric_percentage,
    }

    return features