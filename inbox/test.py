import pprint
import sys
import os
# idea 引入自定义模块编译不通过，有红色的下划线，但是运行正常
# 解决办法：右键工程->open module settings->sdks->classpath->添加引入模块所在的路径
import searchTool
pprint.pprint(sys.path)  # 打印摸快搜索路径
# pprint.pprint(os.environ)  # 打印系统环境变量
# pprint.pprint(searchTool.find_files("E:\\java\\ideaWorkspace\\pythonTest\\tmp","简书"))
dect = {}
dect1 = {"a":1,"b":2,"c":3}
dect2 = {"d":4,"e":5,"f":6}
dect3 = {"g":7,"h":8,"i":9}
dect1.update(dect2)
dect1.update(dect3)
print(dect1);
dect_keys = dect1.keys()
for key in dect_keys:
    print("%s=%s"%(key,dect1.get(key)))
a = ""
b = "1"
a.join(b)
print("a=%s"%a)
print(30*50)
