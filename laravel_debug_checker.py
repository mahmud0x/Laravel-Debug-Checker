import requests
from requests.exceptions import Timeout, RequestException, SSLError
from colorama import init, Fore

# Initialize colorama
init()

def check_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()

    found_urls = []

    for url in urls:
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        url = url + "/_ignition/execute-solution"

        try:
            response_http = requests.get(url, timeout=15)
            response_https = requests.get(url.replace("http://", "https://"), timeout=15)

            if "GET method is not supported" in response_http.text:
                print(f"{Fore.GREEN}Debug Mode On GG{Fore.RESET}",url)
                found_urls.append(url)
            elif "GET method is not supported" in response_https.text:
                print(f"{Fore.GREEN}Debug Mode On GG{Fore.RESET}",url)
                found_urls.append(url.replace("http://", "https://"))
            else:
                print(f"{Fore.RED}DEBUG Mode Disabled{Fore.RESET}",url)

        except Timeout:
            print(f"{Fore.RED}DEBUG Mode Disabled{Fore.RESET}",url)
        except SSLError as ssl_error:
            if "certificate verify failed: Hostname mismatch" in str(ssl_error):
                print(f"{Fore.RED}DEBUG Mode Disabled{Fore.RESET}",url)
            else:
                print(f"{Fore.RED}DEBUG Mode Disabled{Fore.RESET}",url)
                print("Error:", str(ssl_error))
        except RequestException as e:
            print(f"{Fore.RED}DEBUG Mode Disabled{Fore.RESET}",url)
            print("Error:", str(e))

    with open("output_laravel_debug.txt", 'w') as output_file:
        output_file.write("\n".join(found_urls))

    print(f"\n{Fore.GREEN}Found URLs have been saved to 'output_laravel_debug.txt'.{Fore.RESET}")

# Example usage
file_path = input("Enter the file path: ")
check_urls_from_file(file_path)
