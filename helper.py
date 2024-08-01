import re
from dotenv import set_key

def extract_csrf_and_cookie(curl_command):
    csrf_pattern = re.compile(r"X-CSRF-Token: ([^\s']+)")
    cookie_pattern = re.compile(r"Cookie: ([^']+)")
    csrf_match = csrf_pattern.search(curl_command)
    cookie_match = cookie_pattern.search(curl_command)
    csrf_token = csrf_match.group(1) if csrf_match else None
    cookie = cookie_match.group(1) if cookie_match else None
    return csrf_token, cookie

def save_to_env(csrf_token, cookie):
    env_file = '.env'
    set_key(env_file, "CSRF_TOKEN", csrf_token)
    set_key(env_file, "COOKIE", cookie)

if __name__ == "__main__":
    curl_command = input("Please enter the curl command: ")
    csrf_token, cookie = extract_csrf_and_cookie(curl_command)
    if csrf_token and cookie:
        save_to_env(csrf_token, cookie)
        print("Values saved to .env file.")
    else:
        print("Failed to extract CSRF token or cookie.")
