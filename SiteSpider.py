#!/usr/bin/python
#encoding:utf-8
'''
Created on 2014-11-18
@author: Administrator-szx
'''
import platform
from sys import argv,stdout
from os import makedirs,sep
from os.path import dirname,exists,isdir,splitext,abspath
from string import replace,find
from htmllib import HTMLParser
from urllib import urlretrieve
from urlparse import urlparse
from formatter import DumbWriter,AbstractFormatter,NullFormatter
from email.header import UTF8
#from IPython.utils.io import raw_print
#from cStringIO import StringIO
#import model you need

DOM_SUFFIX = tuple(['.com','.gov','.net','.edu','.int','.cn',])
FILE_SUFFIX  = tuple(['html','htm',]) 
LOCPATH = abspath(dirname(argv[0]))

class Retriever(object):
    def __init__(self,url):
        self.url=url
        self.file=self.filename(url)
    def filename(self,url,deffile='index.html'):
        """
        生成下载连接和文件名
        """
        full_url = ""
        if url.endswith(DOM_SUFFIX):
            full_url = url + '/'
        else:
            full_url = url
        parsedurl=urlparse(full_url,'http:',0)
        path=parsedurl[1]+parsedurl[2]
        ext=splitext(path)
        if ext[1]=='':
            if path[-1]=='/':
                path+=deffile
            else:
                path+='/'+deffile
        ldir=dirname(path)
        if sep!='/':
            ldir=replace(ldir,'/',sep)
            path=replace(path,'/',sep)

        if not isdir(ldir):
            if exists(ldir):
                    #unlink(ldir)
                pass
            else:    
                makedirs(ldir)
        print path
        return path
            
    def download(self):
        """
        下载文件
        """
        try:
            retval=urlretrieve(self.url,self.file)
        except IOError:
            retval=('***ERROR :invalid URL "%s"' %self.url,)
        return retval   
    
    def parseAndGetLinks(self):
        """
        获取网页中的链接
        """
        #print 'Get Html Links from file:%s' % self.file
        #self.parser=HTMLParser(AbstractFormatter(DumbWriter(StringIO)))
        self.parser=HTMLParser(NullFormatter())
        #self.parser.feed(open(self.file).read())
        try:
            self.parser.feed(open(self.file).read())
            self.parser.close()
            return self.parser.anchorlist
        except:
            print self.file + " error !"
            return [] 

class Crawler(object):
    count=0
    def __init__(self,url):
        self.q=[url]
        self.seen=[]
        self.dom=urlparse(url)[1]
        
    def getPage(self,url):
        r=Retriever(url)
        retval=r.download()
        if retval[0]=='*':
            print retval,'...skipping parse'
            return 
        Crawler.count+=1
        print '/n(',Crawler.count,')'
        print 'URL:',url
        print 'FILE:',retval[0]
        self.seen.append(url)
        if url[-1] == '/':
            self.seen.append(url+"index.html")
            self.seen.append(url[:-1])
        
        links=r.parseAndGetLinks()
        for eachLink in links:
            #网址为目录
            if url[-1] == "/":
                if  eachLink[:2] != "./" and eachLink[:4] != "http" and eachLink[0] != "/":
                    continue
                else:
                    if  eachLink[:2] == "./":
                        eachLink = url + eachLink[2:]
                    elif eachLink[0] == "/":
                        #eachLink = url + eachLink[1:]
                        eachLink = "http://" + self.dom + eachLink
                    elif eachLink[:4] == "http":
                        pass
                    if eachLink not in self.seen:
                        #if find(eachLink,self.dom)==-1:
                        if url[:7] == "http://" or url[:7] == "http:\\":
                            tmp_url = url[7:]
                        if find(eachLink,tmp_url) == -1:
                            pass
                            #print '...discarded,not in domain'
                        else:
                            if eachLink not in self.q:
                                self.q.append(eachLink)
                                #print '...new ,added to  Q'
                            else:
                                pass
                                #print '...discarded,already in Q'
                    else:
                        print '...discarded,already  processed'

    def go(self):
        """
                            爬虫主程序
        """
        while True:
            if self.q:
                url=self.q.pop()
                self.getPage(url)
            else:
                break

def main(sitelist):

    for site in sitelist:
        print "-----------------------------------"
        print site
        if site.endswith("index.html"):
            site = site[0:-10]
        robot=Crawler(site)
        robot.go()
        print site," All file has download!"
if __name__=='__main__':
    hint = "教育与经济社会发展数据平台--区县数据采集系统 V1.0版  当前平台-"
    if platform.system() == "Windows":
            print hint.decode('utf-8').encode('gb2312','ignore'),
    else:
            print hint,
    print '' + platform.system()
    print '--------------------------------------------------------'

    
    #print hint
    sitelist = set()
    sitefile = open("Site.txt","r")
    if sitefile:
        sites = sitefile.readlines()
        for site in sites:
            if len(site.strip()) > 0:
                sitelist.add(site.strip())
        if len(sitelist) == 0:
            hint = "站点列表文件为空，请向Site.txt文件中添加要下载的网址"
            if platform.system() == "Windows":
                print hint.decode('utf-8').encode('gb2312','ignore')
            else:
                print hint
    else:
        hint = "Site.txt文件打开失败"
        if platform.system() == "Windows":
            print hint.decode('utf-8').encode('gb2312','ignore')
        else:
            print hint

    for site in sitelist:
        print site
    hint = "读入网站名成功，按任意键继续"
    if platform.system() == "Windows":
            print hint.decode('utf-8').encode('gb2312','ignore')
    else:
            print hint
    
    raw_input()
    main(sitelist)
    print "---------------------------------------"
    print "End!"
    raw_input()
                
                 
        
        
    
