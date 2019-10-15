# -*- coding: utf-8 -*-
import random
import requests
import time
def get_random_agent():
    user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    headers={'User-Agent': random.choice(user_agent)}
    return  headers
def get_useful_proxy():
    proxy = [
        {'http': 'http://****:****@**.**.***.106:808', 'https': 'https://****:****@**.**.***.106:808', },
        {'http': 'http://****:****@**.**.***.102:808', 'https': 'https://****:****@**.**.***.102:808', },
        {'http': 'http://****:****@**.**.***.103:808', 'https': 'https://****:****@**.**.***.103:808', },
        {'http': 'http://****:****@**.**.***.108:808', 'https': 'https://****:****@**.**.***.108:808', },
        {'http': 'http://****:****@**.**.151.125:808', 'https': 'https://****:****@**.**.151.125:808', },
        {'http': 'http://****:****@**.**.***.53:888', 'https': 'https://****:****@**.**.***.53:888', },
        {'http': 'http://****:****@**.**.***.166:888', 'https': 'https://****:****@**.**.***.166:888', },
        {'http': 'http://****:****@**.**.***.143:808', 'https': 'https://****:****@**.**.***.143:808', },
        {'http': 'http://****:****@**.**.***.166:888', 'https': 'https://****:****@**.**.***.166:888', },
        {'http': 'http://****:****@**.**.***.107:808', 'https': 'https://****:****@**.**.***.107:808', },
        {'http': 'http://****:****@**.**.***.166:888', 'https': 'https://****:****@**.**.***.166:888', },
        {'http': 'http://****:****@**.**.***.228:888', 'https': 'https://****:****@**.**.***.228:888', },
        {'http': 'http://****:****@**.**.***.68:888', 'https': 'https://****:****@**.**.***.68:888', },
        {'http': 'http://****:****@**.**.***.140:888', 'https': 'https://****:****@**.**.***.140:888', },
        {'http': 'http://****:****@**.**.***.105:808', 'https': 'https://****:****@**.**.***.105:808', },
        {'http': 'http://****:****@**.**.***.104:808', 'https': 'https://****:****@**.**.***.104:808', },
        {'http': 'http://****:****@**.**.***.139:808', 'https': 'https://****:****@**.**.***.139:808', },
        {'http': 'http://****:****@**.**.***.136:808', 'https': 'https://****:****@**.**.***.136:808', },
        {'http': 'http://****:****@**.**.***.110:808', 'https': 'https://****:****@**.**.***.110:808', },
        {'http': 'http://****:****@**.**.***.135:808', 'https': 'https://****:****@**.**.***.135:808', },
        {'http': 'http://****:****@**.**.***.142:808', 'https': 'https://****:****@**.**.***.142:808', },
        {'http': 'http://****:****@**.**.***.134:808', 'https': 'https://****:****@**.**.***.134:808', },
        {'http': 'http://****:****@**.**.***.138:808', 'https': 'https://****:****@**.**.***.138:808', },
        {'http': 'http://****:****@**.**.***.137:808', 'https': 'https://****:****@**.**.***.137:808', },
        {'http': 'http://****:****@**.**.***.141:808', 'https': 'https://****:****@**.**.***.141:808', },
        {'http': 'http://****:****@**.**.***.218:808', 'https': 'https://****:****@**.**.***.218:808', },
        {'http': 'http://****:****@**.**.***.219:808', 'https': 'https://****:****@**.**.***.219:808', },
    ]
   # proxies = random.choice (proxy)
    #循环，如果代理不可用，换代理，最多更换10次
    for i in range(0,10):
#        time.sleep(2)
        proxie = random.choice (proxy)
        url='https://search.51job.com/list/000000,000000,0000,00,9,99,%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8,2,1.html?'
        try:

            res=requests.get(url,headers=get_random_agent(),proxies=proxie)
           # print res
            if res.status_code!=200:
                print "不可用代理：",
                print proxie
            else:
                break
        except:
            print "proxy error"
    return proxie

