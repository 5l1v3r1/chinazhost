import os
import sys
import socket
import grequests
from pyquery import PyQuery as pq

class scan:
    def __init__(self,url,option):
        self.result=""
        self.opt = option
        self.ip = socket.gethostbyname(url.split("/")[2])
        if option:
            self.iplist=[".".join(self.ip.split(".")[:3])+"."+str(x) for x in range(1,255)]
        else:
            self.iplist=[self.ip]
        self.taskhandel(self.taskset())
        with open("result.txt","w") as resultfile:
            resultfile.write(self.result)

    def taskset(self):
        genurl=[]
        tasks=[grequests.get("http://s.tool.chinaz.com/same?s={ip}".format(ip=x)) for x in self.iplist]
        raw=grequests.map(tasks, size=30)
        for i in raw:
            d=pq(i.url)
            count=d("#pn").attr("count")
            if count:
                for t in range(int(count)):
                    genurl.append("{url}&page={num}".format(url=i.url,num=str(t+1)))
            else:
                if d("div.w30-0.overhid>a").text().split(" ") == ['']:
                    print("IP:{ip} doesn't find same host website".format(ip=i.url.split("=")[1]))
                else:
                    self.htmlread(d)
        return genurl

    def taskhandel(self,tasklist):
        tasks = [grequests.get(x) for x in tasklist]
        raw = grequests.map(tasks, size=30)
        for i in raw:
            self.htmlread(pq(i.text))

    def htmlread(self,d):
        result = d("div.w30-0.overhid>a").text().split(" ")
        for i in result:
            print("[+]http://{url}/".format(url=i))
            self.result += "http://{url}/\n".format(url=i)


if __name__ == "__main__":
    try:
        url=sys.argv[2] if "http" in sys.argv[2] else "http://{url}".format(url=sys.argv[2])
        option=1 if "-c" in sys.argv[1] else 0
    except:
        print('''
        Usage: 
            python main.py -c http://www.xxxx.com/
            python main.py -p http://www.xxxx.com/
        ''')
        sys.exit()
    if os.path.exists("result.txt"):
        sys.stdout.write("result.txt exists, Do u want to replace it? [Y/n]:")
        scantype = sys.stdin.readline()
        if scantype=="n":
            print("Bye")
        else:
            test = scan(url=url, option=option)
    else:
        test = scan(url=url, option=option)









