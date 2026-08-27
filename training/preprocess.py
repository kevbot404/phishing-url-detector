import re
from urllib.parse import urlparse


def get_url_length(url):
    return len(url)


def get_domain(url):
    return urlparse(url).netloc


def get_domain_length(url):
    return len(get_domain(url))


def is_domain_ip(url):
    domain = get_domain(url)

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
    return int(any(char in url for char in suspicious_chars))


def get_no_of_obfuscated_char(url):
    return sum(1 for char in url if char == "%" or char == "@")


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
        1 for char in url
        if char in special_chars
    )


def get_special_char_ratio(url):
    if len(url) == 0:
        return 0

    return get_no_of_other_special_chars(url) / len(url)


def is_https(url):
    return int(urlparse(url).scheme.lower() == "https")


def extract_features(url):
    """
    Extract features in the exact order expected by the ML model.
    """

    return [
        get_url_length(url),
        get_domain_length(url),
        is_domain_ip(url),
        get_no_of_subdomain(url),
        has_obfuscation(url),
        get_no_of_obfuscated_char(url),
        get_obfuscation_ratio(url),
        get_no_of_letters(url),
        get_letter_ratio(url),
        get_no_of_digits(url),
        get_digit_ratio(url),
        get_no_of_equals(url),
        get_no_of_question_marks(url),
        get_no_of_ampersands(url),
        get_no_of_other_special_chars(url),
        get_special_char_ratio(url),
        is_https(url),
    ]