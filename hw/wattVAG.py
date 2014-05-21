#-*- coding: utf-8 -*-  
#coding=utf-8  
'''
Created on 2014-3-27 8:46:37

@author: liufangyi

count watt 统计20S平均功率
'''

def loadData(fileName):      
    time = []; watt = []
    fr = open(fileName)
    count = 1                 
    wattCount = 0
    wattTotal = 0
    wattErrorCount = 0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if count == 20 :
            if wattErrorCount == 20 :
                watt.append(0)
            else :
                watt.append(float(wattTotal) / float(wattCount))
            wattErrorCount = 0
            count = count - 20
            wattTotal = 0
            wattCount = 0
        if count == 1 :
            time.append(curLine[0])
        if float(curLine[1]) > 0 :
            wattCount = wattCount + 1
            wattTotal = wattTotal + float(curLine[1])
        else :
            wattErrorCount = wattErrorCount + 1
        #print (curLine[0])
        #print (curLine[1])
        count=count + 1
        #print (wattErrorCount)
    #print (len(fr.readlines()))
    print (len(time))
    print (len(watt))
    f = open(r"F:\Study\testData\\out.txt","w")
    dataOut = []
    for i in range(len(watt)) :
        dataString = str(float('%.4f'% watt[i]))+'\n'
        dataOut.append(dataString)
    f.writelines(dataOut)
    f.close


if __name__ == '__main__':
    inputFileName = raw_input("请输入功率文件路径：")
    #print inputFileName
    #time,watt = loadData(inputFileName)
    #fileName = ('F:\wattCount\\2014-3-26-01.txt')
    loadData(inputFileName)