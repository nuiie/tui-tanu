import numpy as np
file = open('redOrBlack.data','r')
data = []
label = []
for line in file:
	tmp = np.array(line.strip().split(' '))
	if len(tmp) == 1:
		label.append(tmp[0])
	else:
		data.append(np.array(tmp))
		
