import math
#Start of pass one functions
def calByt(mem , operand):
    f = 0
    nBytes= 0
    if(mem == "RESW" or mem == "RESB" or mem == "WORD" or mem == "BYTE" ):
        f=1
        if(mem == "RESW"):
            operand = int(operand)
            nBytes = operand*3
        if(mem == "RESB"):
            operand = int(operand)
            nBytes = operand
        if(mem == "WORD"):
            operand = int(operand)
            nBytes = 3
        if(mem == "BYTE"):
            if(operand[0]=='X'):
                if ((len(operand)-3)%2 == 0):
                    nBytes = (len(operand)-3)/2
                else : nBytes = ((len(operand)-3)/2)+1 
            if(operand[0] == 'C'):
                nBytes = len(operand)-3

    else:
        opcode = open("OPCODE.txt","r")
        for line in opcode:
            op = line.strip().split()
            if(mem == op[0]):
                f=1 #found
                nBytes = op[1]
    if(f == 0):
        nBytes = -1
    return nBytes


def symExist(symbol):
    found = False
    systab = open("SYMTAB.txt","r")
    for i in systab:
        line = i.strip().split() 
        if(line[0]==symbol):
            found=True
            break 
    systab.close()
    return found
# End of Pass one Function

# Start of Pass Two Functions
def calOPCODE(ins):
    opcode = open("OPCODE.txt","r")
    f = 0
    for i in opcode:
        line = i.strip().split()
        if(line[0]==ins):
            op = line[2]
            f=1
            break
    if(f==1):
        return op
    return -1

def retAddress (symbol):
    symtab = open("SYMTAB.txt","r")
    f = 0
    SymbolStr = str(symbol)
    if(SymbolStr.find(",x")!= -1):
        size = len(SymbolStr)
        WithoutX = SymbolStr[:size - 2]
        for i in symtab:
            line = i.strip().split()
            if(str(line[0]) == WithoutX):
                f=1
                add = str(hex(int(line[1],16) + int("8000",16)))[2:] 
                break
        if(f==1):
            return add
        return -1
    else:
        for i in symtab:
            line = i.strip().split()
            if(line[0] == symbol):
                f=1
                add = line[1]
                break
        if(f==1):
            return add
        return -1
#End of Pass Two Functions


##############################################################################################################

#openning intermediate
inputFile = open("intermediate.txt","r")
#create out and symbol table
out = open("Output.txt","w")
symtab = open("SYMTAB.txt","w")
#reading the first line
start = inputFile.readline()
##print(start)

firstLine = start.strip().split() #by2asem el line to words mngher the spaces
hexAdd = firstLine[2]; #first location (1000) as a string
decAdd = int(hexAdd,16) #1000 in decimal = 4096
tempHexa = hexAdd #saving 1000 in tempHex

for i in inputFile:  
    line = i.strip().split() #seperting the line to words without spaces
    print(str(hex(decAdd)) +'\t' +'\t'.join(line) ) 

    ##Getting the location Counter
    if(line[0] == "END"):
        break
    nBytes = 0
    if(len(line)==3):
        nBytes = calByt(line[1],line[2])
        ## TO GET SYMBOL TABLE
        if(symExist(line[0])==False):
                symbol = line[0] + "\t" + tempHexa
                symtab.write(symbol)
                symtab.write("\n")
                symtab.flush()
    elif(len(line)==2 ):
        nBytes = calByt(line[0],line[1])
    elif(len(line)==1):
        nBytes = calByt(line[0],0)

    print(line[0] , nBytes)

    if(nBytes == -1):
        print("error "+ line[0])
        input()
        exit(0)

    wl = tempHexa+"\t"+i
    out.write(wl)
    out.flush()
    decAdd = decAdd + int(nBytes)
    tempHexa=str(format(decAdd,'04x'))

wl = tempHexa+"\t"+i
out.write(wl)
out.flush()
decAdd = decAdd + int(nBytes)
tempHexa=str(format(decAdd,'04x'))

inputFile.close()
out.close()
symtab.close()
##END OF PASS ONE


##Start pass two
out = open("Output.txt","r") #read mno
opcode = open("ObjCode.txt","w") #write fih
out2 = open("Output.txt","r") #read mno

line2 = out2.readline()
start_add = line2.strip().split()[0]

for i in out:
    line = i.strip().split()
    if(len(line)==4):
            operand = line[3]
            ins = line[2]
    elif(len(line)==3):
        operand = line[2]
        ins = line[1]
    elif(len(line)==2):
        ins = line[1]
    
    if(operand == start_add):
        break
    
    if(ins != "RESW" and ins != "RESB"):
        
        if(ins=="BYTE"):
            type = operand.split('\'') #type = ['C', 'EOF', '']
            if(type[0]=='X'):
                i=i.rstrip()
                writeL = i + "\t" + type[1] + "\n"
                opcode.write(writeL)
            if(type[0]=='C'):
                chars = list(type[1]) #chars = ['E', 'O', 'F']
                objL = "" #fadet el object code
                objL=( ''.join(str(hex(int(str(ord(c))))[2:]) for c in chars)) 
                i=i.rstrip()
                writeL = i + "\t" + objL + "\n"
                opcode.write(writeL)

        elif(ins == "RSUB"):
            objL = "4C0000"
            i=i.rstrip()
            writeL = i + "\t\t\t" +objL + "\n"
            opcode.write(writeL)

        elif(calByt(ins,0) == '1' ): #handeling format 1 #
            objL =calOPCODE(ins)
            i=i.rstrip()
            writeL = i + "\t\t\t" +objL + "\n"
            opcode.write(writeL)

        elif(ins == "WORD"):
            operand = int(operand)
            objL = str(format(operand,"06x"))
            i=i.rstrip()
            writeL = i + "\t" + objL + "\n"
            opcode.write(writeL)
        
        else: #not a word / byte / rsub  / not a format 1
            op = calOPCODE(ins) #calculate opcode
            calByt(line[0],0)
            opS = operand.split(",") 
            length = len(opS) 
            TA = retAddress(operand)
            
            if(operand[0]=='#'):
                op=hex(int(op,16)+1)[2:]
                x = hex(int(operand[1:],10))[2:]
                while(len(op)<2):
                    op='0'+op
                while(len(x)<4):
                    x='0'+x
                op = op + x
                objL = op
                TA = 1
            else:
                if(op == -1): #not found opcode
                    print("Error charachter")
                    input()
                    exit(0)
                
                if(TA == -1): #didn't find the label in symbol table
                    print("Error address in " + operand)
                    input()
                    exit(0)
                if(length == 2 and opS[1] == "X"): #to print the obcode in the right format
                    strg = TA
                    cut1 = strg[:1]
                    cut2 = strg[1:]
                    cut1 = int(cut1)
                    cut1 = cut1 +8
                    cut1 = str(format(cut1,'01X'))
                    TA = cut1 +cut2
                objL = op+TA

            i=i.rstrip()
            writeL = i + "\t" + objL + "\n"
            opcode.write(writeL)
    else:
        opcode.write(i)

i=i.rstrip()
writeL = i
opcode.write(writeL)

inputFile.close()
out.close()
symtab.close()
out.close()
opcode.close()
out2.close()

objectCode = open("objCode.txt","r")

#printing the object code
# for aline in objectCode:
# 	line = aline[:-1]
# 	print(line)

#End of Pass Two


#Start HTE#
ObjectCode = open("ObjCode.txt", "r")
ObjectCode.readline()
LOCATION = open("Output.txt", "r")
LOCATION2 = open("Output.txt", "r")
Start = LOCATION.readline()
LA = open("intermediate.txt","r")
Line= LA.readline()

LOC = int(str(Line.split()[len(Line.split()) - 1]), 16) #awel loc in decimal -> 4096
Starting_Address = hex(LOC)[2:] #converted to hexa -> 1000
Program_Name = Line.split()[1] # -> start
Start = LOCATION.readline().split()[0] # -> 1003


with open("HTE.txt","w") as f: #opening the HTE file to wite in
        records = [] #empty array
        while(len(Program_Name)<6):
            Program_Name = Program_Name+"X"
        while(len(Starting_Address)<6):
            Starting_Address = "0" + Starting_Address
        #calculating the length of the program
        c = 3 # you already holded the first instr + End + Start
        for i in LOCATION:
            line = i.strip().split()
            c=c+1 #number of instructions
            if(line[1]=="END"):
                Ending_Address = line[0]
        Program_Size = int(Ending_Address,16) - int(Starting_Address,16)
        Program_Size = hex(Program_Size)[2:]
        while(len(Program_Size)<6):
            Program_Size = "0" + Program_Size
        records.append("H"+Program_Name+Starting_Address+Program_Size)
        #End of H

        instr = [] #array of instructions
        code = [] #array of object codes
        ArrAdd=[] #array of address
        adreses=""
        with open('objCode.txt') as temp: #read from objcode goal:1)instruction array 2)object code array 3)address array
            for line in temp:
                curr_line = line.strip().split()#-> an array of the elements of the curr_line
                ArrAdd.append(curr_line[0]) #array of all the addresses

                #getting the instruction array
                if(len(curr_line)==5):
                    ins = curr_line[2]
                elif(len(curr_line)==4):
                    if(curr_line[2] == "RESW" or curr_line[2] == "RESB"):
                        ins = curr_line[2]
                    else:
                        ins = curr_line[1]
                elif(len(curr_line)==3):
                    ins = curr_line[1]

                # making the object code array
                if(ins =="RESW" or ins =="RESB" or ins=="END" ): 
                    code.append('')
                else:
                    code.append(curr_line[-1])

                instr.append(ins)
                adreses= adreses + curr_line[0] + " "

            i = 0
            adreses=adreses.split(" ")
            T_Starting_Address = adreses[0]
            while(i<len(instr)): #tool ma lesa fih instructions
                T_Starting_Address = ArrAdd[i]
                T_Record = ""
                T_Record_Size = 0
                while(T_Record_Size<30):
                    if(code[i]==''):
                        i+=1 
                        break #breaking the record
                    if(T_Record_Size + math.floor(len(code[i])/2) <=30): #gher kda di lesa instr w haykml fa yhsb el size el gded
                        T_Record_Size+=math.floor(len(code[i])/2)
                        T_Record+=code[i]
                        i+=1
                    else:
                        break

                if(T_Record_Size==0):
                    continue
                T_Record_Size = hex(T_Record_Size)[2:]
                while(len(T_Record_Size)<2):
                    T_Record_Size = "0"+T_Record_Size

                while(len(T_Starting_Address)<6):
                    T_Starting_Address = "0"+T_Starting_Address
                records.append("T"+str(T_Starting_Address) +T_Record_Size +T_Record+"\n")
        # E record
        records.append("E"+Starting_Address)
        for i in range(len(records)):
            f.write(records[i]+"\n")

#End Of HTE