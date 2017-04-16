# 0x00 cheetah

Cheetah is a dictionary-based brute force password webshell tool, running as fast as a cheetah hunt for prey. 

Cheetah's working principle is that it can submit a large number of detection passwords based on different web services at once, blasting 
efficiency is thousands of times other common brute force password webshell tools.

# 0x01 features

* Fast speed.

* Support python 2.x and python 3.x

* Support to read large password dictionary file.

* Support to remove duplicate passwords of large password dictionary file.

* Support for automatic detection of web services.

* Support brute force batch webshell urls password.

* Support for automatic forgery request header.

* Currently support php, jsp, asp, aspx webshell.

# 0x02 parameter description

python cheetah.py -h

	_________________________________________________
	       ______              _____         ______
	__________  /_ _____ _____ __  /_______ ____  /_
	_  ___/__  __ \_  _ \_  _ \_  __/_  __ \ __  __ \
	/ /__  _  / / //  __//  __// /_  / /_/ / _  / / /
	\___/  / / /_/ \___/ \___/ \__/  \____/  / / /_/
	      /_/                               /_/
	
	a very fast webshell password violent crack tool.
	
	usage: cheetah1.py [-h] [-i] [-v] [-c] [-up] [-r] [-w] [-s] [-n] [-u] [-b]
	                   [-p [file [file ...]]]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -i, --info            show information of cheetah and exit
	  -v, --verbose         enable verbose output(default disabled)
	  -c, --clear           clear duplicate password(default disabled)
	  -up, --update         update cheetah
	  -r , --request        specify request method(default POST)
	  -w , --webshell       specify webshell type(default auto-detect)
	  -s , --server         specify web server name(default auto-detect)
	  -n , --number         specify the number of request parameters
	  -u , --url            specify the webshell url
	  -b , --url-file       specify batch webshell urls file
	  -p file [file ...]    specify possword file(default pwd.list)
	
	use examples:
	  python cheetah.py -u http://orz/orz.php
	  python cheetah.py -u http://orz/orz.jsp -r post -n 1000 -v
	  python cheetah.py -u http://orz/orz.asp -r get -c -p pwd.list
	  python cheetah.py -u http://orz/orz -w aspx -s iis -n 1000
	  python cheetah.py -b url.list -c -p pwd1.list pwd2.list -v

# 0x03 screenshot

![screenshot 1](https://raw.githubusercontent.com/sunnyelf/cheetah/master/screenshot/1.png)
![screenshot 2](https://raw.githubusercontent.com/sunnyelf/cheetah/master/screenshot/2.png)
![screenshot 3](https://raw.githubusercontent.com/sunnyelf/cheetah/master/screenshot/3.png)
![screenshot 4](https://raw.githubusercontent.com/sunnyelf/cheetah/master/screenshot/4.png)
