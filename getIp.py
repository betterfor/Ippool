import requests
from bs4 import BeautifulSoup
import DBHelper

class IPpool:
    # 构造函数
    def __init__(self):
        self.userAgent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        self.get_url = 'https://www.xicidaili.com/nn/'
        self.headers = {'User-Agent':self.agent}
        self.connurl = 'https://www.baidu.com'
        self.dbHelper = DBHelper.DBHelper()

    # 获取地址
    def getIps(self,page):
        for numpage in range(1,page+1):
            print('Now Downloading the '+str(page*100)+ ' ips')
            ipurl = self.get_url + str(numpage)
            request = requests.get(ipurl,headers=self.headers)
            print(request)
            bs = BeautifulSoup(request.content,'html.parser')
            res = bs.find_all('tr')
            for item in res[1:]:
                tds = item.find_all('td')
                protocol = str(tds[5].text)
                ip = str(tds[1].text)
                port = str(tds[2].text)
                # 每获取一条数据插入到数据库中
                self.dbHelper.insertDB(protocol.lower(),ip,port)
                # print(protocol.lower(),ip,port)
                # self.dbHelper.insertDB(protocol.lower(),ip,port)

    def getIpsProxy(self,page,proxy):
        for numpage in range(1,page+1):
            print('Now Downloading the '+str(page*100)+ ' ips')
            ipurl = self.get_url + str(numpage)
            request = requests.get(ipurl,headers=self.headers,proxies=proxy)
            print(request)
            bs = BeautifulSoup(request.content,'html.parser')
            res = bs.find_all('tr')
            for item in res[1:]:
                tds = item.find_all('td')
                protocol = str(tds[5].text)
                ip = str(tds[1].text)
                port = str(tds[2].text)
                # 每获取一条数据插入到数据库中
                self.dbHelper.insertDB(protocol.lower(),ip,port)


    # 校验ip
    def validip(self,protocol,ip,port):
        proxy = {protocol:ip+":"+port}
        p = requests.get(self.connurl,headers=self.headers,proxies=proxy)
        if p.status_code == 200 :
            return True
        return False

    # 获取一条可用的ip
    def getIp(self):
        while True:
            row = self.dbHelper.queryDB()
            has = self.validip(row[1],row[2],row[3])
            if has == False:
                # 去掉不能用的ip
                self.dbHelper.deleteDB(row[0])
                print("ip连接超时，重新获取")
            else:
                break
        # 删除已使用的ip，不删，多用点
        # self.dbHelper.deleteDB(row[0])
        proxy_dict = {row[1]: row[2] + ":" + row[3]}
        return proxy_dict

if __name__=='__main__':
    ip = IPpool()
    # ip.getIps(1)

    proxy_dict = ip.getIp()
    print("使用代理：", proxy_dict)

    # 使用代理ip爬取ip，防封ip
    # ip.getIpsProxy(10,proxy_dict)