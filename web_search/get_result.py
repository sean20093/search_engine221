# coding=utf8
from xgoogle.search import GoogleSearch, SearchError
try:
    gs = GoogleSearch("quick and dirty")
    gs.results_per_page = 50
    results = gs.get_results()
    for res in results:
        print res.title.encode("utf8")
        print res.desc.encode("utf8")
        print res.url.encode("utf8")
        print
except SearchError, e:
    print "Search failed: %s" % e
















'''
# coding=utf8
import sys
import urllib
import urllib2
from bs4 import BeautifulSoup

question_word = "tcp"
#url = "http://www.baidu.com/s?wd=" + urllib.quote(question_word.decode(sys.stdin.encoding).encode('gbk')) # print url
url = "https://www.google.com/#q=word&*"
url = url.replace("word", question_word)
print url
htmlpage = urllib2.urlopen(url).read() # print # htmlpage
soup = BeautifulSoup(htmlpage,"lxml") # print soup
print len(soup.findAll('div',{'class':'result c-container '}))
for result_table in soup.findAll('div',{'class':'result c-container '}):
    a_click = result_table.find("a")
    print"------title------\n" + a_click.renderContents() #标题
    print"------url------\n" + str(a_click.get("href"))#链接
    print"------des------\n" + "result_table.find('div',{'class':'c-abstract'})"# 描述  print
'''