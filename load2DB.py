import sqlite3

dbConn = sqlite3.connect("stockData.db")


def load2db(line):
    # 获得一条记录并且存入数据库之中
    dbConn.execute(f'''insert into FiveStockInfo
        (stockNum,year,month,date,opening,highest,lowest,finally,
        risefallABS,risefallREL,volumn,trans,amplitute,turnover)
        values('{line[0]}','{line[1]}','{line[2]}','{line[3]}','{line[4]}',
        '{line[5]}','{line[6]}','{line[7]}','{line[8]}','{line[9]}',
        '{line[10]}','{line[11]}','{line[12]}','{line[13]}')''')


dbConn.execute("drop table FiveStockInfo")
# 如果这张表已经存在就先删除掉

# 创建一个名叫FiveStockInfo的表用于存放所有记录
# 每条记录有14个维度，依次序分别是股票号，年，月，日期，开盘价，最高价，最低价，收盘价
# 涨跌额，涨跌幅(%)，成交量(手)，成交金额(万元)，振幅(%)，换手率(%)，对应的英文名尽量在准确了QWQ
dbConn.execute('''create table FiveStockInfo
        (stockNum varchar(1) not null,
        year varchar(4) not null,
        month varchar(2) not null,
        date varchar(10) not null,
        opening varchar(10) not null,
        highest varchar(10) not null,
        lowest varchar(10) not null,
        finally varchar(10) not null,
        risefallABS varchar(10) not null,
        risefallREL varchar(10) not null,
        volumn varchar(10) not null,
        trans varchar(10) not null,
        amplitute varchar(10) not null,
        turnover varchar(10) not null)''')

inputFile = open("dataFromWeb.txt", "r")
dataFromWeb = inputFile.read()
inputFile.close()
# 从暂时存放数据的TXT里面读取出信息之后就将其按照列分隔然后依次存入数据库之中
lines = dataFromWeb.splitlines()
for Line in lines:
    line = Line.split(sep=" ")
    load2db(line)
dbConn.commit()

# 获得表中元素测试一下
myCursor = dbConn.execute("select * from FiveStockInfo")
print(myCursor.fetchall())
myCursor.close()

dbConn.close()
