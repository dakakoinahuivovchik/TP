import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

TIMEOUT = 5  # secunde, folosit la toate cererile


def short_error(error):
    """Returnează un mesaj scurt de eroare (numele tipului de excepție)."""
    return type(error).__name__


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    # lstrip scoate "/" de la început, deci merge cu sau fără "/"
    return "https://" + host + "/" + path.lstrip("/")


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.exceptions.RequestException as error:
        print("Eroare:", short_error(error))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": short_error(error)}

    # Păstrăm doar tipul (fără "; charset=...")
    content_type = response.headers.get("Content-Type", "unknown").split(";")[0].strip()
    return {
        "status": response.status_code,
        "content_type": content_type,
        "length": len(response.content),
        "server": response.headers.get("Server", "unknown"),
    }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    # 1. Verificăm fiecare site și păstrăm (adresa, rezultatul)
    results = []
    for url in SITES:
        results.append((url, check_site(url)))

    # 2. Păstrăm doar site-urile cu status 200
    working = [(url, info) for url, info in results if info["status"] == 200]

    # 3. Sortăm după length, cel mai mare primul
    working.sort(key=lambda pair: pair[1]["length"], reverse=True)

    for url, info in working:
        print(f"{url} -> {info['status']}, {info['length']} octeți")

    # 4. Rezumat
    ok = len(working)
    failed = len(results) - ok
    print(f"Reușite: {ok} | Eșuate: {failed}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": short_error(error)}

    present = []
    missing = []
    # response.headers nu ține cont de majuscule; ordinea vine din SECURITY_HEADERS
    for header in SECURITY_HEADERS:
        if header in response.headers:
            present.append(header)
        else:
            missing.append(header)

    score = len(present) * 100 // len(SECURITY_HEADERS)
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None
    error = None
    made = 0

    while made < attempts:
        made += 1  # numărăm doar cererile trimise cu adevărat
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as err:
            error = short_error(err)
            continue  # eșec de conexiune/timeout: mai încercăm

        status = response.status_code
        error = None
        if status < 500:
            break  # 2xx, 3xx, 4xx: ne oprim imediat

    result = {"status": status, "attempts": made}
    if status is None:
        result["error"] = error
    return result
