def test(arg):
	"""
	>>> test(1)
	1
	>>> test(2)
	2
	"""
	if arg == 1:
		return 0
	else:
		return 0
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	