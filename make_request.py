import requests
import sys
import json
from colorama import init, Fore
import re
import os

init(autoreset=True)

def parse_url(url):

    if "localhost" in url:
        url = url.replace("localhost", "127.0.0.1")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}"
    
    return url

def make_get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        pretty_json = json.dumps(response.json(), indent=2)

        return pretty_json, response.status_code
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f'Error making request: {e}')
        sys.exit(1)

def make_post_request(url, body, headers=None):
    try:
        if not headers:
            response = requests.post(url, json=body)
        else:
            response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()

        pretty_json = json.dumps(response.json(), indent=2)

        return pretty_json, response.status_code
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f'Error making request: {e}')
        sys.exit(1)


def parse_json_file(filename):

    if not os.path.exists(filename):
        print(Fore.RED + f'Error: file {filename} does not exist')
        sys.exit(1)
    if not os.path.isfile(filename):
        print(Fore.RED + f'Error: {filename} is not a file')
        sys.exit(1)
    if not filename.endswith('.json'):
        print(Fore.RED + 'Error: file must be a .json file')
        sys.exit(1)
    with open(args[2], 'r') as f:
        body = json.load(f)
    
    return body

if __name__ == '__main__':


    patterns = [
        r'^(\S+)$',  # <url>
        r'^(\S+) (.+)$',  # <url> <body>
        r'^(\S+) -r (\S+)$',  # <url> -r <filename_to_read>
        r'^(\S+) -r (\S+) (\S+)$',  # <url> -r <filename_body> <filename_headers>
        r'^(\S+) (.+) -h (.+)$',  # <url> <body> -h <headers>
        r'^(\S+) (.+) -s (\S+)$',  # <url> <body> -s <filename>
        r'^(\S+) -r (\S+) -s (\S+)$',  # <url> -r <filename_to_read> -s <filename_to_save>
    ]

    args = sys.argv[1:]
    prompt = " ".join(args)

    if len(args) == 0:
        print(Fore.RED + 'Usage: python make_request.py <url> [body] [-s filename]')
        sys.exit(1)

    elif len(args) == 1:

        if re.match(patterns[0], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making GET request to: {api_url}')
            api_url = parse_url(api_url)
            data, status = make_get_request(api_url)
        else:
            print(Fore.RED + 'Usage: python make_request.py <url>')
            sys.exit(1)
    
    elif len(args) == 2:

        if re.match(patterns[1], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            api_url = parse_url(api_url)
            body = json.loads(args[1])
            data, status = make_post_request(api_url, body)
        else:
            print(Fore.RED + 'Usage: python make_request.py <url> [body]')
            sys.exit(1)

    elif len(args) == 3:

        if re.match(patterns[2], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            api_url = parse_url(api_url)
            filename = args[2]
            body = parse_json_file(filename)
            data, status = make_post_request(api_url, body)
        else:
            print(Fore.RED + 'Usage: python make_request.py <url> -r <filename_to_read>')
            sys.exit(1)
        
    elif len(args) == 4:

        patterns_4 = patterns[3:6]

        # pattern 3
        if re.match(patterns_4[0], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            
            api_url = parse_url(api_url)
            
            filename_body = args[2]
            filename_headers = args[3]

            body = parse_json_file(filename_body)
            headers = parse_json_file(filename_headers)

            data, status = make_post_request(api_url, body, headers)
        
        # pattern 4
        elif re.match(patterns_4[1], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            api_url = parse_url(api_url)
            body = json.loads(args[1])
            headers = json.loads(args[3])
            data, status = make_post_request(api_url, body, headers)
        
        # pattern 5
        elif re.match(patterns_4[2], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            api_url = parse_url(api_url)
            body = json.loads(args[1])
            data, status = make_post_request(api_url, body)

            print(Fore.GREEN + f'Saving response to {args[3]}')
            with open(args[3], 'w') as f:
                f.write(data)

        else:
            print(Fore.RED + 'Usage: python make_request.py <url> -r <filename_to_read> <filename_to_save>')
            sys.exit(1)
    
    elif len(args) == 5:

        if re.match(patterns[6], prompt):
            api_url = args[0]
            print(Fore.CYAN + f'Making POST request to: {api_url}')
            api_url = parse_url(api_url)
            filename = args[2]
            body = parse_json_file(filename)
            data, status = make_post_request(api_url, body)

            print(Fore.GREEN + f'Saving response to {args[4]}')
            with open(args[4], 'w') as f:
                f.write(data)
        else:
            print(Fore.RED + 'Usage: python make_request.py <url> <body> -s <filename>')
            sys.exit(1)

    else:
        print(Fore.RED + 'Usage: python make_request.py <url> [body] [-s filename]')
        sys.exit(1)

    print(Fore.YELLOW + f"Status code: {status}")
    print("Response data:")
    print(data)