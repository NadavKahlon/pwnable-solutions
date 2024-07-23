def print_char(char):
	prefix = '\x1b['
	if char == '1':
		prefix += '107'
	elif char == 'S':
		prefix += '43'
	elif char == 'G':
		prefix += '41'
	elif char == 'E':
		prefix += '42'
	else:
		prefix += '0'
	prefix += 'm'

	print(prefix + char, end='')

def main():
	f = open('maze_map.txt', 'r')
	data = f.read()
	f.close()

	for char in data:
		print_char(char)
	print_char('\x1b[0m')

if __name__ == '__main__':
	main()
