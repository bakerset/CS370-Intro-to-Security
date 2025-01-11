def test_authorization_bypass(base_url, endpoints, sessions):
    for endpoint in endpoints:
        for role, session in sessions.items():
            response = send_request(base_url + endpoint, session)
            if response.status_code == 200 and role != "admin":
                log_vulnerability(endpoint, role, "Authorization Bypass Detected")
