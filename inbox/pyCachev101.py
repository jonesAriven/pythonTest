'''
Created on 2019年12月24日

@author: hWX393213
'''
import os
import datetime


class SearchCache(object):
    '''
    classdocs
    '''
    cachemap = {}
    cachePath = ""
    cacheFile = ""

    def __init__(self):
        '''
        Constructor
        '''
        start_time = datetime.datetime.now()
        self.cachePath = "E:/pySearchCache"
        self.cacheFile = "E:/pySearchCache/st_mtime_cache_file"
        if not os.path.exists(self.cachePath):
            os.makedirs(self.cachePath)
        if not os.path.exists(self.cacheFile):
            open(self.cacheFile, "w+", encoding="utf-8").close()
        data_dict = {}
        # 读取缓存文件
        # file格式为  原路径文件名:[文件时间戳,缓存文件路径],原路径文件名:[文件时间戳,缓存文件路径],原路径文件名:[文件时间戳,缓存文件路径],

        with open(self.cacheFile, "r", encoding="utf-8") as f:
            data = f.read();
            data_list = data.split(",")
            if data_list and len(data_list) >= 1:
                for data_map in data_list:
                    if data_map:
                        # print(data_map.split("==>"))
                        data_dict.update({data_map.split("==>")[0]: data_map.split("==>")[1]})
        self.cachemap = data_dict
        end_time = datetime.datetime.now()
        # print("(end_time - start_time).seconds=", (end_time - start_time).seconds)

    def get_pyCache(self, filename):
        return self.cachemap.get(filename)

    def get_cachePath(self):
        return self.cachePath

    def get_cachemap(self):
        return self.cachemap

    def get_cacheFile(self):
        return self.cacheFile

    # 对象销毁调用方法,将map序列化到缓存文件中  
    def __del__(self):
        tmp_map = self.get_cachemap()
        map_keys = tmp_map.keys()
        with open(self.get_cacheFile(), "w", encoding="utf-8") as f:
            i = 0
            # each_line = ""
            for each in map_keys:
                f.writelines(str(each) + "==>" + str(tmp_map.get(each))+",")
                # write_flag = True
            #     each_line = each_line + str(each) + "==>" + str(tmp_map.get(each))+","
            #     if i % 2 == 0:
            #         f.writelines(each_line+"\r\n")
            #         each_line = ""
            #     i += 1
            # if not each_line:
            #     f.writelines(each_line)
            f.close()
