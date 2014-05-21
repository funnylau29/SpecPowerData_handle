#-*- coding: utf-8 -*-  
#!/usr/bin/env python
'''
Created on 2014-5-12

@author: liufangyi
'''
import time
import re
import math
import os
from collections import deque
from config import INPUT_URL,OUTPUT_URL
from compiler.ast import TryExcept
#===============================================================================
# 判断是否为正浮点数
#===============================================================================
def isfolat(Str):
    p = re.compile(r'^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$')
    m = p.match(Str)
    if m:
        return True
    else:
        return False

#===============================================================================
# 加载数据
#===============================================================================
def loadData(fileName):      
    wattTime = []; watt = []
    try:
        fr = open(fileName)
        for line in fr.readlines():
            curLine = line.strip().split(',')
            if curLine[0].isdigit() and isfolat(curLine[12])  == True:     #判断是否是数字编号开头的有效数据
                wattTime.append(curLine[1])
                watt.append(curLine[12])
    except Exception as err:
        print err
    return wattTime ,watt

def cmpTime(time1,time2):           #比较时间，判断时间相差几秒
    timeData1 = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    timeData2 = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    return timeData2-timeData1

def processData(Time,Watt):      #检查时间是否是每一秒取一个
    wattTime = Time
    wattData = Watt
    #print "wattTime:",len(wattTime),"wattData:",len(wattData)
    timMin  = time.mktime(time.strptime(wattTime[0],'%Y-%m-%d %H:%M:%S'))
    #print timMin,"timMin"
    timMax  = time.mktime(time.strptime(wattTime[len(wattTime)-1],'%Y-%m-%d %H:%M:%S'))
    #print timMax,"timMax"
    timeNum = timMax-timMin+1
    for i in range(len(wattTime)):
        if i < len(wattTime)-1:   #如果不是最后一秒
            timeData1 = time.mktime(time.strptime(wattTime[i],'%Y-%m-%d %H:%M:%S'))
            N =cmpTime(wattTime[i],wattTime[i+1])
            if (N) > 1:
                addTime =time.localtime(timeData1 + 1)
                addTimeStr = time.strftime('%Y-%m-%d %H:%M:%S',addTime)
                wattTime.insert(i+1,addTimeStr)          #时间加1s
                wattData.insert(i+1,'0')
    if len(wattTime) == timeNum:             
        return wattTime,wattData
    else :
        processData(wattTime,wattData)      #递归
        return wattTime,wattData


def outData(fileName,Time,Watt):
    wattTime = Time
    watt =  Watt
    try:
        fileName= fileName+'\\Watt_Data_Out.csv'
        f = open(fileName,"w")
        dataOut = []
        for i in range(len(watt)) :
            dataString = str(wattTime[i])+','+watt[i]+'\n'
            dataOut.append(dataString)
        f.writelines(dataOut)
    except Exception, e:
        print e
    finally:
        print 'out put Watt_Data_Out.csv success!'
        f.close

def save_watt_data(URL):
    inputFileName = URL
    #inputFileName = raw_input("请输入功率文件路径：")
    print "输入路径:",inputFileName
    wattTime,wattData = loadData(inputFileName)
    #outputFileName = raw_input("请输入输出路径：")
    outputFileName =r"F:\Study\testData"
    outTime,outWatt = processData(wattTime,wattData)
    outData(outputFileName,outTime,outWatt)
    
#===============================================================================
# 计算方差    输入：list  输入：方差 
# #===============================================================================
def varData(list):   
    num = len(list)
    sum = 0
    squaSum = 0
    for i in range(num):
        sum = sum + float(list[i])
    for i in range(num):
        squaSum = squaSum + (float(list[i])-sum/num )**2
    return squaSum**0.5

#===============================================================================
# 判断是不是00 ，20  ，40 S 时 取到的功率值
#===============================================================================
def ifTimePoint(str):      
    curLine = str.strip().split(':')
    time = cmp(curLine[2],'20')*cmp(curLine[2],'40')*cmp(curLine[2],'00') 
    return time

def load_var_Data(fileName):      
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

def process_var_Data(Time,Watt,N):      
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

def out_var_Data(Time,Watt,Var):
    try:
        time = Time
        watt =  Watt
        var = Var
        f = open(r"F:\Study\testData\out_var.csv","w")
        dataOut = []
        print 'len(watt):',len(watt)
        for i in range(len(watt)) :
            dataString = str(time[i])+','+watt[i]+','+str(float('%.4f'% var[i]))+'\n'
            dataOut.append(dataString)
            f.writelines(dataOut)
    except Exception, e:
        print e
    finally:
        print 'out put out_var.csv.csv success!'
        f.close
def save_var_watt_data():
    #inputFileName = raw_input("请输入功率文件路径：")
    inputFileName = r"F:\Study\testData\Watt_Data_Out.csv"
    time,watt = load_var_Data(inputFileName)
    outTime,outWatt,outVar = process_var_Data(time,watt,2)
    out_var_Data(outTime,outWatt,outVar)

if __name__ == '__main__':
    #INPUT_URL = raw_input("请输入功率文件路径：")
    save_watt_data(INPUT_URL)
    save_var_watt_data()