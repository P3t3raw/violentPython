import socket

HOST = "127.0.0.1" #localhost
PORT = 8084

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    server.listen(1)
    print(f"Listening on {HOST}:{PORT}...")
    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")
        conn.sendall(b"Ability Server 2.34")
