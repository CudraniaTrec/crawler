## 网络爬虫作业报告

1. 本次作业完成爬取数据并呈现任务主要使用了reptile.py, load2DB.py, stockShow.py 3个python文件
2. 主体思路是使用reptile.py将爬取的数据先存放在临时的dataFromWeb.txt文件之中，并且对每条数据生成额外的年，月等信息以便后续查询。
3. 然后通过load2DB.py正式读取dataFromWeb.txt文件的内容，并存入数据库stockData.db的表FiveStockInfo之中。
4. stockShow.py通过渲染templates.stock_show.html提供股票信息查询页面。每次用户请求某只股票某年某月的数据的时候，客户端向服务器提供股票编号，年，月。服务器生成并返回一个以字符串形式呈现的table表单元素，里面是所请求的股票数据以及对应的颜色标签等，然后客户端接收到这个字符串之后直接将其渲染到我们的页面之中。
5. 更多详细信息请查看代码的注释。