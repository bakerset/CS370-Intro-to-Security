def test_js_vulnerabilities(base_url, endpoints, payloads):
    for endpoint in endpoints:
        for payload in payloads:
            response = send_request(base_url + endpoint, payload)
            if detect_script_execution(response):
                log_vulnerability(endpoint, payload, "JavaScript Execution Detected")
            if check_cookies_for_weakness(response.cookies):
                log_vulnerability(endpoint, payload, "Weak Session Handling Detected")