import base64
import json
import requests


class VeriCodeUtil:
    uname = "hahaha123"
    pwd = "lol123456"
    url = "http://api.ttshitu.com/base64"

    def base64_api(self,img):
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        data = {"username": self.uname, "password": self.pwd, "image": b64,"typeid": 7}
        result = json.loads(requests.post(self.url, json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]
        return ""

# if __name__ == "__main__":
#     img_path = "C:/Users/Administrator/Desktop/file.jpg"
#     result = base64_api(uname='你的账号', pwd='你的密码', img=img_path)
#     print(result)