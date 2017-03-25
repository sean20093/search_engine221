# coding=utf8
import urllib2
import string
import urllib
import re
import random
import sys
from bs4 import BeautifulSoup
#设置多个user_agents，防止百度限制IP
'''
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
         'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
         (KHTML, like Gecko) Element Browser 5.0', \
          'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
          'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
          'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
         Version/6.0 Mobile/10A5355d Safari/8536.25', \
           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
              Chrome/28.0.1468.0 Safari/537.36', \
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
'''


def baidu_search(keyword, pn):
    p = {'wd': keyword}
    res = urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn))
    html = res.read()
    return html


def getList(regex, text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr


def getMatch(regex, text):
    res = re.findall(regex, text)
    print res
    if res:
        return res[0]
    return ""


def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("",text)
    return retval


def geturl(keyword):
    for page in range(1):
        pn = page*100+1
        html = baidu_search(keyword,pn)
        content = unicode(html, 'utf-8', 'ignore')
        arrList = getList("<table.*?class=\"result\".*?>.*?<\/a>", content)
        for item in arrList:
            print item
            regex = u"<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
            link = getMatch(regex,item)
            url = link[0]
            print uri
    #获取标题
    #title = clearTag(link[1]).encode('utf8')
            try:
                domain = urllib2.Request(url)
                r = random.randint(0,11)
                domain.add_header('User-agent', user_agents[r])
                domain.add_header('connection','keep-alive')
                response=urllib2.urlopen(domain)
                uri=response.geturl()
                print uri
            except:
                continue
if __name__=='__main__':
    geturl('python')


def search(key):
    search_url = 'http://www.baidu.com/s?wd=key&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'
    req = urllib2.urlopen(search_url.replace('key', key))
    result = []
    # 循环抓取10页结果进行解析
    for count in range(10):
        html = req.read()
        soup = BeautifulSoup(html,"lxml")

        file = open("result.txt", 'a')

        content = soup.findAll('table', id=re.compile("\d"))
        num = len(content)
        print num
        for i in range(num):
                # 先解析出来内容
            p_str = content[i].find('a')
                # 提取关键字
            if p_str.em:
                str = "".join(p_str.em.string)
                    # 提取缩略标题
            patt = re.compile(u"<\/em>(.*?)<\/a>")
            text = re.search(patt, unicode(p_str))
            if text:
                str += text.group(1)
                    # 构造字典序列
                # result +=[{str:p_str['href']}]
            file.write(str + u'\n' + unicode(p_str['href']) + u'\n')

        file.close()
            # 解析下一页
        next_page = 'http://www.baidu.com' + soup('a', {'href': True, 'class': 'n'})[0][
                'href']  # search for the next page
        req = urllib2.urlopen(next_page)

search("tcp")


'''
#geturl("tcp")
question_word = "吃货 程序员"
url = "http://www.baidu.com/s?wd=" + urllib.quote(question_word.decode(sys.stdin.encoding).encode('gbk'))
htmlpage = urllib2.urlopen(url).read()
soup = BeautifulSoup(htmlpage, "lxml")
#print soup
print len(soup.findAll("table", {"class": "result"}))
print len(soup.findAll("<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"))
for result_table in soup.findAll("table", {"class": "result"}):
    a_click = result_table.find("a")
    print "-----标题----\n" + a_click.renderContents()#标题
    print "----链接----\n" + str(a_click.get("href"))#链接
    print "----描述----\n" + result_table.find("div", {"class": "c-abstract"}).renderContents()#描述
    print
'''