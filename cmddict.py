#--coding:utf-8--
__author__ = "Kaiwen Sun"
__copyright__ = "Copyright 2016, cmddict"
__credits__ = ["Kaiwen Sun"]
__license__ = "GPL"
__version__ = "1.0.3"
__maintainer__ = "Kaiwen Sun"
__email__ = "myagent.receiver@gmail.com"

import sys
import urllib2
import json

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

key = "884563952"
word = ""
appname = "cmddict"

errCodes = {
	0:u"正常",
	20:u"要翻译的文本过长",
	30:u"无法进行有效的翻译",
	40:"不支持的语言类型",
	50:u"无效的key",
	60:u"无词典结果，仅在获取词典结果生效"
	}

keylist = [
		"keyfrom",
		"key",
		"type",
		"doctype",
		"version",
		"q"
		]

def display(word,dic):
	found = False
	errCode = dic["errorCode"]
	if errCode!=0:
		print errCodes[errCode]
		return
	if "translation" not in dic or (len(dic["translation"])==1 and dic["translation"][0]==word):
		pass
	else:
		for trans in dic["translation"]:
			print trans
			found = True

	if "basic" in dic and "explains" in dic["basic"]:
		for trans in dic["basic"]["explains"]:
			print trans
			found = True

	
	if "web" in dic and "key" in dic["web"] and "value" in dic["web"]:
		print dic["web"]["key"]
		for trans in dic["web"]["value"]:
			print trans
			found = True
	if not found:
		print u"没有找到翻译"

def lookup(word):
	if not is_ascii(word):
		print u"无法识别的英文"
		return
	if '&' in word and '=' in word and any(key in word for key in keylist):
		print u"危险的查询"
		return
	reply = urllib2.urlopen("http://fanyi.youdao.com/openapi.do?keyfrom="+appname+"&key="+key+"&type=data&doctype=json&version=1.1&q="+word).read()
	if type(reply) is str and reply=='no query':
		print u"无效的输入"
		return
	dic = json.loads(reply)
	display(word,dic)

def main():
	try:
		if len(sys.argv)>1:
			word = " ".join(sys.argv[1:])
			lookup(word)
		else:
			while True:
				try:
					line = raw_input('> ')
					if len(line)==0:
						continue
					lookup(line)
				except (EOFError,KeyboardInterrupt):
					break
				except:
					print u"你好，程序测试员！"
	except:
		print u"你好，程序测试员！"

if __name__ == "__main__":
	main()
