import socket
import time
import threading

def handle_attacker(client_socket, address, delay):
    """
    Handles an incoming connection by sending data extremely slowly.
    """
    print(f"[!] Trapped attacker from: {address}")
    try:
        # Send a fake SSH banner one character at a time
        banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n"
        for char in banner:
            client_socket.send(char.encode())
            # This is the "Tar": a 5-second delay between every character
            time.sleep(delay)
            
        client_socket.close()
    except Exception as e:
        print(f"Attacker {address} disconnected: {e}")

def start_tarpit(host='127.0.0.1', port=2222, delay=2):
    """
    Sets up the listening socket for the tarpit.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(100)
    print(f"[*] Tarpit Active on {host}:{port} (Delay: {delay}s)")

    while True:
        client, addr = server.accept()
        # Spin up a thread for each "guest" to keep them trapped
        t = threading.Thread(target=handle_attacker, args=(client, addr, delay))
        t.start()

if __name__ == "__main__":
    # Use a high port for testing to avoid needing sudo
    start_tarpit(port=2222, delay=1)