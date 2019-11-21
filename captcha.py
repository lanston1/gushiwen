from PIL import Image
import tesserocr
import requests
import os
import re

'''
识别字母数字验证码
参数1：验证码本地保存路径
参数2：验证码图片地址
如果有识别的验证码有image_url，那么要先通过网址下载图片，需要传入的参数有：参数1和参数2
如果识别的验证码是已经下载保存在本地的图片，则不需下载图片，需要传入的参数有：参数1
:return: 
'''

class CracklmageCode():

    def __init__(self, image_path, image_url = None):
        # 图片下载链接
        self.image_url = image_url
        # 图片保存路径
        self.image_path = image_path
        self.times = 1

    def image_download(self):
        """
        图片下载
        """

        response = requests.get(self.image_url)
        with open(self.image_path, 'wb') as f:
            f.write(response.content)

    def get_image(self):
        """
        用Image获取图片文件
        :return: 图片文件
        """
        image = Image.open(self.image_path)
        return image

    def image_grayscale_deal(self, image):
        """
        图片转灰度处理
        :param image:图片文件
        :return: 转灰度处理后的图片文件
        """
        image = image.convert('L')
        #取消注释后可以看到处理后的图片效果
        # image.show()
        return image

    def image_thresholding_method(self, image, threshold = 160):
        """
        图片二值化处理
        :param image:转灰度处理后的图片文件
        :return: 二值化处理后的图片文件
        :threshold为二值化阈值
        """
        pixdata = image.load()
        w, h = image.size
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        # image.show()
        return image

        # 以下代码效果与上相同
        # table = []
        # for i in range(256):
        #     if i < threshold:
        #         table.append(0)
        #     else:
        #         table.append(1)
        # # 图片二值化，此处第二个参数为数字一
        # image = image.point(table, '1')
        # #取消注释后可以看到处理后的图片效果
        # image.show()
        # return image

    def image_depoint(self, image, threshold = 100):
        """传入二值化后的图片进行降噪
        去除干扰线，常见的4邻域、8邻域算法。所谓的X邻域算法，可以参考手机九宫格输入法，按键5为要判断的像素点，4邻域就是判断上下左右，8邻域就是判断周围8个像素点。如果这4或8个点中255的个数大于某个阈值则判断这个点为噪音，阈值可以根据实际情况修改。
        """
        pixdata = image.load()
        w,h = image.size
        for y in range(1,h-1):
            for x in range(1,w-1):
                count = 0
                if pixdata[x,y-1] > threshold:#上
                    count = count + 1
                if pixdata[x,y+1] > threshold:#下
                    count = count + 1
                if pixdata[x-1,y] > threshold:#左
                    count = count + 1
                if pixdata[x+1,y] > threshold:#右
                    count = count + 1
                if pixdata[x-1,y-1] > threshold:#左上
                    count = count + 1
                if pixdata[x-1,y+1] > threshold:#左下
                    count = count + 1
                if pixdata[x+1,y-1] > threshold:#右上
                    count = count + 1
                if pixdata[x+1,y+1] > threshold:#右下
                    count = count + 1
                if count > 5:
                    pixdata[x,y] = 255
        # image.show()
        return image



    def captcha_tesserocr_crack(self, image):
        """
        图像识别
        :param image: 二值化处理后的图片文件
        :text: 识别结果
        """
        tip = True
        text = ""

        try:
            text = tesserocr.image_to_text(image)
            text = text.rstrip()
            if text == "":            # 如果识别结果为空，则识别失败
                tip = False
                print(text)

            if re.search(r'[0-9a-zA-Z]{4}', text):
                pass
            else:
                tip = False           # 如果识别结果中出现了了字母数字之外的字符，则识别失败
            if len(text) != 4:
                tip = False           # 如果识别结果不足四位（因为有部分字符粘连的验证码），则识别失败

        except UnicodeDecodeError as e:
            tip = False                # 如果报字符编码错误，则识别失败，需要捕捉错误

        if tip == False:
            # 识别失败
            return None
        else:
            return text





    def run(self):
        '''
        如果有识别的验证码有image_url，那么先通过网址下载图片
        如果识别的验证码是已经下载保存在本地的图片，
        :return:
        '''
        if self.image_url:
            self.image_download()
            image = self.get_image()
            img1 = self.image_grayscale_deal(image)
            img2 = self.image_thresholding_method(img1)
            img3 = self.image_depoint(img2)
            text = self.captcha_tesserocr_crack(img3)

            # 如果识别失败，迭代、重新识别、调用验证码获取函数重新获取验证码
            if text != None:
                print("第{}次识别成功".format(self.times))
                return text
            else:
                print("第{}次识别失败".format(self.times))
                self.times += 1
                text = self.run()
                return text
        else:
            image = self.get_image()
            img1 = self.image_grayscale_deal(image)
            img2 = self.image_thresholding_method(img1)
            img3 = self.image_depoint(img2)
            text = self.captcha_tesserocr_crack(img3)

            # 如果识别失败，迭代、重新识别、调用验证码获取函数重新获取验证码
            if text != None:
                print("验证码识别成功")
                return text
            else:
                print("验证码识别失败")
                return None



if __name__ == '__main__':
    image_url = 'http://my.cnki.net/elibregister/CheckCode.aspx'
    image_path = '{0}/{1}.{2}'.format(os.getcwd(), 'verification_code', 'jpg')
    c = CracklmageCode(image_path, image_url)
    print(c.run())
