import requests
from bs4 import BeautifulSoup as bs

dataFromWeb = []  # 存放我们从网上找到的数据，每个列表元素就是一条记录
stocks = ['平安银行', '万科A', '金田A', '国华网安', 'ST星源']


def getData(stockNum, year, season):
    # 这个函数接收到查询的股票号，对应的年，季度之后生成URL开始查找，
    # 并对于每条记录自己额外生成股票号，年，月三个维度的信息之后使用
    print(f"Trying to get {stocks[stockNum]} data in {year}年{season}季度")
    dictKey = {"year": year, "season": season}
    url = f'http://quotes.money.163.com/trade/lsjysj_00000{stockNum}.html'
    htmlCode = requests.get(url, params=dictKey)
    htmlCode.encoding = "utf-8"
    oBS = bs(htmlCode.text, "html.parser")
    tableCode = oBS.find("table", {"class": "table_bg001 border_box limit_sale"})  # 找到放置股票信息的表单元素
    for tr in tableCode.contents[3:-1]:  # 直接取contents，生成的列表里面第0,1,2,倒数第一个元素是无用的
        trData = [str(stockNum), '', '']  # 每条记录前三个元素是自己额外生成股票号，年，月
        elems = tr.contents
        for elem in elems:  # 获得每个表格单元（td)里面的值并添加到记录trData里面
            eleString = elem.string
            # 如果发现这个元素存放的是日期（形如2018-10-11),就先对应的解析其月份信息并填充每条记录的年，月
            if len(eleString) == 10 and '-' in eleString:
                trData[1] = str(year)  # 获得年
                trData[2] = eleString[5:7]  # 获得月
            trData.append(eleString)
        dataFromWeb.append(trData[:])


if __name__ == "__main__":
    for stocknum in range(1, 6):
        if stocknum == 3:  # 跳过已经退市的股票3
            continue
        for year in range(2015, 2022):
            for season in range(1, 5):
                getData(stocknum, year, season)
    outputFile = open("dataFromWeb.txt", "w")  # 先存到一个txt里面
    for linedata in dataFromWeb:
        print(" ".join(linedata), file=outputFile)
    outputFile.close()
