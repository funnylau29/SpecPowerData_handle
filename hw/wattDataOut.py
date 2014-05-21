# -*- coding: utf-8 -*-  
# coding=utf-8  
'''
Created on 2014-3-27 8:46:37

@author: liufangyi

提取spec中读取功率仪记录文件ccs-log.csv，整理watt初始数据，按格式输出
'''
import time

def loadData(fileName):      
    wattTime = []; watt = []
    # queue = deque([])    #队列
    fr = open(fileName)
    # for count, line in enumerate(open(fileName, 'rU')): #统计有多少行
    #    count += 1
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if curLine[0].isdigit() == True:  # 判断是否是数字编号开头的有效数据
            wattTime.append(curLine[1])
            watt.append(curLine[12])
    return wattTime , watt
'''
def loadData1(fileName):      
    wattTime = []; watt = []
    #queue = deque([])    #队列
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        #if curLine[0].isdigit() == True:           #判断是否是数字编号开头的有效数据
        wattTime.append(curLine[0])
        watt.append(curLine[1])
    print wattTime
    return wattTime ,watt
'''

def cmpTime(time1, time2):  # 比较时间，判断时间相差几秒
    timeData1 = time.mktime(time.strptime(time1, '%Y-%m-%d %H:%M:%S'))
    timeData2 = time.mktime(time.strptime(time2, '%Y-%m-%d %H:%M:%S'))
    return timeData2 - timeData1

'''
def processData(Time,Watt):      #检查时间是否是每一秒取一个
    wattTime = Time
    wattData = Watt
    timMin = timeData1 = time.mktime(time.strptime(wattTime[0],'%Y-%m-%d %H:%M:%S'))
    timMax = timeData1 = time.mktime(time.strptime(wattTime[len(wattTime)-1],'%Y-%m-%d %H:%M:%S'))
    print (timMax-timMin)
    for i in range(int(timMax-timMin)):
        if i < len(wattTime)-1:   #如果不是最后一秒
        #print (wattTime[i])
            timeData1 = time.mktime(time.strptime(wattTime[i],'%Y-%m-%d %H:%M:%S'))
            N =cmpTime(wattTime[i],wattTime[i+1])
            #print str(N)+'one'
            while (N) > 1:
                #print wattTime[i]+' time error'
                addTime =time.localtime(timeData1 + 1)
                addTimeStr = time.strftime('%Y-%m-%d %H:%M:%S',addTime)
                wattTime.insert(i+1,addTimeStr)
                N = N - 1
                print N
                print len(wattTime)
        print wattTime
    #return outTime,outWatt,
'''

def processData1(Time, Watt):  # 检查时间是否是每一秒取一个
    wattTime = Time
    wattData = Watt
    timMin = timeData1 = time.mktime(time.strptime(wattTime[0], '%Y-%m-%d %H:%M:%S'))
    timMax = timeData1 = time.mktime(time.strptime(wattTime[len(wattTime) - 1], '%Y-%m-%d %H:%M:%S'))
    timeNum = timMax - timMin + 1
    for i in range(len(wattTime)):
        if i < len(wattTime) - 1:  # 如果不是最后一秒
            timeData1 = time.mktime(time.strptime(wattTime[i], '%Y-%m-%d %H:%M:%S'))
            N = cmpTime(wattTime[i], wattTime[i + 1])
            if (N) > 1:
                addTime = time.localtime(timeData1 + 1)
                addTimeStr = time.strftime('%Y-%m-%d %H:%M:%S', addTime)
                wattTime.insert(i + 1, addTimeStr)  # 时间加1s
                wattData.insert(i + 1, '0')
    if len(wattTime) == timeNum:             
        return wattTime, wattData
    else :
        processData1(wattTime, wattData)  # 递归
        return wattTime, wattData


def outData(fileName, Time, Watt):
    wattTime = Time
    watt = Watt
    try:
        fileName = fileName + '\\Watt_Data_Out.csv'
        f = open(fileName, "w")
        dataOut = []
        for i in range(len(watt)) :
            dataString = str(wattTime[i]) + ',' + watt[i] + '\n'
            dataOut.append(dataString)
        f.writelines(dataOut)
    except Exception, e:
        print e
    finally:
        print 'out put Watt_Data_Out.csv success!'
        f.close


if __name__ == '__main__':
    inputFileName = r"F:\Study\testData\ssj.0001.ccs-log.csv"
    # inputFileName = raw_input("请输入功率文件路径：")
    print inputFileName
    wattTime, wattData = loadData(inputFileName)
    
    # outputFileName = raw_input("请输入输出路径：")
    outputFileName = r"F:\Study\testData"
    outTime, outWatt = processData1(wattTime, wattData)
    outData(outputFileName, outTime, outWatt)

'''  
    #print "请输入功率文件路径："
    inputFileName = raw_input("请输入功率文件路径：")
    #fileName = r(fileName)
    print inputFileName
    wattTime,wattData = loadData(inputFileName)
    outputFileName = raw_input("请输入输出路径：")
    #outTime,outWatt = processData1(wattTime,wattData，outputFileName)
    outTime,outWatt = processData1(wattTime,wattData)
    outData(outputFileName,outTime,outWatt)
    #time1="2014/3/26  9:55:14"
    # time2="2014/3/26  11:07:42"
    #timeData1 = time.mktime(time.strptime(time1,'%Y/%m/%d %H:%M:%S'))
    #timeData2 = time.mktime(time.strptime(time2,'%Y/%m/%d %H:%M:%S'))
    #t1 = time.strptime(time1,"%Y%m%d")
    #print timeData2-timeData1+1

    #A = datetime.now()
    #print    A
'''
    