from flask import Flask, render_template, request
import sqlite3

# 每张表的开头字符串
tableHead = '''
		<table class="stockTable">
            <thead>
                <tr class="cell">
                    <th class="cell">日期</th>
                    <th class="cell">开盘价</th>
                    <th class="cell">最高价</th>
                    <th class="cell">最低价</th>
                    <th class="cell">收盘价</th>
                    <th class="cell">涨跌额</th>
                    <th class="cell">涨跌幅(%)</th>
                    <th class="cell">成交量(手)</th>
                    <th class="cell">成交金额(万元)</th>
                    <th class="cell">振幅(%)</th>
                    <th class="cell">换手率(%)</th>
                </tr>
            </thead>
            <tbody>
        '''
# 每张表的结尾字符串
tableTail = "</tbody></table>"

stockWeb = Flask(__name__)


@stockWeb.route("/")  # 主界面
def root():
    return render_template("stock_show.html")


# 服务器，接受股票号，年，月信息之后再找出所有的符合要求的记录按照时间降序排列并返回
@stockWeb.route("/server", methods=("POST", "GET"))
def server():
    stockNum = request.args.get('stockNum')
    year = request.args.get("year")
    month = request.args.get("month")
    if len(month) == 1:  # 月份必须是两位数，比如“04”，位数不够就在前面补零
        month = '0' + month
    dbConn = sqlite3.connect("stockData.db")

    # 在数据库中按照要求找出所有符合要求的数据并按照时间降序排列
    command = f"""select * from FiveStockInfo where stockNum='{stockNum}' 
    and year='{year}' and month='{month}' order by date desc"""
    myCursor = dbConn.execute(command)
    stockInfo = myCursor.fetchall()  # 获得所有符合的记录

    # 生成字符串appendInfo,表示所有记录对应的表单元素,即table的核心tr,td部分
    appendInfo = ""
    for index, info in enumerate(stockInfo):

        # beginColor是表示开盘值相对于上一次收盘值是涨是跌
        if index == len(stockInfo) - 1:  # 最早的一个记录无法比较，默认是绿色
            beginColor = 'colorGreen'
        else:
            nextInfo = stockInfo[index + 1]
            beginColor = 'colorRed' if info[4] > nextInfo[7] else 'colorGreen'

        highestColor = 'colorRed' if info[5] > info[4] else 'colorGreen'
        lowestColor = 'colorRed' if info[6] > info[4] else 'colorGreen'
        endColor = 'colorRed' if info[7] > info[4] else 'colorGreen'
        # 这三条记录分别表示最高值，最低值以及收盘值相对于开盘值是涨是跌

        addInfo = f'''
                    <tr class="cell">
                        <td class="cell">{info[3]}</td>
                        <td class="cell {beginColor}">{info[4]}</td>
                        <td class="cell {highestColor}">{info[5]}</td>
                        <td class="cell {lowestColor}">{info[6]}</td>
                        <td class="cell {endColor}">{info[7]}</td>
                        <td class="cell {endColor}">{info[8]}</td>
                        <td class="cell {endColor}">{info[9]}</td>                                
                        <td class="cell">{info[10]}</td>
                        <td class="cell">{info[11]}</td>
                        <td class="cell">{info[12]}</td>
                        <td class="cell">{info[13]}</td>
                        </tr>
                    '''
        appendInfo += addInfo
    dbConn.close()

    # 最后三个字符串结合，生成一个完整的table表单元素
    return tableHead + appendInfo + tableTail


if __name__ == "__main__":  # 新增代码
    stockWeb.run(host="0.0.0.0", port=80, debug=True)
