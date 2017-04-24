![cheetah logo](images/logo.jpg)

[English description](README.md) | [中文说明](README_zh.md)

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/) 
[![Build Status](https://travis-ci.org/sunnyelf/cheetah.svg?branch=master)](https://travis-ci.org/sunnyelf/cheetah)
[![Code Climate](https://codeclimate.com/github/sunnyelf/cheetah/badges/gpa.svg)](https://codeclimate.com/github/sunnyelf/cheetah)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cheetah-community/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/sunnyelf)

# 0x00 介绍 #
Cheetah是一款基于字典的webshell密码爆破工具，Cheetah的工作原理是能根据自动探测出的web服务设置相关参数一次性提交大量的探测密码进行爆破，爆破效率是其他普通webshell密码暴力破解工具上千倍。

项目地址：[https://github.com/sunnyelf/cheetah](https://github.com/sunnyelf/cheetah)

# 0x01 特点 #

- 速度极快
- 支持批量爆破
- 自动伪造请求
- 自动探测web服务设置相关参数
- 支持读取和去重超大密码字典文件
- 支持python 2.x和3.x
- 目前支持php、jsp、asp、aspx webshell

# 0x02 参数说明 #


	_________________________________________________
	       ______              _____         ______
	__________  /_ _____ _____ __  /_______ ____  /_
	_  ___/__  __ \_  _ \_  _ \_  __/_  __ \ __  __ \
	/ /__  _  / / //  __//  __// /_  / /_/ / _  / / /
	\___/  / / /_/ \___/ \___/ \__/  \____/  / / /_/
	      /_/                               /_/
	
	a very fast brute force webshell password tool.
	
	usage: cheetah.py [-h] [-i] [-v] [-c] [-up] [-r] [-w] [-s] [-n] [-u] [-b]
	                   [-p [file [file ...]]]
	
	可选参数:
	  -h, --help            显示帮助信息并退出
	  -i, --info            显示程序信息并退出
	  -v, --verbose         启用详细输出模式(默认禁用)
	  -c, --clear           去重字典文件(默认禁用)
	  -up, --update         更新cheetah
	  -r , --request        指定请求方式(默认POST方式)
	  -t , --time           指定请求间隔时间(默认0秒)
	  -w , --webshell       指定webshell类型(默认自动探测)
	  -s , --server         指定web服务器名称(默认自动探测)
	  -n , --number         指定一次请求参数数量(默认自动设置)
	  -u , --url            指定webshell url地址
	  -b , --url-file       指定批量webshell urls文件
	  -p   file [file ...]  指定多个字典文件(默认使用data/pwd.list)
	
	使用示例:
	  python cheetah.py -u http://orz/orz.php
	  python cheetah.py -u http://orz/orz.jsp -r post -n 1000 -v
	  python cheetah.py -u http://orz/orz.asp -r get -c -p pwd.list
	  python cheetah.py -u http://orz/orz -w aspx -s apache -n 1000
	  python cheetah.py -b url.list -c -p pwd1.list pwd2.list -v

# 0x03 下载使用 #

	git clone https://github.com/sunnyelf/cheetah.git
	python cheetah.py 

# 0x04 文件说明 #

	cheetah:
	│  .codeclimate.yml
	│  .gitignore
	│  .travis.yml
	│  cheetah.py             主程序
	│  LICENSE
	│  README.md
	│  README_zh.md
	│  update.py              更新模块
	│
	├─data
	│      big_shell_pwd.7z   高效shell大字典
	│      pwd.list           默认指定字典文件
	│      url.list           默认指定批量webshell url文件
	│      user-agent.list    用户代理文件
	│
	└─images
	        1.png
	        2.png
	        3.png
	        4.png
	        logo.jpg

# 0x05 截图 #

## Ubuntu
![screenshot 4](images/4.png)

## Windows
![screenshot 1](images/1.png)
![screenshot 2](images/2.png)
![screenshot 3](images/3.png)

# 0x06 问题 #

如果在使用过程中出现了bug欢迎提交[issues](https://github.com/sunnyelf/cheetah/issues)，我会及时回复并修复。

# 0x07 参考 #

[让你的一句话爆破速度提升千倍](https://www.t00ls.net/articles-36985.html)

[一种有效的Web指纹识别方法](http://journal.ucas.ac.cn/CN/abstract/abstract12402.shtml)

[识别Web服务器 (OTG-INFO-002)](https://kennel209.gitbooks.io/owasp-testing-guide-v4/content/zh/web_application_security_testing/fingerprint_web_server_otg-info-002.html)

[python读GB级大文件](https://github.com/Shuang0420/Shuang0420.github.io/wiki/python%E8%AF%BBGB%E7%BA%A7%E5%A4%A7%E6%96%87%E4%BB%B6)
