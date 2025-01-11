# Target URL and credentials
url = "http://localhost/DVWA/login.php"
session_ids = []

# Simulate login to collect session IDs
for _ in range(10):
    response = requests.post(url, data={"username": "admin", "password": "password"})
    cookie = response.cookies.get("PHPSESSID")  # Adjust for actual session cookie name
    session_ids.append(cookie)

# Analyze randomness
print("Collected Session IDs:")
for sid in session_ids:
    print(sid)

# Check predictability (hypothetical logic)
def is_predictable(ids):
    # Example: Check for incremental or repeating patterns
    return all(ids[i] != ids[i + 1] for i in range(len(ids) - 1))
