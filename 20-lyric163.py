#!/usr/bin/python3
# -*- coding: utf-8 -*-

#########################################################################
# File Name: 下载网易云匹配歌词
# Author: Jesse
# github: jesseconfig
# Created Time: 2021年07月05日 星期一 23时00分04秒
#########################################################################


import argparse,sys,os
import requests
import json

parser = argparse.ArgumentParser(description="Lyrics for 163.com  Download.")
parser.add_argument("artist", nargs="?", default="",help="Song artist")
parser.add_argument("title", nargs="?", default="", help="Song title")
args = parser.parse_args()
if args.artist == "":
  print ("Song artist missing")
  sys.exit(1)     

if args.title == "":
  args.title=args.artist
  #print ("Song title missing")
  #sys.exit(1)

print(args.artist)
print(args.title)


##
# 根据歌曲名称获取ID
##
#music_nm=input("请输入歌曲名称：")
music_nm=args.title + args.artist

print (music_nm)

url = "https://music.163.com/api/search/pc?s=" + music_nm + "&offset=0&limit=1&type=1"
payload={}
headers={"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
  "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language" : "en-us",
  "Connection" : "keep-alive",
  "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7"}
r = requests.request("GET", url, headers=headers, data=payload)
json_obj = r.text
j = json.loads(json_obj)#进行json解析ID name artists
p=j['result']['songs']
_as=p[0]['artists'][0]['name']
_sn=p[0]['name']
_id=p[0]['id']
music_id=str(_id)
urll = "http://music.163.com/api/song/lyric?"+ "id=" + music_id+ "&lv=1&kv=1&tv=-1"
r = requests.get(urll,headers=headers,allow_redirects=False)
json_obj = r.text
j = json.loads(json_obj)
#进行json解析输出
#print(j['lrc']['lyric'])

## 保存歌词
import codecs
lrc_nm="/home/pi/.lyrics/" + args.artist + " - " + args.title + ".lrc"

if os.path.exists(lrc_nm):
    print("文件已存在!")
else:
    file = codecs.open(lrc_nm, 'w', 'utf-8')
    file.write(j['lrc']['lyric'])
    file.close()
print("artists:",_as)
print("歌曲名称:",_sn)
print("歌曲ID:",_id)
print(j['lrc']['lyric'])

