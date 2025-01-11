# Step 1: Login to application
session = requests.Session()
login_data = {"username": "admin", "password": "password"}
session.post("http://localhost/DVWA/login.php", data=login_data)

# Step 2: Get a sensitive page
response = session.get("http://localhost/DVWA/vulnerabilities/csrf/")
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Attempt to modify request without a CSRF token
data = {"action": "malicious_action"}  # Missing CSRF token
vulnerable_response = session.post("http://localhost/DVWA/vulnerabilities/csrf/", data=data)

# Step 4: Check if the action succeeded
if "Success" in vulnerable_response.text:
    print("CSRF vulnerability detected!")
else:
    print("No vulnerability detected.")