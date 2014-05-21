#-*- coding: utf-8 -*-  
#coding=utf-8  
'''
Created on 2014-3-27 15:51:00

@author: liufangyi

count watt var
'''
from collections import deque
import math
import os

def varData(list):   
    num = len(list)
    sum = 0
    squaSum = 0
    for i in range(num):
        sum = sum + float(list[i])
    for i in range(num):
        squaSum = squaSum + (float(list[i])-sum/num )**2
    return squaSum**0.5

def ifTimePoint(str):      
    curLine = str.strip().split(':')
    time = cmp(curLine[2],'20')*cmp(curLine[2],'40')*cmp(curLine[2],'00') 
    return time

def loadData(fileName):      
    time = []; watt = []
    queue = deque([])    
    fr = open(fileName)
    for count, line in enumerate(open(fileName, 'rU')): 
        count += 1
    for line in fr.readlines():
        curLine = line.strip().split(',')
        time.append(curLine[0])
        watt.append(curLine[1])
    return time ,watt

def processData(Time,Watt,N):      
    time = Time
    watt = Watt
    outTime = [];outWatt = [];var = [];wattList = []
    for i in range(len(time)):
        if ifTimePoint(time[i]) == 0:
            outTime.append(time[i])
            outWatt.append(watt[i])
            if i == 0:
                for j in range(int(N)+1):
                    wattList.append(watt[i+j])
                var.append(varData(wattList))
                wattList = []
            else :
                for j in range(-int(N),int(N)+1):
                    wattList.append(watt[i+j])
                var.append(varData(wattList))
                wattList = []
    return outTime,outWatt,var

def outData(Time,Watt,Var):
    try:
        time = Time
        watt =  Watt
        var = Var
        f = open(r"F:\Study\testData\out_var.csv","w")
        dataOut = []
        for i in range(len(watt)) :
            dataString = str(time[i])+','+watt[i]+','+str(float('%.4f'% var[i]))+'\n'
            dataOut.append(dataString)
            f.writelines(dataOut)
    except Exception, e:
        print e
    finally:
        print 'out put out_var.csv.csv success!'
        f.close


if __name__ == '__main__':
    os.system("F:\Workspace\HWprj\hw\handle_watt_data.py")
    inputFileName = raw_input("请输入功率文件路径：")
    #print inputFileName
    time,watt = loadData(inputFileName)
    outTime,outWatt,outVar = processData(time,watt,2)
    outData(outTime,outWatt,outVar)