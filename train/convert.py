f = open('train.data', 'r')
for line in f:
	a = line.strip().split(',')
	print ' '.join(a[1:]).strip()
	if a[0] == 'blkelephant':
		print '1'
	elif a[0] == 'elephant':
		print '2'
	elif a[0] == 'horse':
		print '3'
	elif a[0] == 'boat':
		print '4'
	elif a[0] == 'red':
		print '5'
	elif a[0] == 'black':
		print '6'
	elif a[0] == 'fly':
		print '7'
	elif a[0] == 'house':
		print '8'