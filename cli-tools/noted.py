from datetime import date
import requests
import json
from base64 import b64decode as decode,b64encode as encode
from colorama import init,Fore

settings = []
init(autoreset=True)

with open('config.json','r') as files:
    settings = json.loads(''.join(files.readlines()))

def getJson():
    req = requests.get('https://api.github.com/repos/defrindr/noted/contents/noted/__noted.json')
    return req.json()

jsonData = getJson()

sha = jsonData["sha"]
content = json.loads(decode(jsonData["content"]).decode())

today = date.today()
today = today.strftime("%Y-%m-%d");

newPost = []
print(Fore.BLUE+"[*] Jika sudah tekan CTRL+D untuk mengirim .")

while True:
    try:
        line = input()
    except EOFError:
        break
    newPost.append(line)

newPost = '\n'.join(newPost);
content.append({
    "date": today,
    "post": newPost
})

payloads = {
    "path": "noted/__noted.json",
    "message": "Update "+today,
    "content": encode(json.dumps(content).encode()).decode()+"\n",
    "branch": "master",
    "sha": sha
}

headers = {
    "Authorization": "token "+settings['SECRET_TOKEN']
}

confirm = input(Fore.YELLOW+'[?] Apakah Anda Yakin [y/n] ? ')

if confirm.lower() == "y":
    res = requests.put('https://api.github.com/repos/'+settings['GITHUB_USERNAME']+'/noted/contents/noted/__noted.json',headers=headers,json=payloads)
    res = res.json()
    if res['content']:
        print(Fore.GREEN+"[+] Berhasil meng-update note.")
else:
    print(Fore.RED+"[+] exiting ....")
    exit()

