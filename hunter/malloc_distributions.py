import numpy as np

SIZE_SZ = 4
MALLOC_ALIGN_MASK = 7
MINSIZE = 16


def cartesian_product(*arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la)


def req2size(req):
	return np.where(
		(((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)),
		MINSIZE,
		((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK
	)

def safe_alloc_size_dist(size_to_allocate):
	pad_request = np.arange(128)
	pad_sizes = req2size(pad_request)

	main_request = size_to_allocate + 4
	main_size = req2size(main_request)

	return pad_sizes + main_size

def buy_item_size_dist():
	item_size_dist = safe_alloc_size_dist(12)
	name_struct_size_dist = safe_alloc_size_dist(8)
	product = cartesian_product(item_size_dist, name_struct_size_dist)
	return product.sum(axis=1)


def main():
	dist = buy_item_size_dist()
	average = np.average(dist)
	print(f'Average space required by a new item: {average}')
	monster = req2size(0x4010).item()
	print(f'The number of bytes in the monster\'s chunk is: {monster}')
	print(f'To become less than 512, the number of items required is about: {round((monster - 512) / average, 2)}')
	print(f'To become less than 256, the number of items required is about: {round((monster - 256) / average, 2)}')
	print(f'I may recommend being in the middle of the left monster, for safety')

	print()

	dist = safe_alloc_size_dist(12)
	average = np.average(dist)
	print(f'The number of bytes allocated upon "change player": {average}')
	print(f'To become less than 512, the number of changes required is about: {round((monster - 512) / average, 2)}')
	print(f'To become less than 256, the number of changes required is about: {round((monster - 256) / average, 2)}')
	print(f'I may recommend being in the middle of the left monster, for safety')

if __name__ == '__main__':
	main()

