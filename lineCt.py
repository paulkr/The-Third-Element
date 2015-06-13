from glob import glob
files = glob("*.py") + glob("Game/*.py")
files.remove("lineCt.py")

lines = 0
comments = 0
chars = 0

for f in files: 
	thing = open(f).read()
	lines += thing.count("\n")
	comments += thing.count("#")

print("%d Lines\n%d Files\nWithout comments %d"%(lines, len(files), lines-comments))
