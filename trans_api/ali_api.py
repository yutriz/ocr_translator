from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models


class ali_translator():
    def __init__(self, key_id='', key_id_secret='', from_lang='ja', to_lang='zh'):
        self.access_key_id = key_id
        self.access_key_secret = key_id_secret
        self.from_lang = from_lang
        self.to_lang = to_lang

    def create_client(self,
        access_key_id: str,
        access_key_secret: str,
    ) -> alimt20181012Client:
        config = open_api_models.Config(
            access_key_id = access_key_id,
            access_key_secret = access_key_secret
        )
        config.endpoint = f'mt.cn-hangzhou.aliyuncs.com'
        return alimt20181012Client(config)
    def query(self, text, write_log=False,
              log_file='D:\.ali_trans_log.txt'):
        client = self.create_client(self.access_key_id, self.access_key_secret)
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            format_type = 'text',
            source_language = self.from_lang,
            target_language = self.to_lang,
            source_text = text,
            scene = 'general'
        )
        runtime = util_models.RuntimeOptions()
        resp = client.translate_general_with_options(translate_general_request, runtime)
        translation = resp.body.data.__dict__['translated']

        src_and_dst = []
        text = text.splitlines()
        translation = translation.splitlines()
        for index in range(0, len(text)):
            src_and_dst.append("src: " + text[index] + "\n" + \
                               "dst: " + translation[index])


        if write_log:
            with open(log_file, 'a') as f:
                f.write("\n".join(src_and_dst))
                f.close
        
        return src_and_dst


