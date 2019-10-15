# -*- coding: utf-8 -*-
#这里的agent_proxy模块是自己另外写的请求头和IP代理随机获取模块
from agent_proxy import get_random_agent,get_useful_proxy
import requests
from bs4 import BeautifulSoup
import threading
import HTMLParser
import datetime
import pymysql
import re
import ssl
import time
import random
import sys
from Queue import Queue
reload (sys)
sys.setdefaultencoding ("utf-8")
ssl._create_default_https_context = ssl._create_unverified_context

lock = threading.RLock()

headers=get_random_agent()
proxies=get_useful_proxy()
#数据插入的数据库
# db2 = pymysql.connect (host='10.140.85.247', user='hs_dev_mw', password='084f46f92537', port=6633, db='data_center', charset='utf8mb4')
db2 = pymysql.connect (host='******', user='******', password='******', port=6633, db='******', charset='******')
cursor2 = db2.cursor ()


#公司500强数据库
db = pymysql.connect (host='******', user='******', password='******', port=4000, db='******', charset='utf8')
cursor = db.cursor ()




def get_page_url(company_dict):
    """
    判断500强公司全名是否有匹配的工作岗位，没有则调用delete_com_tail方法处理掉公司全名后面属性
    有就继续往下执行
    :param each_company:
    :param each_id:
    :return:
    """
    page_proxie = get_useful_proxy ()
    each_company=company_dict[0].encode ('utf-8')
    each_id=company_dict[1]
    print "正在抓取：" + each_company
    page_url='https://search.51job.com/list/000000,000000,0000,00,9,99,'+each_company+',1,1.html?'
    print page_url
    try:
        res=requests.get(page_url,headers =headers,proxies=page_proxie)
        soup = BeautifulSoup (res.content, 'html.parser', from_encoding='utf8')
        url_tag = soup.find_all ('p', class_="t1")
    except Exception as e:
        pass
    # 没有符合条件的职位
    if not url_tag:
        delete_com_tail (each_company,each_id,page_proxie)
    else:
        parse_index_page (soup,url_tag,each_company,each_id,page_proxie)

def delete_com_tail (each_company,each_id,page_proxie):
    """
    如果公司原名无法匹配到相关职位，去掉“股份有限供公司”、“控股有限公司”、“有限公司”，用公司前面关键词在
    https://mq.51job.com/joblist.php?keyword=' + each_company + '&jobarea=000000&lang=c网页中查找
    :param each_company:
    :param each_id:
    :param page_proxie:
    :return:
    """
    headers=get_random_agent()
    proxies=get_useful_proxy()
    if '控股有限公司' in each_company:
        each_company = each_company.replace, "")
    elif '股份有限公司' in each_company:
        each_company = each_company.replace ("股份有限公司", "")
    elif '有限公司' in each_company:
        each_company = each_company.replace ("有限公司", "")
    if each_company == '北京':
        return
    url = 'https://mq.51job.com/joblist.php?keyword=' + each_company + '&jobarea=000000&lang=c'
    try:

        res = requests.get (url, headers=headers, proxies=proxies)
        soup = BeautifulSoup (res.content, 'html.parser', from_encoding='utf8')
        url_tag = soup.find_all ('strong', class_="title")
    except Exception as e:
        pass

    if not url_tag:
        print each_company+"没有相关联的岗位"
    else:
        parse_index_page (soup, url_tag, each_company, each_id, page_proxie)

def parse_index_page(soup,url_tag,each_company,each_id,page_proxie):
    """
    解析列表页，判断是否需要翻页，并进行进一步处理
    :param soup:
    :param url_tag:
    :param each_company:
    :param each_id:
    :param page_proxie:
    :return:
    """
    page_num = soup.find ('span', class_="td").text
    page_num = re.findall ("\d+", page_num)[ 0 ]

    if int(page_num)!=1:
        try:

            for page in range(2,int(page_num)+1):
                if 'strong class="title' not in str(url_tag):
                    next_page_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,'+str(each_company)+',1,' + str(page) + '.html?'
                    res = requests.get (next_page_url, headers=headers, proxies=proxies)
                    soup = BeautifulSoup (res.content, 'html.parser', from_encoding='utf8')
                    url_tag = soup.find_all ('p', class_="t1")
                else:
                    next_page_url='https://mq.51job.com/joblist.php?keyword='+str(each_company)+'&jobarea=000000&lang=c&page='+str(page)
                    print next_page_url
                    res = requests.get (next_page_url, headers=headers, proxies=proxies)
                    soup = BeautifulSoup (res.content, 'html.parser', from_encoding='utf8')
                    url_tag = soup.find_all ('strong', class_="title")
                print "翻页"
                print next_page_url
                page_proxie=get_useful_proxy()
                parse_tag_url (url_tag, each_company, each_id, page_proxie)
        except Exception as e:
            pass
    else:
        parse_tag_url (url_tag, each_company, each_id, page_proxie)

def parse_tag_url(url_tag,each_company,each_id,page_proxie):
    """
    #处理列表页的每个标签，取出详情页url,根据url在mysql进行去重
    :param url_tag:
    :param each_company:
    :param each_id:
    :param page_proxie:
    :return:
    """
    for each in url_tag:
        each_url = each.a[ 'href' ]
        # 根据job_url去重
        sql = "select job_url from ntf_tyc_com_job where job_url = ('%s')" % (each_url)
        try:
            db2.ping (reconnect=True)
            res = cursor2.execute (sql)
            if res:
                print "数据存在：" + each_url
                continue
        except:
            print "Error"
        detail_page (each_url, each_company, each_id, page_proxie)



def detail_page (each_url,each_company,each_id,page_proxie):
    """
    #解析详情页,取出需要信息
    :param each_url:
    :param each_company:
    :param each_id:
    :param page_proxie:
    :return:
    """
    time.sleep (0.001)

    try:
        res = requests.get (each_url, headers = headers, proxies=page_proxie)
        soup = BeautifulSoup (res.content, 'html.parser', from_encoding='utf8')
        #p判断是否是测试的岗位，如果是，丢弃
        test_job = soup.find ('div', class_='bmsg inbox')
        if test_job and '测试使用' in str(test_job):
            return
        job_info = {}

        job_info[ 'com_name' ] = each_company # 公司名称

        job_info[ 'come_source' ] = u'前程无忧'#数据源

        job_info[ 'com_id' ] = each_id #公司id，和天眼查公司关联取id

        job_info[ 'job_url' ] = each_url # 来源url

        job_info[ 'com_sname' ] = soup.find ('p', class_="cname").text # 招聘公司名称
        job_info[ 'job_name' ] = soup.find ('h1').text # 招聘岗位


        job_info[ 'job_salary' ] = soup.find ('div', class_="cn").strong.text # 薪资
        info = soup.find_all ('span', class_="sp4")
        #详情页有工作经验、学历要求、招聘人数、发布时间、学历的情况
        if len (info) == 4:

            job_info[ 'work_exp' ] = info[ 0 ].text # 工作经验

            job_info[ 'job_edu' ] = info[ 1 ].text # 学历要求

            job_info[ 'recruit_number' ] = info[ 2 ].text.replace("招","") # 招聘人数

            pub_time = info[ 3 ].text.replace ("发布", "")
            pub_time_v2 = '2018-' + str (pub_time)
            job_info[ 'stat_date' ] = pub_time_v2.replace ("-", "/")  # 招聘发布时间

            d = datetime.datetime.strptime (pub_time_v2, '%Y-%m-%d')
            seven_day = datetime.timedelta (days=7)
            da_days = d + seven_day
            job_info[ 'closing_date' ] = da_days.strftime ('%Y-%m-%d').replace ("-", "/")# 招聘截止时间

        # 详情页只有工作经验、招聘人数、发布时间、没有学历的情况
        else:
            job_info[ 'work_exp' ] = info[ 0 ].text# 工作经验

            job_info[ 'recruit_number' ] = info[ 1 ].text # 招聘人数

            pub_time = info[ 2 ].text.replace ("发布", "")
            pub_time_v2 = '2018-' + str (pub_time)
            job_info[ 'stat_date' ] = pub_time_v2.replace ("-", "/")# 招聘发布时间

            d = datetime.datetime.strptime (pub_time_v2, '%Y-%m-%d')
            seven_day = datetime.timedelta (days=7)
            da_days = d + seven_day
            job_info[ 'closing_date' ] = da_days.strftime ('%Y-%m-%d').replace ("-", "/")   # 招聘截止时间


        job_info[ 'city' ]=soup.find ('div', class_="cn").span.text#城市
        if '-' in job_info['city']:#有“-”符号，取出城市下面的区
            city_area = job_info[ 'city' ]
            job_info[ 'city' ] = job_info[ 'city' ].split ('-')[ 0 ]

            job_info[ 'area' ] = city_area.split ('-')[ 1 ]   #城市下面的区域

        job_des_tag = soup.find ('div', class_="bmsg job_msg inbox")
        parser = HTMLParser.HTMLParser ()
        node = parser.unescape (job_des_tag)

        job_belong_tag = node.find ('div', class_="mt10")
        if job_belong_tag:
            job_belong_tag.decompose () # 去除包含工作类别、关键字等无用信息标签

        share_tag = node.find ('div', class_="share")
        share_tag.decompose ()   # 去除分享外链的标签

        job_info[ 'job_des' ] = node.text
        print each_url+'解析完成'
        insert_mysql (job_info)
    except Exception as e:
        pass

def insert_mysql(job_info):
    """
    #数据插入mysql数据库
    :param job_info:
    :return:
    """
    # lock.acquire()
    keys = ','.join (job_info.keys ())
    values = ','.join ([ '%s' ] * len (job_info))
    sql = 'INSERT INTO ntf_tyc_com_job({keys}) values({values})'.format (keys=keys, values=values)
    db2.ping (reconnect=True)
    try:
        if cursor2.execute (sql, tuple (job_info.values ())):
            print 'Data insert Succesful'
            db2.commit ()
    except:
        print "Data insert Failed"
        db2.rollback ()
    db2.close ()
    # lock.release()

if __name__ == '__main__':
    sql = 'SELECT com_name,com_id FROM ****** WHERE id <= 500'
    db.ping (reconnect=True)
    cursor.execute (sql)
    rowQueue = Queue(500)
    rows = cursor.fetchall ()
    for row in rows:
        rowQueue.put(row)
    threadcrawl = []
    while True:
        if threading.active_count() < 10:
            try:
                t = threading.Thread (target=get_page_url, args=(rowQueue.get(False),))
                t.setDaemon (True)
                threadcrawl.append(t)
                t.start ();
            except:
                pass

    for thread in threadcrawl:
        thread.join()
    db.close ()

