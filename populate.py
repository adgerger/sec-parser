import os


fp = open("data/tickers.txt")
lines = fp.readlines()

for line in lines:
    line = line.strip('\n')
    line =  "data/" + line + '/'
    
    os.mkdir(line + "2020/processed")
    os.mkdir(line + "2019/processed")
    os.mkdir(line + "2018/processed")
    os.mkdir(line + "2017/processed")
    os.mkdir(line + "2016/processed")
   
    os.mkdir(line + "2020/unprocessed")
    os.mkdir(line + "2019/unprocessed")
    os.mkdir(line + "2018/unprocessed")
    os.mkdir(line + "2017/unprocessed")
    os.mkdir(line + "2016/unprocessed")

