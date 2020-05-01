from datetime import date
import requests
import json
from base64 import b64decode as decode,b64encode as encode
from colorama import init,Fore

init(autoreset=True)


class noted:
    def __init__(self):
        self.settings = self.getSettings()
        self.link = 'https://api.github.com/repos/'+self.settings['GITHUB_USERNAME']+'/noted/contents/assets/noted/source.json'
        self.today = self.getDateToday()
        self.sha,self.content = self.parseJson()

    def getSettings(self):
        with open('config.json','r') as files:
            return json.loads(''.join(files.readlines()))

    def getJson(self):
        req = requests.get(self.link)
        return req.json()

    def parseJson(self):
        jsonData = self.getJson()
        sha,content = jsonData["sha"],json.loads(decode(jsonData["content"]).decode())
        return [sha,content]

    def getDateToday(self):
        today = date.today().strftime("%Y-%m-%d");
        return today

    def getInputuser(self):
        user_input = []
        print(Fore.BLUE+"[*] Jika sudah tekan CTRL+D untuk mengirim .")
        while True:
            try:
                line = input()
            except EOFError:
                break
            user_input.append(line)
        return '\n'.join(user_input)

    def prepareUpdate(self,user_input):
        self.content.append({
            "date": self.today,
            "post": user_input
        })
        payloads = {
            "path": "assets/noted/source.json",
            "message": "Update "+self.today,
            "content": encode(json.dumps(self.content).encode()).decode()+"\n",
            "branch": "master",
            "sha": self.sha
        }
        headers = {
            "Authorization": "token "+self.settings['SECRET_TOKEN']
        }
        return [payloads,headers]

    def question2Continue(self,headers,payloads):
        confirm = input(Fore.YELLOW+'[?] Apakah Anda Yakin [y/n] ? ')
        if confirm.lower() == "y":
            res = requests.put(self.link,headers=headers,json=payloads)
            res = res.json()
            if res['content']:
                print(Fore.GREEN+"[+] Berhasil meng-update note.")
        else:
            print(Fore.RED+"[+] exiting ....")
            exit()

    def main(self):
        inputUser = self.getInputuser()
        payloads,headers = self.prepareUpdate(inputUser)
        self.question2Continue(headers,payloads)

noted().main()


