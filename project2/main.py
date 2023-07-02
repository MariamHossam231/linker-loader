import pandas as pd
import numpy as np
from numpy.random import randn
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pandastable import Table
import re

def to_hex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))


data=[]
start_addH=0
start_addT=0
lengthH=0
f_data=[] 
n= '10'
flag=0
count =2
j=0
Lenthss=[]
address=[]
H_address = []
H_length = []
H_name=[]
T_recs=[]
T_start_add=[]
T_length_rec=[]
T_size = 0
D_name=[]
D_add = []
D=[]
g=0
k =1
defi=[]
d1=[]
d2=[]
R_rec=[]
q=0
added_len='0'
zer0='0'
t_address=[]
stg=[]
stg2=[]
adddd=[]
tot_add=[]


st='0'
hh= 0
jj=0
ppp=[]
T_new_start_add=[]
kk=[]
labels=[]
label_address=[]
firstChar = ""
label = ''
found_add=0
#----------------------- GIVING THE USER A CHOICE ! --------------------
while(flag == 0):
    Address=''
    win= Tk()
    win.geometry("750x250")
    Address_entry=None
    labelFrame = LabelFrame(win,text = "Choose " , padx=50,pady=50) #label in a frame
    labelFrame.pack()
    Label(labelFrame,text="SIC OR SICXE").pack() #label 3ady
    Address_entry = Entry(labelFrame) #input text field
    Address_entry.pack()
    
    Button(labelFrame,text="Start" ,command=win.quit).pack()
    win.mainloop()
    choice = Address_entry.get()
    

    if(choice =="SIC" or choice =="sic"):
        FILEIN = open("InputSic.txt","r")
        LOCATION = open("out.txt","w")
        flag=1
#--------------------- READING THE FILE --------------------------

        line1 = FILEIN.readline()
        name=line1[1:7]
        start_addH = line1[7:13]
        lengthH = line1[13:]

        for line in FILEIN:
            if(line[0] == 'T'):
                start_addT = line[1:7] #SAVING THE STARTING ADDRESS FOR EACH T REACOD
                address.append(start_addT)  #SAVING EACH STARTING ADDRESS IN A LIST CALLED ADDRESS
                length = line[7:9]     #SAVING THE LENGTH OF EACH T RECORD
                Lenthss.append(length)      #SAVING EACH LENGTH FOR EACH T REACORD IN A LIST CALLED LENGTHSSS
                opcode = line[9:]      #SAVIING ALL THE OOPCODES IN ALL T RECORD IN A LIST CALLED OPCODE
                x = 2
                list1 =[opcode[i:i+2] for i in range (0,len(opcode),x)]
                edited = list1[:-1]
                data.append(edited)

        FILEIN.close()

        #-------------------------------- DOING STUFF -----------------------------------

        size = hex(int(start_addH, 16) + int(lengthH, 16))                  #CALCULTAING THE TOTAL SIZE OF THE PROGRAM 
        last_row = str(hex(int(start_addH, 16) + int(lengthH, 16)- int(n, 16)))[2:]  #CALCULLATING THE LAST ROW OF THE TABLE
        index=str(hex(int(start_addH,16)))[2:]
        f_data.append(index)                                  
        while index<last_row:
            index= str(hex(int(index, 16) + int(n, 16)))[2:]                        #CALCULATING EACH ADDRESS TO BE ADDED BY 10
            f_data.append(index)

        m =' '.join(map(str,f_data))     #CONVERTING THE LIST INTO STRINGS SO WE CAN ADD THEM IN THE INDEX SINCE THE INDEX ACCEPTS ONLY STRING 
        patn = re.sub(r"[\([{''})\]]", "", m)                              #REMOVES THE SQAURE BRACETS, SINGLE QUOTATIONS , THE X CHAR 


        #------------------------------- DATAFRAME ------------------------------------------

        # pd.set_option('display.max_rows', None)
        df = pd.DataFrame(index=patn.split(),columns='0 1 2 3 4 5 6 7 8 9 a b c d e f'.split())

        #------------------------------ TABLE STUFF --------------------------------------------

        P='1'
        while (j <len(data)):
            T_rec = data[j]         #SINCE EN EACH OPCODE FOR THE EACH T RECORD IS AN ARRAY INSIDE AN ARRAY FA THIS MEAN WE CAN ACCESS THE LIST THAT HAS AN ENTIRE OPCODE FOR EACH T REOCRD ; HERE WE ARE ACCESSING THE FIRST OPCODES FOR THE FIRST T RECORD
            curr_add=address[j] #ADDRESS HAS ALL THE STARTING ADDRESSES FOR EACH T RECORD HERE WE ARE ACCESSING EACH ONE OF THEM AND REMOVING 0x
            curr_len=Lenthss[j]     #LENGTHSS IS A LIST THAT HAS ALL THE LENGTHS OF EACH T RECORD SO HERE WE ARE ACCESSING EACH LENGTH OF EACH T RECORD
            last_add = str(hex(int(curr_add, 16) + int(curr_len, 16)))[2:]  #HERE WE HAVE THE LAST ADDRESS FOR EACH T RECORD OR THE S
            add = str(hex(int(curr_add,16)))[2:]    #HERE WE ARE CONVERTING THE CURR ADD TO A STRING 
            c = 0       #COUNTER
            while(curr_add<last_add):   
                col2 = add[:-1]+'0'  
                row2 = add[-1]
                add = str(hex(int(add,16)+int(P,16)))[2:]   #THIS ADDS THE ADDRESS SO WE CAN BE ABLE TO MOVE THRU THE MEMORY (1075-->1076-->1077-->1078-->1079-->107A...AND SO ON)
                curr_add= str(hex(int(curr_add,16)+int(P,16)))[2:] #THIS TO ADD THE CURR ADD SO WE THE WHILE LOOP WORKS 
                df[row2][col2]=T_rec[c] #HERE WE ARE ADDING THE VALUES OF THE T RECORD INTO POSITIONS ROW2 AND COL2
                c+=1                       #INCREMENT THE COUNTER 
            j+=1                           #INCREMENT THE COUNTER
        print(df)
#---------------------------------------- UPLODING THE DATAFRAME INTO TKINTER AND IMPLEMENTING THE GUI --------------------------------------
        
        #THIS IS STANDARD CODING 
        root = tk.Tk()
        root.title('Absolute Loader')

        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=df)
        pt.show()
        pt.showindex=True 
        root.mainloop()

#--------------------------------------------------------------------------------------------------------------------------------------

    elif(choice =="SICXE" or choice=="sicxe"):
        FILEIN = open("HTE_SICXE.txt","r")
        LOCATION = open("out.txt","w")
        flag=1
        # Address = input("Enter the starting Address : ")
        Address=''

        win= Tk()

        win.geometry("750x250")
        Address_entry=None
        labelFrame = LabelFrame(win,text = "GENERATE " , padx=50,pady=50)
        labelFrame.pack()
        Label(labelFrame,text="ENTER STARTING ADDRESS").pack()
        Address_entry = Entry(labelFrame)
        Address_entry.pack()
        
        Button(labelFrame,text="Confirm Address" ,command=win.quit).pack()
        win.mainloop()
        Address = Address_entry.get()

        for line in FILEIN:
            if(line[0] == 'H'):
                name = line[1:6]
                hAddress = line[7:13] + Address
                lengthHre = line[13:19]
                H_name.append(line[1:7].replace('X',''))
                H_address.append(line[7:13])
                H_length.append(line[13:19])

            if(line[0] == 'D'):
                defi=line[1:]
                itr=12
                D1 =[defi[i:i+6] for i in range (0,len(defi),itr)][:-1]
                D2 =[defi[i+6:i+12] for i in range (0,len(defi),itr)][:-1]
                D_name.append(D1)   #values for all the extdef names
                D_add.append(D2)    #values for all the extdef location
                D.append(D1)

            if(line[0] == 'R'):
                ref=line[1:]
                itr=6
                R =[ref[i:i+6] for i in range (0,len(ref),itr)][:-1]
                R_rec.append(R)         #Values of all the ref

            if(line[0] == 'T'):
                start_addT = line[1:7] #SAVING THE STARTING ADDRESS FOR EACH T REACOD
                address.append(start_addT)  #SAVING EACH STARTING ADDRESS IN A LIST CALLED ADDRESS
                length = line[7:9]     #SAVING THE LENGTH OF EACH T RECORD
                Lenthss.append(length)      #SAVING EACH LENGTH FOR EACH T REACORD IN A LIST CALLED LENGTHSSS
                opcode = line[9:]      #SAVIING ALL THE OOPCODES IN ALL T RECORD IN A LIST CALLED OPCODE
                x = 2
                list1 =[opcode[i:i+2] for i in range (0,len(opcode),x)]
                edited = list1[:-1]
                data.append(edited)
            
        FILEIN.close()

#-------------------------------------------------- GETTING THE ESTABLE ------------------------------------------------------------------------------------

        m =' '.join(map(str,H_name))
        patn = re.sub(r"[\([{''})\]]", "", m)
        patnLen=patn.split()
        df = pd.DataFrame(index=patn.split(),columns='Address Length Symbol_Name'.split())
        while(q<len(patnLen)): # patnlen = 3
            gg=str(hex(int(added_len,16)+ int(Address,16)))[2:]
            adddd.append(gg)
            df['Address'][q]=str(hex(int(added_len,16)+ int(Address,16)))[2:]
            added_len=str(hex(int(added_len,16)+int(H_length[q][2:],16)))[2:]
            df['Length'][q] = H_length[q]
            y=0
            while(y<len(D_name[q])):
                d_full_add=str(hex(int(D_add[q][y],16)+ int(adddd[q],16)))[2:]
                stringaya = D_name[q][y].replace('X','')+':'+d_full_add
                stg.append(stringaya)
                # print("llllllllllllllllllllll")
                # print(stg)
                x=2
                list2 =[stg[i:i+2] for i in range (0,len(stg),x)]
                df['Symbol_Name'][q]=list2[q]  
                y+=1          
            q+=1
        
        root = tk.Tk()
        root.title('ESTABLE ')
        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=df)
        pt.show()
        pt.showindex=True 
        root.mainloop()
        
        EXT_SYM = open("EXT_SYM_Table","w")
        df.to_csv(r'D:\AAST term7\systems of programming\project2\EXT_SYM_Table' ,sep=' ', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------- CALULARING THE INDEX OF THE MEMORY--------------------------------------------------------
        while(j< len(H_name)):
            cal_add1=str(hex(int(zer0,16)+ int(Address,16)))[2:]
            t_address.append(cal_add1)                                  #START ADDRESS OF EACH PROGRAM 
            zer0=str(hex(int(zer0,16)+int(H_length[j][2:],16)))[2:] 
            j+=1
        # print(t_address)
        while(jj < len(t_address)):
            Last_add = hex(int(t_address[jj], 16) + int(H_length[jj], 16))[2:]    #LAST ADDRESS OF EACH PROGRAM
            ppp.append(Last_add)
            jj+=1               
        
        
        index=str(hex(int(t_address[0],16)))[2:]
        f_data.append(index)                                  
        while index<Last_add:
            index= str(hex(int(index, 16) + int('10', 16)))[2:]                        #CALCULATING EACH ADDRESS TO BE ADDED BY 10
            f_data.append(index)                                                        #f_data has the index of the memory

        m2 =' '.join(map(str,f_data))     #CONVERTING THE LIST INTO STRINGS SO WE CAN ADD THEM IN THE INDEX SINCE THE INDEX ACCEPTS ONLY STRING 
        patn2 = re.sub(r"[\([{''})\]]", "", m2)                              #REMOVES THE SQAURE BRACETS, SINGLE QUOTATIONS , THE X CHAR 
        # print(t_address)       \

#-------------------------------------------------------------------------------------------------------------------------------------------------
        
        df2 = pd.DataFrame(index=patn2.split(),columns='0 1 2 3 4 5 6 7 8 9 a b c d e f'.split())

        FILEIN = open("HTE_SICXE.txt","r")

        for line1 in FILEIN:
            if(line1[0]=='H'):
                name = line1[1:7].replace('X','')
                start = df.loc[name]["Address"]
            
            if(line1[0]=='T'):
                tStart = hex(int(line1[1:7],16)+int(start,16))
                T_new_start_add.append(tStart)
        FILEIN.close()

#----------------------------------------------- UPLAODING THE MEMORY ----------------------------------------------------------------------

        P='1'
        while (hh <len(data)):
            T_rec = data[hh]         #SINCE EN EACH OPCODE FOR THE EACH T RECORD IS AN ARRAY INSIDE AN ARRAY FA THIS MEAN WE CAN ACCESS THE LIST THAT HAS AN ENTIRE OPCODE FOR EACH T REOCRD ; HERE WE ARE ACCESSING THE FIRST OPCODES FOR THE FIRST T RECORD
            curr_add=T_new_start_add[hh] #ADDRESS HAS ALL THE STARTING ADDRESSES FOR EACH T RECORD HERE WE ARE ACCESSING EACH ONE OF THEM AND REMOVING 0x
            curr_len=Lenthss[hh]     #LENGTHSS IS A LIST THAT HAS ALL THE LENGTHS OF EACH T RECORD SO HERE WE ARE ACCESSING EACH LENGTH OF EACH T RECORD
            last_add = str(hex(int(curr_add, 16) + int(curr_len, 16)))[2:]  #HERE WE HAVE THE LAST ADDRESS FOR EACH T RECORD OR THE S
            add = str(hex(int(curr_add,16)))[2:]    #HERE WE ARE CONVERTING THE CURR ADD TO A STRING
            c = 0       #COUNTER
            while(curr_add<last_add):
                col2 = add[:-1]+'0'  
                row2 = add[-1]            
                
                add = str(hex(int(add,16)+int(P,16)))[2:]   #THIS ADDS THE ADDRESS SO WE CAN BE ABLE TO MOVE THRU THE MEMORY (1075-->1076-->1077-->1078-->1079-->107A...AND SO ON)          
                curr_add= str(hex(int(curr_add,16)+int(P,16)))[2:] #THIS TO ADD THE CURR ADD SO WE THE WHILE LOOP WORKS 
                df2[row2][col2]=T_rec[c] #HERE WE ARE ADDING THE VALUES OF THE T RECORD INTO POSITIONS ROW2 AND COL2
                c+=1                       #INCREMENT THE COUNTER 
            hh+=1                          #INCREMENT THE COUNTER
        # print(df2)

#----------------------------------------------UPLODING THE GUI INTO TKINTER --------------------------------------
        root = tk.Tk()
        root.title('Linker Loader')

        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=df2)
        pt.show()
        pt.showindex=True 
        root.mainloop()

#-----------------------------------------------------------------------------------------------------------------------
        
        FILEIN = open("HTE_SICXE.txt","r")

        for line2 in FILEIN:
            if(line2[0]=='H'):
                name2 = line2[1:7].replace('X','')
                start2 = df.loc[name2]["Address"]
                for ayhaga in df.loc[name2]["Symbol_Name"]:
                    definition = ayhaga.split(":")
                    label_address.append(definition[1])
                    labels.append(definition[0])
                    

            if(line2[0]=='M'):
                label = line2[10:].strip()              
                    # print(value)

        FILEIN = open("HTE_SICXE.txt","r")

        for line2 in FILEIN:
            firstChar =''
            if(line2[0]=='H'):
                name2 = line2[1:7].replace('X','')
                start2 = df.loc[name2]["Address"]
            if(line2[0]=='M'):
                m_add = line2[1:7]
                name_m = line2[10:15]                   
                mod_add = str(hex(int(m_add,16)+int(start2,16)))[2:]
                row = mod_add[:3]+'0'
                rowadded = str(hex(int(row,16)+int('10',16)))[2:]
                col=mod_add[3:]
                coladded=str(hex(int(col,16)+int('1',16)))[2:]
                coladdedby2=str(hex(int(col,16)+int('2',16)))[2:]
                lengthM = line2[7:9]
                operator = line2[9:10]
                

                if(int(col,16)<14):
                    value=str(df2[col][row])+str(df2[coladded][row])+str(df2[coladdedby2][row])
                    # print(value)
            
                elif(int(col,16)==14):
                    value=str(df2[col][row])+str(df2[coladded][row])+str(df2['0'][rowadded])
                    # print(value)

                elif(int(col,16)==15):
                    value=str(df2[col][row])+str(df2['0'][rowadded])+str(df2['1'][rowadded])  

                if(line2[7:9]=='05'):
                    firstChar = value[0]
                    value = value[1:]

                label = line2[10:].strip()
                curr_prog = df.loc[name2].name
                if(label==curr_prog):
                    found_add = df.loc[name2]["Address"]
                    # print(found_add)
                else:
                    for labell , addr in zip(labels,label_address):
                        #print(f'{labell} == {label}')
                        if(labell == label):
                            found_add = addr
                            # print("FOUND: "+label)
                            # print("FOUND2: "+addr)
                            break
                if(operator == '+'):
                    # print(value +'+'+ found_add +'= ')
                    value = firstChar+str(hex(int(value,16)+int(found_add,16))).replace("0x", "").zfill(6).upper()[-int(lengthM):]
                    # print(value)

                if(operator == '-'):
                    # print(value)   
                    value = firstChar+str(hex(int(value,16)-int(found_add,16))).replace("0x", "").zfill(6).upper()[-int(lengthM):]
                    # print("BY SUB "+value)

                
                if(int(col,16)<14):
                    print(col +'  '+ coladded + ' ' +coladdedby2)
                    df2.at[row,col]=value[0:2]
                    df2.at[row,coladded]=value[2:4]
                    df2.at[row,coladdedby2]=value[4:6]
            
                elif(int(col,16)==14):
                    print(col +'  '+ coladded + ' ' +coladdedby2)
                    df2.at[row,col]=value[0:2]
                    df2.at[row,coladded]=value[2:4]
                    df2.at[rowadded,'0']=value[4:6]

                elif(int(col,16)==15):
                    print(col +'  '+ coladded + ' ' +coladdedby2)
                    df2.at[row,col]=value[0:2]
                    df2.at[rowadded,'0']=value[2:4]
                    df2.at[rowadded,'1']=value[4:6]
        
        
        root = tk.Tk()
        root.title('Linker Loader After Modifications')
        
        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=df2)
        pt.show()
        pt.showindex=True 
        root.mainloop()

    else:
        print("Invalid Input")
        flag=0
