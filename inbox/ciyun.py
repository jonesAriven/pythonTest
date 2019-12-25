import random
from collections import Counter

import jieba
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from sklearn.preprocessing import minmax_scale
from PIL import Image

# 灵感出自博客https://blog.csdn.net/cainiao_python/article/details/98697669
# 另有在制作线词云地址：http://yciyun.com/
# 中文正则表达式
pattern = re.compile(u"[\u4E00-\u9FA5]+")
# filePath = "C:\\Users\\hwx393213\\Desktop\\liupan WX498468_lwx498468.txt"
filePath = "E:\\java\\ideaWorkspace\\pythonTest\\hello.txt"
clearPath = "E:\\java\\ideaWorkspace\\pythonTest\\clear.txt"
# f = open(filePath, 'r',encoding='utf-8')
# print(f.read());
# 新建一个输入流，
# filePath是要读的文件名的全路径，注意：该路径中不能包含中文，并且文件是utf-8的编码
with open(filePath, 'r', encoding='utf-8') as f:
    #     print(f.read);
    # 匹配所有的中文字符
    data = re.findall(pattern, f.read())
    data = ''.join(data)
# print(data)
# 新建一个输出流，
# filePath是输出文件名的全路径，注意：该路径中不能包含中文，并且文件是utf-8的编码
with open(clearPath, 'w', encoding='utf-8') as f:
    f.write(data)


# data_path是需要读取的txt文件的全路径
# math_path 是遮罩图，注意，该文件必须是新建一个png类型的文件，如通过window的画图软件新建一个图片
# （否则可能会报 read past end of file或其他错误），不能是其他类型的文件在重命名为.png后缀的文件
def word_cloud(data_path, math_path):
    with open(data_path, "r", encoding='utf-8') as f:
        data_tmp = f.read()
    mask = plt.imread(math_path)
    cut_data = jieba.cut(data_tmp)
    str_cut_data = " ".join(cut_data)
    list_cut_data = str_cut_data.split(" ")
    '''
    font_path : string  #字体路径，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'
    width : int (default=400) #输出的画布宽度，默认为400像素
    height : int (default=200) #输出的画布高度，默认为200像素
    prefer_horizontal : float (default=0.90) #词语水平方向排版出现的频率，默认 0.9 （所以词语垂直方向排版出现频率为 0.1 ）
    mask : nd-array or None (default=None) #如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 		取代。除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。如：bg_pic = imread('读取一张图片.png')，背景图片的画布一定要设置为白色（#FFFFFF），然后显示的形状为不是白色的其他颜色。可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了。
    scale : float (default=1) #按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍
    min_font_size : int (default=4) #显示的最小的字体大小
    font_step : int (default=1) #字体步长，如果步长大于1，会加快运算但是可能导致结果出现较大的误差
    max_words : number (default=200) #要显示的词的最大个数
    stopwords : set of strings or None #设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS
    background_color : color value (default=”black”) #背景颜色，如background_color='white',背景颜色为白色
    max_font_size : int or None (default=None) #显示的最大的字体大小
    mode : string (default=”RGB”) #当参数为“RGBA”并且background_color不为空时，背景为透明
    relative_scaling : float (default=.5) #词频和字体大小的关联性
    color_func : callable, default=None #生成新颜色的函数，如果为空，则使用 self.color_func
    regexp : string or None (optional) #使用正则表达式分隔输入的文本
    collocations : bool, default=True #是否包括两个词的搭配
    colormap : string or matplotlib colormap, default=”viridis” #给每个单词随机分配颜色，若指定color_func，则忽略该方法
    random_state : int or None  #为每个单词返回一个PIL颜色
    fit_words(frequencies)  #根据词频生成词云
    generate(text)  #根据文本生成词云
    generate_from_frequencies(frequencies[, ...])   #根据词频生成词云
    generate_from_text(text)    #根据文本生成词云
    process_text(text)  #将长文本分词并去除屏蔽词（此处指英语，中文分词还是需要自己用别的库先行实现，使用上面的 fit_words(frequencies) ）
    recolor([random_state, color_func, colormap])   #对现有输出重新着色。重新上色会比重新生成整个词云快很多
    to_array()  #转化为 numpy array
    to_file(filename)   #输出到文件
    '''
    # mask=np.array(Image.open(math_path))
    # background_color='white', max_words=2000,repeat=True
    my_word_cloud = WordCloud(font_path="./simfang.ttf", mask=mask, background_color="yellow").generate(str_cut_data)
    plt.imshow(my_word_cloud)
    plt.axis("off")
    plt.show()


# 在线词云制作
def online_word_cloud(data_path, colors):
    with open(data_path, "r", encoding="utf-8") as f:
        data_tmp = f.read()
    cut_data = jieba.cut(data_tmp)
    str_cut_data = " ".join(cut_data)
    list_cut_date = str_cut_data.split(" ")
    a = Counter(list_cut_date).most_common(200)
    print(len(a))
    np_data = np.array([i[1] for i in a])
    transfer = minmax_scale(np_data, feature_range=(3, 9))
    transfer = np.around(transfer)
    for i, j in zip(a, transfer):
        b = "{} | {} | {} |1|是".format(int(j), i[0], random.choice(colors))
        print(b)


if __name__ == "__main__":
    word_cloud("E:\\java\\ideaWorkspace\\pythonTest\\tmp\\hello.txt", "E:\\java\\ideaWorkspace\\pythonTest\\sample.png")
    # online_word_cloud("E:\\java\\ideaWorkspace\\pythonTest\\tmp\\hello.txt",["red","pink"])
