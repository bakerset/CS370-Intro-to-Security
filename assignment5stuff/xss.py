# Set up browser driver
driver = webdriver.Chrome()

# Target URL
url = "http://localhost/DVWA"

# Test payloads
payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]

# Test each payload
for payload in payloads:
    test_url = f"{url}?input={payload}"  # Append payload to input parameter
    driver.get(test_url)
    if "alert" in driver.page_source:
        print(f"XSS vulnerability found with payload: {payload}")

# Close the driver
driver.quit()