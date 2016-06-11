#--coding:utf-8--
__author__ = "Kaiwen Sun"
__copyright__ = "Copyright 2016, cmddict"
__credits__ = ["Kaiwen Sun"]
__license__ = "GPL"
__version__ = "3.0.1"
__maintainer__ = "Kaiwen Sun"
__email__ = "myagent.receiver@gmail.com"

import sys
import urllib2
import json
import locale
import re

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

key = "884563952"
word = ""
appname = "cmddict"
syscode = locale.getpreferredencoding()

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

phonDict = {
u'ʌ':u'Λ',	#c_u_p, l_u_ck
#u'ɑ':u'a',	#_a_rm, f_a_ther
u'æ':u'@',	#c_a_t, b_a_ck
u'ə':u'3',	#_a_way, cin_e_m_a_
u'ɜ':u'3',	#t_ur_n, l_ear_n
u'ɪ':u'i',	#h_i_t, s_i_tting
u'ɒ':u'o',	#h_o_t, r_o_ck
u'ɔ':u'o',	#c_a_ll, f_ou_r
u'ʊ':u'u',	#p_u_t, c_oul_d
u'ʳ':u'(r)',
u'ŋ':u'η',	#si_ng_, fi_n_ger
u'ʃ':u'∫',	#_sh_e, cra_sh_
#u'θ':u'th',	#_th_ink, bo_th_
u'ð':u'犭',	#_th_is, mo_th_er
u'ʒ':u'ろ',	#plea_s_ure, vi_si_on
u'\u02d0':u':'
}
#The ASCII Phonetic Alphabet is from http://www.antimoon.com/how/pronunc-ascii.htm
pattern = re.compile(r'\b(' + '|'.join(phonDict.keys()) + r')\b')

def convertPhonetic(phonetic):
	if sys.platform == "win32":
		l = list(phonetic)
		for i in xrange(len(l)):
			if l[i] in phonDict:
				l[i]=phonDict[l[i]]
		#rtn = pattern.sub(lambda x: phonDict[x.group()], phonetic)
		return ''.join(l)
	else:
		return phonetic
	

def display(word,dic):
	found = False
	errCode = dic["errorCode"]
	if errCode!=0:
		print errCodes[errCode]
		return
	if "translation" not in dic or (len(dic["translation"])==1 and dic["translation"][0]==word):
		pass
	elif "basic" not in dic or 'phonetic' not in dic['basic']:
		for trans in dic["translation"]:
			print trans
			found = True

	if "basic" in dic and "uk-phonetic" in dic["basic"]:
		if "basic" in dic and "uk-phonetic" in dic["basic"]:
			print '[',(convertPhonetic(dic["basic"]["uk-phonetic"])).encode(syscode,'replace'),']'
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
	if '&' in word and '=' in word and any(key in word for key in keylist):
		print u"危险的查询"
		return
	try:
		reply = urllib2.urlopen("http://fanyi.youdao.com/openapi.do?keyfrom="+appname+"&key="+key+"&type=data&doctype=json&version=1.1&q="+word).read()
	except:
		print u"请检查网络连接"
		return
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
					if line=='exit':
						break;
					if len(line)==0:
						continue
					line = urllib2.quote(line.decode(syscode,'replace').encode('utf8','replace'))
					lookup(line)
				except (EOFError,KeyboardInterrupt):
					break
				except:
					print u"你好啊，程序测试员！"
	except:
		print u"你好，程序测试员！"

if __name__ == "__main__":
	main()
