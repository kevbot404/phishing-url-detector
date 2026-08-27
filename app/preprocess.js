function normalizeUrl(url) {
    /*
     Make URL parsing correctly recognize URLs that don't contain
     http:// or https://
    */
    url = String(url).trim();

    if (!url) {
        return "";
    }

    if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(url)) {
        url = "http://" + url;
    }

    return url;
}


function getUrlLength(url) {
    return url.length;
}


function getDomain(url) {
    try {
        const parsed = new URL(normalizeUrl(url));
        return parsed.host;
    } catch {
        return "";
    }
}


function getDomainLength(url) {
    return getDomain(url).length;
}


function isDomainIp(url) {
    let domain = getDomain(url);

    domain = domain.split(":")[0];

    const pattern = /^(?:\d{1,3}\.){3}\d{1,3}$/;

    return pattern.test(domain) ? 1 : 0;
}


function getNoOfSubdomain(url) {
    let domain = getDomain(url);

    domain = domain.split(":")[0];

    const parts = domain.split(".");

    // example.com -> 0
    // sub.example.com -> 1
    return Math.max(0, parts.length - 2);
}


function hasObfuscation(url) {
    const suspiciousChars = ["@", "%"];

    return suspiciousChars.some(char => url.includes(char))
        ? 1
        : 0;
}


function getNoOfObfuscatedChar(url) {
    let count = 0;

    for (const char of url) {
        if (char === "%" || char === "@") {
            count++;
        }
    }

    return count;
}


function getObfuscationRatio(url) {
    if (url.length === 0) {
        return 0;
    }

    return getNoOfObfuscatedChar(url) / url.length;
}


function getNoOfLetters(url) {
    let count = 0;

    for (const char of url) {
        if (/[a-zA-Z]/.test(char)) {
            count++;
        }
    }

    return count;
}


function getLetterRatio(url) {
    if (url.length === 0) {
        return 0;
    }

    return getNoOfLetters(url) / url.length;
}


function getNoOfDigits(url) {
    let count = 0;

    for (const char of url) {
        if (/[0-9]/.test(char)) {
            count++;
        }
    }

    return count;
}


function getDigitRatio(url) {
    if (url.length === 0) {
        return 0;
    }

    return getNoOfDigits(url) / url.length;
}


function getNoOfEquals(url) {
    return (url.match(/=/g) || []).length;
}


function getNoOfQuestionMarks(url) {
    return (url.match(/\?/g) || []).length;
}


function getNoOfAmpersands(url) {
    return (url.match(/&/g) || []).length;
}


function getNoOfOtherSpecialChars(url) {
    const specialChars = "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";

    let count = 0;

    for (const char of url) {
        if (specialChars.includes(char)) {
            count++;
        }
    }

    return count;
}


function getSpecialCharRatio(url) {
    if (url.length === 0) {
        return 0;
    }

    return getNoOfOtherSpecialChars(url) / url.length;
}


function isHttps(url) {
    try {
        const parsed = new URL(normalizeUrl(url));

        return parsed.protocol.toLowerCase() === "https:"
            ? 1
            : 0;

    } catch {
        return 0;
    }
}


function extractFeatures(url) {
    
    return [
        getUrlLength(url),
        getDomainLength(url),
        isDomainIp(url),
        getNoOfSubdomain(url),
        hasObfuscation(url),
        getNoOfObfuscatedChar(url),
        getObfuscationRatio(url),
        getNoOfLetters(url),
        getLetterRatio(url),
        getNoOfDigits(url),
        getDigitRatio(url),
        getNoOfEquals(url),
        getNoOfQuestionMarks(url),
        getNoOfAmpersands(url),
        getNoOfOtherSpecialChars(url),
        getSpecialCharRatio(url),
        isHttps(url)
    ];
}