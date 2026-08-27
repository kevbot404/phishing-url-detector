function normalizeUrl(url) {
    url = String(url).trim();

    if (!url) return "";

    if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(url)) {
        url = "http://" + url;
    }

    return url;
}

function parseUrl(url) {
    return new URL(normalizeUrl(url));
}

function getUrlLength(url) {
    return url.length;
}

function getDomain(url) {
    return parseUrl(url).host;
}

function getDomainLength(url) {
    return getDomain(url).length;
}

function isDomainIp(url) {
    let domain = getDomain(url).split(":")[0];
    let pattern = /^(?:\d{1,3}\.){3}\d{1,3}$/;

    return pattern.test(domain) ? 1 : 0;
}

function getNoOfSubdomain(url) {
    let domain = getDomain(url).split(":")[0];
    let parts = domain.split(".");

    return Math.max(0, parts.length - 2);
}

function hasObfuscation(url) {
    return ["@", "%"].some(c => url.includes(c)) ? 1 : 0;
}

function getNoOfObfuscatedChar(url) {
    return [...url].filter(c => c === "%" || c === "@").length;
}

function getObfuscationRatio(url) {
    return url.length === 0 ? 0 : getNoOfObfuscatedChar(url) / url.length;
}

function getNoOfLetters(url) {
    return [...url].filter(c => /[a-zA-Z]/.test(c)).length;
}

function getLetterRatio(url) {
    return url.length === 0 ? 0 : getNoOfLetters(url) / url.length;
}

function getNoOfDigits(url) {
    return [...url].filter(c => /\d/.test(c)).length;
}

function getDigitRatio(url) {
    return url.length === 0 ? 0 : getNoOfDigits(url) / url.length;
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
    let specialChars = "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";

    return [...url].filter(c => specialChars.includes(c)).length;
}

function getSpecialCharRatio(url) {
    return url.length === 0 ? 0 : getNoOfOtherSpecialChars(url) / url.length;
}

function isHttps(url) {
    return parseUrl(url).protocol.toLowerCase() === "https:" ? 1 : 0;
}

function calculateEntropy(url) {
    if (url.length === 0) return 0;

    let freq = {};

    for (let char of url) {
        freq[char] = (freq[char] || 0) + 1;
    }

    let entropy = 0;

    for (let count of Object.values(freq)) {
        let p = count / url.length;
        entropy -= p * Math.log2(p);
    }

    return entropy;
}

function getTokens(url) {
    return url.split(/[^a-zA-Z0-9]/);
}

function getSubdomain(domain) {
    let parts = domain.split(".");

    if (parts.length > 2) {
        return parts.slice(0, -2).join(".");
    }

    return "";
}

function getTld(domain) {
    let parts = domain.split(".");

    return parts.length > 1 ? parts[parts.length - 1] : "";
}

function getQueryParamCount(url) {
    let parsed = parseUrl(url);

    if (!parsed.search) return 0;

    return parsed.search.substring(1).split("&").length;
}


const POPULAR_TLDS = new Set([
    "com","org","net","edu","gov","io","co","us","uk","ca",
    "de","fr","jp","au","in","br","mx","ru","cn","es","it",
    "nl","se","no","fi","dk","ch","at","be","pt","pl","cz",
    "gr","tr","kr","za","nz","sg","hk","tw","my","th","ph",
    "id","vn","ar","cl","pe","ve","ng","ke","gh","eg","ma",
    "dz","tn","sa","ae","il"
]);


function getTldPopularity(tld) {
    return POPULAR_TLDS.has(tld) ? 1 : 0;
}


const SUSPICIOUS_EXTENSIONS = new Set([
    "exe","dll","bat","cmd","scr","ps1","vbs","js","jar",
    "zip","rar","7z","tar","gz","msi","apk","bin","sh",
    "py","php","asp","aspx","cgi","pl","rb"
]);


function hasSuspiciousFileExtension(url) {
    let parsed = parseUrl(url);
    let path = parsed.pathname;

    if (!path) return 0;

    let ext = path.split(".").pop().toLowerCase();

    return SUSPICIOUS_EXTENSIONS.has(ext) ? 1 : 0;
}


function extractFeaturesDict(url) {
    let normalizedUrl = normalizeUrl(url);
    let parsed = parseUrl(normalizedUrl);

    let domain = parsed.hostname;
    let subdomain = getSubdomain(domain);
    let suffix = getTld(domain);
    let path = parsed.pathname;

    let hasIp = isDomainIp(url);
    let tokens = getTokens(url);

    let queryParamCount = getQueryParamCount(normalizedUrl);

    let digitCount = getNoOfDigits(url);

    let numericPercentage =
        url.length > 0 ? (digitCount / url.length) * 100 : 0;

    let tldPopularity = getTldPopularity(suffix);

    let suspiciousFileExtension =
        hasSuspiciousFileExtension(normalizedUrl);


    return {
        url_length: url.length,
        has_ip_address: hasIp,
        dot_count: (url.match(/\./g) || []).length,
        https_flag: url.startsWith("https") ? 1 : 0,
        url_entropy: calculateEntropy(url),
        token_count: tokens.length,
        subdomain_count: subdomain ? subdomain.split(".").length : 0,
        query_param_count: queryParamCount,
        tld_length: suffix.length,
        path_length: path === "/" ? 0 : path.length,
        has_hyphen_in_domain: domain.includes("-") ? 1 : 0,
        number_of_digits: digitCount,
        tld_popularity: tldPopularity,
        suspicious_file_extension: suspiciousFileExtension,
        domain_name_length: domain.length,
        percentage_numeric_chars: numericPercentage
    };
}

function extractFeatures(url) {
    const featureDict = extractFeaturesDict(url);

    return [
        featureDict.url_length,
        featureDict.has_ip_address,
        featureDict.dot_count,
        featureDict.https_flag,
        featureDict.url_entropy,
        featureDict.token_count,
        featureDict.subdomain_count,
        featureDict.query_param_count,
        featureDict.tld_length,
        featureDict.path_length,
        featureDict.has_hyphen_in_domain,
        featureDict.number_of_digits,
        featureDict.tld_popularity,
        featureDict.suspicious_file_extension,
        featureDict.domain_name_length,
        featureDict.percentage_numeric_chars
    ];
}