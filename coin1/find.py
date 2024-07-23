import socket
from typing import Tuple
from time import sleep


HOST = 'pwnable.kr'
PORT = 9007
MAX_PACKET_LEN = 2048
START_SLEEP_TIME = 3  # In seconds
NUM_ROUNDS = 100
VERBOSE = True

g_socket = None


def recv() -> str:
    data = g_socket.recv(MAX_PACKET_LEN).decode()
    if VERBOSE:
        print(data, end='')
    return data


def send(data: str) -> None:
    data = data + '\n'
    g_socket.sendall(data.encode())
    if VERBOSE:
        print(data, end='')


def init_game() -> None:
    recv()
    sleep(START_SLEEP_TIME)


def init_round() -> Tuple[int, int]:
        init_line = recv()
        N_string, C_string = init_line.split()
        return int(N_string[2:]), int(C_string[2:])


def range_contains_fake(left: int, right: int):
    """ Both ends are inclusive """
    range_string = ' '.join((str(pos) for pos in range(left, right+1)))
    send(range_string)

    expected_weight = 10 * (right - left + 1)
    actual_weight = int(recv())
    return (expected_weight != actual_weight)


def win_round():
    N, C = init_round()

    left = 0  # Inclusive
    right = N-1  # Inclusive
    for _ in range(C):
        mid = (right + left) // 2  # Inclusive
        if range_contains_fake(left, mid):
            right = mid
        else:
            left = mid + 1
    send(str(left))
    recv()
    

def main():
    global g_socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as g_socket:
        g_socket.connect((HOST, PORT))
        init_game()
        for i in range(NUM_ROUNDS):
            win_round()
        recv()


if __name__ == '__main__':
    main()