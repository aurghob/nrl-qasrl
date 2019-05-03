# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 16:52:50 2018

@author: slash
"""

import pandas as pd
from collections import defaultdict


xl = pd.ExcelFile("/mnt/c/Masters Studies/interests/question_answering/qasrl-forked/ProPara.xlsx")
df = xl.parse('State_change_annotations')

def writedescription(file, participant, pdescription):
    splitds = pdescription.split(";")
    splitds = [x.strip() for x in splitds]
    for p in splitds:
        file.write("description(")
        file.write(participant)
        file.write(",\"")
        file.write(p)
        file.write("\").\n")
    return    
        
def printParticipants(file, n):
    file.write("participant(")
    for i in range(n):
        if (i!=0):
            file.write(";")
        file.write("p")
        file.write(str(i+1))
    file.write(").")    
        

pidToEntAndlocs = defaultdict(dict)
for row in df.iterrows():
    if (not(pd.isnull(row[1][0]))):
        pid = str(row[1][0])
        if (row[1][1]=="SID"):
            pidToEntAndlocs[pid]["entities"] = list(row[1][3:].dropna())     
        elif ((type(row[1][1])==str) and (row[1][1].startswith("state"))):
            x = list(row[1][3:].dropna())
            z = list(filter(lambda a: a != '-', x))
            locs = [tok.strip(". ") for ents in z for tok in list(set(ents.split("|"))) if tok!='?']
            locs = list(set(locs))
            pidToEntAndlocs[pid]["locations"] = locs
        elif ( (type(row[1][1])==str) and (row[1][1]=="event1")):
            pidToEntAndlocs[pid]["text"] = row[1][2]
        elif ( (type(row[1][1])==str) and (row[1][1].startswith("event"))):
            pidToEntAndlocs[pid]["text"] = pidToEntAndlocs[pid]["text"] + " " + row[1][2]
            
            
            
print(pidToEntAndlocs)  