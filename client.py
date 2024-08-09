import socket

def start_client(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Type 'dice' to play Pig Game ('quit' to exit)")
        while True:
            message = input(": ")
            if message.lower() == 'quit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"{data.decode()}")  
            if (data.decode().endswith("Goodbye!")):
                break

if __name__ == "__main__":
    start_client()
