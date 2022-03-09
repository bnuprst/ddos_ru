import time

import socket
from concurrent.futures import ThreadPoolExecutor


def ping_udp(host_ip: str, port: int):
    data = "Putin huilo"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(30)
            sock.sendto(bytes(data + "\n", "utf-8"), (host_ip, port))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-16")
            print(f"{host_ip}:{port} Received: {received} ")
    except TimeoutError as te:
        print(f"{host_ip}:{port}  {str(te)} ")
    except BrokenPipeError:
        pass
    except Exception as e:
        print(f"{host_ip}:{port}  {type(e)}: {str(e)} ")

    # print(f"Sent:     {data} to {host_ip}:{port}")


def ping_tcp(host_ip: str, port: int):
    data = "Putin huilo"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(30)
            sock.sendto(bytes(data + "\n", "utf-8"), (host_ip, port))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            print(f"{host_ip}:{port}    Received: {received} ")
    except TimeoutError as te:
        print(f"{host_ip}:{port}  {str(te)} ")
    except BrokenPipeError:
        pass
    except Exception as e:
        print(f"{host_ip}:{port}  {type(e)}: {str(e)} ")

    # print(f"Sent:     {data} to {host_ip}:{port}")


if __name__ == '__main__':
    udp_hosts = []
    udp_port = 53
    with open("udp_hosts.txt") as infile:
        try:
            udp_hosts = [line.strip() for line in infile.readlines() if not line.startswith('#') and not line == '']
            udp_hosts = [(line.split(':')[0], int((line.split(':')[1])) if ':' in line else udp_port) for line in udp_hosts]
            print(print(f"UDP: {udp_hosts}"))
        except IOError:
            print("Failed to read hosts list ")
    tcp_hosts = []
    tcp_port = 22
    with open("tcp_hosts.txt") as infile:
        try:
            tcp_hosts = [line.strip() for line in infile.readlines() if not line.startswith('#') and not line == '']
            tcp_hosts = [(line.split(':')[0], int((line.split(':')[1])) if ':' in line else tcp_port) for line in tcp_hosts]
            print(f"TCP: {tcp_hosts}")
        except IOError:
            print("Failed to read hosts list ")

    start = time.time()
    with ThreadPoolExecutor(max_workers=1_000) as executor:
        while True:
            for host, port in udp_hosts:
                executor.submit(lambda: ping_udp(host, port))
                time.sleep(0.001)
            for host, port in tcp_hosts:
                executor.submit(lambda: ping_tcp(host, port))
                time.sleep(0.001)
