import subprocess
import sys
import requests
from bs4 import BeautifulSoup

def get_input_fields(url):
    """Fetch and extract input fields from a URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    input_fields = soup.find_all('input')

    field_info = []
    for field in input_fields:
        field_type = field.get('type', 'N/A')
        field_name = field.get('name', 'N/A')
        field_info.append({'type': field_type, 'name': field_name})
    
    return field_info

def save_to_file(fields, file_name):
    """Save the input fields data to a file."""
    with open(file_name, 'w') as file:
        file.write("Input Fields:\n")
        for field in fields:
            file.write(f"Type: {field['type']}, Name: {field['name']}\n")
    print(f"Input fields have been saved to {file_name}")

def run_command(command, output_file=None):
    """Run a command and optionally save output to a file."""
    try:
        if output_file:
            with open(output_file, 'w') as file:
                subprocess.run(command, stdout=file, stderr=subprocess.PIPE, text=True, check=True)
            print(f"Output saved to {output_file}")
        else:
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def main():
    while True:
        print("Enter your choice:")
        print("1 - Reconnaissance")
        print("2 - Web Pentesting")
        print("0 - Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            url = input("Enter URL: ")
            print("1 - Scan - WHOIS data, configurations")
            print("2 - Enumerate parameters, subdomains, and directories")
            ch = int(input("Enter your choice: "))

            if ch == 1:
                print("Starting WHOIS scan...")
                out = input("Output file name (if you want to save): ")
                if out:
                    run_command(["whois", url], f"{out}.txt")
                else:
                    run_command(["whois", url])
            elif ch == 2:
                print("Starting enumeration...")
                out = input("Output file name: ")
                if out:
                    run_command(["subfinder", "-d", url], f"enum{out}.txt")
                    print(f"Subdomain enumeration saved to enum{out}.txt")
                    run_command(["httpx", "-l", f"enum{out}.txt", "-silent"], f"enum_status{out}.txt")
                    print(f"Status of subdomains saved to enum_status{out}.txt")
            else:
                print("Wrong choice. Please try again.")

        elif choice == 2:                  
                print("1 - GET ALL URLs")
                print("2 - GET ALL PARAMETERS")
                ch = int(input("Enter your choice: "))
                if ch == 1:
                        
                        url = input("Enter the URL: ")
                        command = f'echo {url}| hakrawler'
                        run_command([command], "urls.txt")
                elif ch == 2:
                        print("Getting all parameters...")
                        url = input("Enter the URL: ")
                        fields = get_input_fields(url)
                        save_to_file(fields, "paramsout.txt")
                        
                else:
                        print("Wrong choice. Please try again.")

        elif choice == 0:
                sys.exit(0)

if __name__ == "__main__":
    main()
