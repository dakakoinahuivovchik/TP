from checker import (build_url, is_https, show_response, check_site,
                     scan_sites, check_headers, retry_check)

# Partea 1: build_url și is_https
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url (cu /):", build_url("example.com", "/login"))
print("Partea 1, is_https (https):", is_https("https://example.com"))
print("Partea 1, is_https (http):", is_https("http://example.com"))

# Partea 2: show_response
print("Partea 2, show_response (site care merge):")
show_response("https://example.com")
print("Partea 2, show_response (site inexistent):")
show_response("http://this-site-does-not-exist.invalid")

# Partea 3: check_site
print("Partea 3, check_site (merge):", check_site("https://example.com"))
print("Partea 3, check_site (inexistent):",
      check_site("http://this-site-does-not-exist.invalid"))
print("Partea 3, check_site (prea lent):", check_site("https://httpbin.org/delay/10"))

# Partea 4: scan_sites
print("Partea 4, scan_sites:")
scan_sites()

# Partea 5: check_headers
print("Partea 5, check_headers (un antet):",
      check_headers("https://httpbin.org/response-headers?x-frame-options=DENY"))
print("Partea 5, check_headers (două antete):",
      check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers (inexistent):",
      check_headers("http://this-site-does-not-exist.invalid"))
