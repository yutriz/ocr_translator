import requests
import random
import json
from hashlib import md5


class bd_translator():
    def __init__(self, from_lang='jp', to_lang='zh', \
                 # Set your own appid/appkey.
                bd_appid = 'appid', \
                bd_appkey = 'appkey'
                ):
        
        self.appid = bd_appid
        self.appkey = bd_appkey 

        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        self.from_lang = from_lang
        self.to_lang = to_lang

        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path

    # Generate salt and sign
    def make_md5(self, text, encoding='utf-8'):
        return md5(text.encode(encoding)).hexdigest()
    
    def query(self, query_text, write_log=False, 
              log_file='D:\.bd_trans_log.txt'):
        """
        output: list
        """
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appid + query_text + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query_text, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        src_and_dst = []
        for result_line in result['trans_result']:
            content = "src: " + result_line['src'] + "\n" \
                        + "dst: " + result_line['dst']
            src_and_dst.append(content)

        if write_log :
            with open(log_file, 'a') as f:
                f.write("\n".join(src_and_dst))
                f.close

        # restore response
        # print(json.dumps(result, indent=4, ensure_ascii=False))
        return src_and_dst
