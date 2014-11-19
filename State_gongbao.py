#!/usr/bin/python
#-*- coding=utf-8 -*-
#crawler.py
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
from urllib import urlopen

#返回包含有class但并不包含sytle的div标签
def div_has_class_no_style(tag):
    return tag.has_attr('class') and not tag.has_attr('style')


code_text = urlopen('http://www.stats.gov.cn/tjsj/zxfb/201402/t20140224_514970.html').read()

soup = BeautifulSoup(code_text)
Trs_PreAppend = soup.find("div",class_ = "TRS_PreAppend")

title = soup.title.string

p_set = Trs_PreAppend.find_all(div_has_class_no_style)
text = ""

print 'get the text from : ' + str(title)

filename = str(title)+".txt"
f = open(filename,'w')

for p in p_set:
    #print p['class']
    span_set = p.find_all('span')
    #span_set = p.contents
    for span in span_set:
        if span.parent.name != "sup":
            st = str(span.string)
            if st != "" and st != " ":
                st.strip
                #print st
                text = text + st
    text = text + "\n"
f.write(text)
f.close()


#print p_set

#print(Trs_PreAppend.prettify())
#print text