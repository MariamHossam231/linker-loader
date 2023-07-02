#Opening SIC program
inp = open("in.txt","r")

#For output in intermediate file
out = open("intermediate.txt","w")

#reading the first line
start = inp.readline()
firstLine = start.strip().split() #by2asem el line to words mngher the spaces
hexAdd = firstLine[3]; #first location (1000) as a string
LastWord_removed = start[:start.rstrip().rfind(" ")] #Line with last word removed
res= LastWord_removed.split(' ', 1)[1] #split at the space and return a list with 2 elements, 2nd element in the res
out.write(str(res)+ '\n')

for i in inp.readlines():  #take each line in the input file seperatly
	n = i.strip().split()  #list of words

	if n[1] != '.':		
		LastWord_removed = i[:i.rstrip().rfind(" ")] #Line with last word removed
		res= LastWord_removed.split(' ', 1)[1] #split at the space and return a list with 2 elements, 2nd element in the res
		out.write(str(res)+ '\n')

out.write("END"+ '\t'+hexAdd)

inp.close()
out.close()
