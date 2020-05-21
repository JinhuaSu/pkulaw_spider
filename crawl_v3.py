#coding:utf-8
import socket
socket.setdefaulttimeout(60)
import requests
import urllib.request, urllib.error, urllib.parse
# import cchardet
import os,time
from lxml import etree
import threading
import re
import time
import random
from scrapy.selector import Selector

# filenames=os.listdir('.')
# count=0
# for fname in filenames:
# 	if fname.startswith('gid_log'):
# 		count+=1

# gid_path='gid_log_%d' %(count)

# 1、2步分开运行要注意gid_path
# gid_path='gid_log_12'

	    #"Cookie": "Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1528548975,1528552208,1528598726; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1528598726; Encoding=true; ASP.NET_SessionId=gm15xlzbzjszevk0m0q4w5u2; CookieId=gm15xlzbzjszevk0m0q4w5u2; CheckIPAuto=0; CheckIPDate=2018-06-10 10:45:28", 
def get_html(url,cookie1=True):  #得到网页源码
	headers = {
	    "Accept-Language": "zh-CN,zh;q=0.8", 
	    "Accept-Encoding": "gzip, deflate, sdch", 
	    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
	    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36", 
	    "Host": "www.pkulaw.cn", 
	    "Upgrade-Insecure-Requests": "1", 
	    "Cookie": "QINGCLOUDELB=f7fbfc03a670863f34b0656d2e114d6fec61ed2f1b6f7d61f04556fafeaf0c45; ASP.NET_SessionId=lsvtq1ivg0o0a1vpk5n2lujw; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1590032048; Hm_lvt_b196e3c9d71b8c7dfa4d1d668cee40f0=1590032048; Hm_lpvt_b196e3c9d71b8c7dfa4d1d668cee40f0=1590032048; CookieId=lsvtq1ivg0o0a1vpk5n2lujw; CheckIPAuto=; CheckIPDate=2020-05-21 11:34:08; FWinCookie=1; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1590032912; bdyh_record=1970324934084378%2C1970324934199982%2C1970324934087941%2C1970324934022197%2C1970324934179630%2C1970324934166496%2C1970324934180023%2C1970324933943538%2C1970324934173448%2C1970324934201674%2C1970324934109579%2C1970324934222876%2C1970324934139582%2C1970324934196247%2C1970324934198751%2C1970324934069496%2C1970324934180096%2C1970324934170348%2C1970324934202395%2C1970324933940967%2C; isCheck=ValidateSuccess_117; lsvtq1ivg0o0a1vpk5n2lujw=true", 
	    "Proxy-Connection": "keep-alive"
	}
	print(url)
	req=requests.get(url,headers=headers)
	if cookie1:
		html=req.text
		return html
	else:
		gid = url.split('&')[-2].split('=')[-1]
		headers = {
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", 
	 	"Accept-Encoding": "gzip, deflate", 
		"Accept": "text/html, */*; q=0.01", 
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", 
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
		"Content-Length": "81", 
		"Host": "www.pkulaw.cn", 
		"Origin": "http://www.pkulaw.cn", 
		"Referer": "http://www.pkulaw.cn/case/pfnl_%s.html?match=Exact" %gid, 
		"X-Requested-With": "XMLHttpRequest", 
		"Upgrade-Insecure-Requests": "1", 
		"Cookie": "QINGCLOUDELB=f7fbfc03a670863f34b0656d2e114d6fec61ed2f1b6f7d61f04556fafeaf0c45; ASP.NET_SessionId=lsvtq1ivg0o0a1vpk5n2lujw; Hm_lvt_b196e3c9d71b8c7dfa4d1d668cee40f0=1590032048; Hm_lpvt_b196e3c9d71b8c7dfa4d1d668cee40f0=1590032048; CookieId=lsvtq1ivg0o0a1vpk5n2lujw; FWinCookie=1; isCheck=ValidateSuccess_117; bdyh_record=1970324934210715%2C1970324934170434%2C1970324934178555%2C1970324934169154%2C1970324934186679%2C1970324934217544%2C1970324934173823%2C1970324934207074%2C1970324934110186%2C1970324934220235%2C1970324934202935%2C1970324934217455%2C1970324933944267%2C1970324934110241%2C1970324934213287%2C1970324934019819%2C1970324934103673%2C1970324934220206%2C1970324934074565%2C1970324934218634%2C; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1590041045", 
	 	"Proxy-Connection": "keep-alive"
		}
		req=requests.get(url,headers=headers)
		html=req.text
		print(html)
		print("http://www.pkulaw.cn/case/pfnl_%s.html?match=Exact"%gid)
		return html

def write2file(content,filename):  # 将爬取的文书写入文件保存
	try:
		f=open(filename,'w')
	except Exception as e:
		filename=filename.split('、')[0]+'_error_filename.txt'
		f=open(filename,'w')
	f.write(content)#.decode('utf-8')
	f.close()

 #下载ihref对应的文书
def load_one_wenshu(gid,title): 
	ex_href='http://www.pkulaw.cn/case/FullText/_getFulltext?library=pfnl&gid=#gid#&loginSucc=0'
	ex_href='http://www.pkulaw.cn/case/pfnl_#gid#.html?match=Exact'
	ex_href='http://www.pkulaw.cn/case/FullText/_getFulltext?library=pfnl&gid=#gid#&loginSucc=0'
	href=ex_href.replace('#gid#',gid)
	html=get_html(href,False)
	page=etree.HTML(html)
	#page=Selector(html)
	content=page.xpath('body')[0].xpath('string(.)').strip()
	#content='\n'.join(page.css('div#divFullText *::text').getall())
	write2file(content,filepath+os.sep+title+'.txt')

def load_one_page_wenshu(gid_list,titles):  # 多线程抓取多个href的文书
	# threads=[]   # 尝试多线程加速 失败 访问频繁 出现验证码 封ip
	# for i in range(len(gid_list)):
	# 	gid,title=gid_list[i],titles[i]
	# 	threads.append(threading.Thread(target=load_one_wenshu,args=(gid,title,)))
	# for t in threads:
	# 	t.start()
	# t.join()  # 阻塞

	for i in range(len(gid_list)):  # 顺序爬取 时间过长 一个月大概需要20~30h
		load_one_wenshu(gid_list[i],titles[i])
		# time.sleep(0.1)

# 保存案件标题和id至文件
def save_gids(pageIndex,gid_list,titles):
	fpath=gid_path
	if not os.path.exists(fpath):
		os.mkdir(fpath)
	f=open(fpath+os.sep+str(pageIndex)+'.txt','w')
	for i in range(len(gid_list)):
		f.write('%s\t%s\n' %(titles[i],gid_list[i]))#.encode('utf-8')
	f.close()

#得到一页上所有的文书名称和案件id并保存
def get_one_page_all_href(href,pageIndex):
	html=get_html(href.replace('#pageIndex#',str(pageIndex)))
	# time.sleep(random.random())
	page=etree.HTML(text=html)
	items=page.xpath('//dl[@class="contentList"]/dd/a')
	print(len(items))
	gid_list=[]
	titles=[]
	for item in items:
		ihref=item.attrib['href']
		# title=item.text.strip()
		title=item.xpath('string(.)').strip()
		# if u'、' in title:
		# 	title=title.split(u'、')[1]
		gid=re.findall(r'_(.*?).html',ihref)[0]
		if gid not in gid_list:
			gid_list.append(gid)
			titles.append(title)
	# print len(set(titles))
	print('page:%d has %d different case.' %(pageIndex,len(gid_list)))
	# load_one_page_wenshu(gid_list,titles)
	save_gids(pageIndex,gid_list,titles)

# 获取当前log文件的所有title和id
def get_titles_gids(filename):
	gid_list=[]
	titles=[]
	f=open(filename,'r')
	for line in f:
		pieces=line.strip().split('\t')
		title,gid=pieces[0],pieces[1]
		title=title.replace('?','')
		# print cchardet.detect(title)
		gid_list.append(gid)
		titles.append(title)#.decode('utf-8'))
	return gid_list,titles

def load_one_page_from_gid_log(filename):  # 从下载好的gid中开始下载文书
	gid_list,titles=get_titles_gids(filename)   # 得到 gid_list 和 titles
	f=open('href_error_log.txt','a')
	for i in range(len(gid_list)):
		#try:
		load_one_wenshu(gid_list[i],titles[i])
		print('%s-%d load success..' %(filename,i+1))
# 		except Exception as e:   # 若该项抓取出错 记录至error_log.txt
# 			print('%s-%d load failed...' %(filename,i+1),e)
# 			f.write('%s-%d:\t%s\t%s\n' %(filename,i+1,titles[i],gid_list[i])) #.decode('utf-8')
# 			f.flush()
# 			time.sleep(1)
	f.close()

#得到目标日期范围内的数据页数pageNum
def getPageNum(href):
	html=get_html(href.replace('#pageIndex#','0'))
	page=etree.HTML(html)
	pageNum=page.xpath('//*[@id="toppager"]/span/span[2]')
	if pageNum!=None:
		pageNum=int(pageNum[0].xpath('string(.)').strip())
	else:
		pageNum=50
	pageNum = 5
	print('pageNum:',pageNum)
	return pageNum

def main():
	# PageSize=1000&Pager.PageIndex=0   
	# Start"%3A"2016.09.24"%2C"End"%3A"2016.10.13"%7D
	# href为查询案例与裁判文书的 链接  可设置页大小 页码  起始结束日期
	href='http://www.pkulaw.cn/case/Search/Record?Menu=CASE\
		&IsFullTextSearch=False&MatchType=Exact&Keywords=\
		&OrderByIndex=0&GroupByIndex=0&ShowType=1\
		&ClassCodeKey=#classcode1#%2C%2C#classcode3#&OrderByIndex=0&GroupByIndex=0\
		&ShowType=0&ClassCodeKey=#classcode1#%2C%2C#classcode3#&Library=PFNL\
		&FilterItems.CourtGrade=&FilterItems.TrialStep=\
		&FilterItems.DocumentAttr=&FilterItems.TrialStepCount=\
		&FilterItems.LastInstanceDate=%7B"Start"%3A"#start_date#"%2C"End"%3A"#end_date#"%7D\
		&FilterItems.CriminalPunish=&FilterItems.SutraCase=\
		&FilterItems.CaseGistMark=&FilterItems.ForeignCase=&GroupIndex=\
		&GroupValue=&TitleKeywords=#keyword_title#&FullTextKeywords=#keyword_full#\
		&Pager.PageSize=1000&Pager.PageIndex=#pageIndex#&X-Requested-With=XMLHttpRequest'

	href='http://www.pkulaw.cn/case/Search/Record?Menu=CASE&IsFullTextSearch=False&MatchType=Exact&Keywords=&OrderByIndex=0&GroupByIndex=0&ShowType=1&ClassCodeKey=00202%2C%2C&OrderByIndex=0&GroupByIndex=0&ShowType=1&ClassCodeKey=00202%2C%2C&Library=PFNL&FilterItems.CourtGrade=&FilterItems.TrialStep=&FilterItems.DocumentAttr=&FilterItems.TrialStepCount=&FilterItems.LastInstanceDate=&FilterItems.CriminalPunish=&FilterItems.SutraCase=&FilterItems.CaseGistMark=&FilterItems.ForeignCase=&SubKeyword=%E5%9C%A8%E7%BB%93%E6%9E%9C%E7%9A%84%E6%A0%87%E9%A2%98%E4%B8%AD%E6%A3%80%E7%B4%A2&GroupIndex=&GroupValue=&TitleKeywords=&FullTextKeywords=&Pager.PageSize=20&Pager.PageIndex=228213&X-Requested-With=XMLHttpRequest'
	global filepath
	# filepath='2017-12_15-1_19'  # 日期修改 href中也要修改

	# filepath='2017_01_01-2017_09_01'

	print('input date info (eg:2017_01_01-2017_09_01):')
	filepath=input(">").strip()

	start_date,end_date=filepath.split('-')

	start_date=start_date.replace('_','.')
	end_date=end_date.replace('_','.')

	print('start_date:',start_date)
	print('end_date:',end_date)

	# classcode1='007'

	print('input classcode1(an you):(eg:007)')
	classcode1=input(">").strip()

	href=href.replace('#start_date#',start_date).replace('#end_date#',end_date).replace('#classcode1#',classcode1)

	print('input classcode3(fa yuan):(eg:01)')
	classcode3=input(">").strip()

	href=href.replace('#classcode3#',classcode3)

	# keyword=u'离婚'
	print('input keyword_title:')
	keyword_title=input('>').strip()#.decode('GB18030').strip()
	href=href.replace('#keyword_title#',keyword_title)
	
	# keyword=u'离婚'
	print('input keyword_full:')
	keyword_full=input('>').strip()#.decode('GB18030').strip()
	href=href.replace('#keyword_full#',keyword_full)

	# print href

	# filepath='tmp'

	filepath=filepath+'+'+classcode1+'+'+classcode3+'+'+keyword_title+'+'+keyword_full

	if not os.path.exists(filepath):
		os.mkdir(filepath)

	global gid_path
	gid_path=filepath+'_log'

	pageNum=getPageNum(href)  # 得到所有案件页数
	print(pageNum)
	
	
	# 第一步 下载hrefs 和 titles
	for i in range(pageNum):   # 页数要修改
		get_one_page_all_href(href,i)
	
	
	'''
	# t0=time.time()
	# threads=[]   # 多线程
	# for i in range(459):
	# 	threads.append(threading.Thread(target=get_one_page_all_href,args=(href,i,)))
	# for t in threads:
	# 	t.start()
	# t.join()
	# print 'load %s cost:%.2f' %(filepath,time.time()-t0)
	'''
	
	
	
	# 第二步 根据gid文件下载相应的文书
	for i in range(pageNum):
		f=open('page_error_log.txt','a')
# 		try:
		fname=gid_path+os.sep+str(i)+'.txt'
		load_one_page_from_gid_log(fname)  #从gid_log中取title和id 下载相关文书
		print('%s load success...' %(fname))
# 		except Exception as e:
# 			print('%s load failed...' %(fname),e)
# 			f.write('%s' %(fname))#.decode('utf-8')
# 			f.flush()
# 			time.sleep(10)  # 休眠10s
		f.close()
	
	

if __name__ == '__main__':
	main()