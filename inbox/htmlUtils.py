import os
import sys
from selenium import webdriver
import webbrowser
import pprint
import time


class HtmlUtils():

    def __init__(self):
        pass

    # 创建html文件
    # message，需要写的html内容，file_path生成的html文件全路径，若不传，将会在电气文件的同级路径下生成名为helloworld.html的文件
    def create_html(self, message, file_path="./helloworld.html"):
        f = open(file_path, 'w', encoding="utf-8")
        # message = """<html>
        # <head></head>
        # <body><p>Hello World!</p></body>
        # </html>"""
        f.write(message)
        f.close()

    # 使用webdriver api 打开html文件
    # 注意，使用from selenium import webdriver时，需要依次有以下操作
    # 1、下载安装selenium包： 在终端执行 pip install selenium -i https://pypi.douban.com/simple
    # 2、想要使用webdriver操作哪个浏览器，就需要下载哪个浏览器的驱动包，并且该驱动包与浏览器的版本要兼容，对应的有官网下载地址，由于官网比较慢，这里提供阿里的下载地址，驱动包下载地址如下：
    # -我的google版本是“版本 79.0.3945.88（正式版本） （64 位）” ，我下载的google驱动包：http://npm.taobao.org/mirrors/chromedriver/79.0.3945.36/chromedriver_win32.zip，百度云链接地址：https://pan.baidu.com/s/1U6R8SCYpBYw1ZQy5A8_rGA
    # -我的火狐版本是 “71.0 (64 位)”，我下载的火狐驱动包：http://npm.taobao.org/mirrors/geckodriver/v0.7.1/wires-v0.7.1-win32.zip,百度云链接地址：https://pan.baidu.com/s/1FI6DFlKgWvRtNRQ9-cLL0A
    # 3、将以上下载的驱动包依次添加到对应浏览器的根目录，python的根目录，
    # 4、将对应浏览器的根目录添加到系统环境变量
    # 5、将对应的浏览器设置为默认浏览器
    # 6、重启对应的浏览器或者重启电脑
    # 　若没有以上操作，程序执行时会出现错误： selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
    def open_browser_by_webdriver(self, url_path):

        driver = webdriver.Chrome()
        # 这里可能会出现及时你用的是火狐的驱动，打开的也是谷歌的浏览器，那是因为系统设置的默认浏览是谷歌浏览去，需要更改默认浏览器
        # driver = webdriver.Firefox()
        driver.get("http:\\www.baidu.com")
        # time.sleep(5)
        # driver.close()
        # driver.quit()

    # 使用webbrowser api打开浏览器
    # webbrowser.open(url, new=0, autoraise=True)
    def open_browser_by_webbrowser(self, url_path):
        # 该方法是使用系统默认浏览器打开，也可以使用指定浏览器打开
        webbrowser.open(url_path)


if __name__ == "__main__":
    htmlUtils = HtmlUtils()
    # pprint.pprint(os.environ)
    # windows 下开发注意路径，将路径中所有的“\”替换成“\\”或者“/”，但是为了把代码迁移到linux上能正常运行， 改成“/”比较合适
    # htmlUtils.create_html("你好")
    htmlUtils.open_browser_by_webdriver("E:/java/ideaWorkspace/pythonTest/inbox/helloworld.html")
