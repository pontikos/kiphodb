
lines = file('2009-02-03-full.txt', 'r').readlines()

headers = [x.strip() for x in lines[0].split('\t')]

for l in lines[1:20]:
	print
	for a in zip(headers, [x.strip() for x in l.split('\t')]):
		print a
