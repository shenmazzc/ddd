# coding:utf-8

import nls

URL = "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN = "yourToken"  # 参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = "yourAppkey"  # 获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist


# 以下代码会根据音频文件内容反复进行实时语音识别（文件转写）
class St:
    def __init__(self):
        self.sr = None
        self.__slices = None
        self.__data = None
        self.filename = None

    def in_file(self, filename):
        self.filename = filename

    def __loadfile(self, filename):
        with open(filename, "rb") as f:
            self.__data = f.read()

    def start(self):
        self.__loadfile(self.filename)
        self.__run()

    def on_sentence_begin(self, message, *args):
        print("test_on_sentence_begin:{}".format(message))

    def on_sentence_end(self, message, *args):
        print("test_on_sentence_end:{}".format(message))

    def on_start(self, message, *args):
        print("test_on_start:{}".format(message))

    def on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def on_close(self, *args):
        print("on_close: args=>{}".format(args))

    def on_result_chg(self, message, *args):
        print("test_on_chg:{}".format(message))

    def on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))

    def __connect(self):
        self.sr = nls.NlsSpeechTranscriber(
            url=URL,
            token=TOKEN,
            appkey=APPKEY,
            on_sentence_begin=self.on_sentence_begin,
            on_sentence_end=self.on_sentence_end,
            on_start=self.on_start,
            on_result_changed=self.on_result_chg,
            on_completed=self.on_completed,
            on_error=self.on_error,
            on_close=self.on_close,
            callback_args=[]
        )

    def __start(self):
        self.sr.start(aformat="pcm",
                      enable_intermediate_result=True,
                      enable_punctuation_prediction=True,
                      enable_inverse_text_normalization=True)

    def __run(self):
        self.__connect()

        self.__start()

        self.__slices = zip(*(iter(self.__data),) * 640)

        for i in self.__slices:
            self.sr.send_audio(bytes(i))

    def ctrl(self, key: str, value: str):
        self.sr.ctrl(ex={key: value})

    def stop(self):
        self.sr.stop()


if __name__ == '__main__':
    pass
