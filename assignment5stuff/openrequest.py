def test_open_redirect(base_url, params):
    malicious_url = "http://malicious.com"
    for param in params:
        test_url = f"{base_url}?{param}={malicious_url}"
        response = send_request(test_url)
        if response.status_code == 302 and "malicious.com" in response.headers.get("Location", ""):
            log_vulnerability(test_url, "Open HTTP Redirect Found")