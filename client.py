import os
import requests
import webbrowser

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n=== File Sharing App ===")
    print("1. Upload File")
    print("2. Access File")
    print("3. Exit")
    print("=====================")

def upload_file(server_url):
    filepath = input("\nEnter the path to the file you want to upload: ")
    # Convert to absolute path if relative
    filepath = os.path.abspath(filepath)
    
    if not os.path.exists(filepath):
        print("File does not exist!")
        return

    try:
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f)}
            headers = {'Accept': 'application/json'}
            response = requests.post(f"{server_url}/", files=files, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("\nFile uploaded successfully!")
                print("Share these details with the recipient:")
                print(f"Access Link: {data['link']}")
                print(f"Access Key: {data['key']}")
            except ValueError as e:
                print(f"\nServer response format error: {str(e)}")
                print("Response content:", response.text)
        else:
            try:
                error_data = response.json()
                print(f"\nError uploading file: {error_data.get('error', 'Unknown error')}")
            except ValueError:
                print(f"\nError uploading file: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Please check if the server is running.")
    except Exception as e:
        print(f"\nError: {str(e)}")

def access_file():
    url = input("\nEnter the access link: ")
    webbrowser.open(url)
    print("\nBrowser opened to access the file.")
    print("Enter the access key in the browser when prompted.")

def main():
    server_url = input("Enter the server URL (default: http://localhost:5000): ").strip()
    if not server_url:
        server_url = "http://localhost:5000"

    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            upload_file(server_url)
        elif choice == '2':
            access_file()
        elif choice == '3':
            print("\nThank you for using the File Sharing App!")
            break
        else:
            print("\nInvalid choice! Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    main()
