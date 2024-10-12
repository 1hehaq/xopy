import random
import time
import os
import json
from itertools import cycle
import requests
import concurrent.futures
from colorama import init, Fore, Style
import readline
import glob
import threading

init(autoreset=True)

CACHE_FILE = ".active-proxies.json"
MAX_CONCURRENT_TESTS = 50
TEST_TIMEOUT = 5

def display_banner():
    banner = """
    ─┐ ┬┌─┐┌─┐┬ ┬
    ┌┴┬┘│ │├─┘└┬┘
    ┴ └─└─┘┴   ┴ 
    
  Created by @1hehaq
    """
    print(f"{Fore.CYAN}{banner}{Fore.RESET}")

def path_completer(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(path_completer)

def load_proxies():
    while True:
        file_path = input(f"\n{Fore.YELLOW}[→] Enter the path to your proxy list file:{Fore.RESET} ").strip()
        try:
            with open(file_path, "r") as file:
                proxies = [line.strip() for line in file.readlines() if line.strip()]
            if proxies:
                print(f"{Fore.GREEN}[✓] Successfully loaded {len(proxies)} proxies.")
                return proxies
            else:
                print(f"{Fore.RED}[✗] Error: The file is empty. Please provide a file with proxies.")
        except FileNotFoundError:
            print(f"{Fore.RED}[✗] Error: File not found. Please provide a valid file path.")

def is_proxy_working(proxy):
    try:
        response = requests.get("https://api.ipify.org", proxies={"http": proxy, "https": proxy}, timeout=TEST_TIMEOUT)
        return response.status_code == 200
    except:
        return False

def test_proxy(proxy):
    if is_proxy_working(proxy):
        return proxy
    return None

def get_working_proxies(proxy_list):
    working_proxies = load_cached_proxies()
    proxies_to_test = list(set(proxy_list) - set(working_proxies))

    if not proxies_to_test:
        print(f"{Fore.GREEN}[✓] All proxies are cached. Skipping tests.")
        return working_proxies

    print(f"{Fore.YELLOW}[‼] Testing {len(proxies_to_test)} proxies, Take a deep breathe..\n")

    progress_lock = threading.Lock()
    progress_counter = 0
    total_proxies = len(proxies_to_test)

    def test_and_update(proxy):
        nonlocal progress_counter
        result = test_proxy(proxy)
        with progress_lock:
            progress_counter += 1
            print(f"\r{Fore.YELLOW}[↯] {Fore.CYAN}Progress: {Fore.YELLOW}{progress_counter}/{total_proxies}", end="", flush=True)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TESTS) as executor:
        results = list(executor.map(test_and_update, proxies_to_test))

    print()

    new_working_proxies = [proxy for proxy in results if proxy]
    working_proxies.extend(new_working_proxies)

    save_cached_proxies(working_proxies)

    print(f"{Fore.GREEN}    ↪ Found {len(new_working_proxies)} new working proxies.")
    print(f"{Fore.GREEN}    ↪ Total working proxies: {len(working_proxies)}")

    return working_proxies

def load_cached_proxies():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def save_cached_proxies(proxies):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(set(proxies)), f)

def set_system_proxy(proxy):
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    print(f"{Fore.GREEN}[✓] System proxy set to: {proxy}")

def clear_system_proxy():
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    print(f"{Fore.GREEN}[✓] {Fore.YELLOW}System proxy cleared")

def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        return response.text
    except:
        return "Unable to fetch IP"

def print_menu():
    print(f"\n{Fore.MAGENTA}Xopy Proxy Rotator")
    print(f"{Fore.CYAN}Commands:")
    print(f"{Fore.CYAN}  r - Rotate to next proxy")
    print(f"{Fore.CYAN}  c - Clear current proxy")
    print(f"{Fore.CYAN}  i - Show current IP")
    print(f"{Fore.CYAN}  q - Quit the program\n")

def main():
    display_banner()
    proxy_list = load_proxies()
    working_proxies = get_working_proxies(proxy_list)

    if not working_proxies:
        print(f"{Fore.RED}[✗] No working proxies found. Please update your proxy list.")
        return

    random.shuffle(working_proxies)
    proxy_cycle = cycle(working_proxies)

    print_menu()

    while True:
        command = input(f"{Fore.YELLOW}[→] Enter command (r/c/i/q): ").strip().lower()

        if command == 'q':
            clear_system_proxy()
            print(f"{Fore.RED}[▴]{Fore.CYAN} Proxy rotation stopped. System proxy cleared.")
            break
        elif command == 'c':
            clear_system_proxy()
        elif command == 'r':
            proxy = next(proxy_cycle)
            set_system_proxy(proxy)
            current_ip = get_current_ip()
            print(f"{Fore.YELLOW}[⏔] {Fore.MAGENTA}Current IP: {current_ip}")
        elif command == 'i':
            current_ip = get_current_ip()
            print(f"{Fore.YELLOW}[⏔] {Fore.MAGENTA}Current IP: {current_ip}")
        else:
            print(f"{Fore.RED}[✗] Invalid command.")
            print_menu()

if __name__ == "__main__":
    main()
