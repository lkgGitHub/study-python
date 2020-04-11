import requests
import base64
import re
import json

url = "https://raw.githubusercontent.com/Alvin9999/pac2/master/ssconfig.txt"
url2 = "https://coding.net/u/Alvin9999/p/ip/git/raw/master/ssconfig.txt"

if __name__ == '__main__':
    for u in [url, url2]:
        response = requests.get(u)
        b = base64.b64decode(response.text)
        s = b.decode()
        server_pattern = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        server_port_pattern = re.compile(r"\"server_port\" : \d+")
        method_pattern = re.compile(r"\"method\" : \".+\"")
        password_pattern = re.compile(r"\"password\" : \".+\"")
        server = re.findall(server_pattern, s)
        server_port = re.findall(server_port_pattern, s)
        method = re.findall(method_pattern, s)
        password = re.findall(password_pattern, s)

        configs = []
        for i in range(len(server)):
            port = server_port[i][server_port[i].find(":") + 2:len(server_port[i])]
            method = method[i][method[i].find(":") + 3:len(method[i])-1]
            password = password[i][password[i].find(":") + 3:len(password[i])-1]
            config = {
                'server': server[i],
                'server_port': int(port),
                'password': password,
                'method': method,
                'plugin': '', 'plugin_opts': '', 'plugin_args': '', 'remarks': '', 'timeout': 5}
            configs.append(config)
            print("==="*10)
            print('server: {}\nport:{}\npassword:{}\nmethod:{}'.format(server[0], int(port), password, method))

    # content = ""
    # try:
    #     with open("./gui-config.json", 'rt') as g:
    #         j = json.loads(g.read())
    #         j['configs'] = configs
    #         content = json.dumps(j)
    # except:
    #     with open("./gui-back.json", 'rt') as g:
    #         j = json.loads(g.read())
    #         j['configs'] = configs
    #         content = json.dumps(j)
    # with open("./gui-config.json", 'wt') as g:
    #     g.write(content)




