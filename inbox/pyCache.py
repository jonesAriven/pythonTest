'''
Created on 2019年12月24日
@author: hWX393213
'''
import os
import datetime
import threading
import traceback
import pythoncom
from win32com import client as wc
import shutil
import time
import shutil
import pymysql
import cusMysqlUtils


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
        self.lock = threading.Lock()
        self.cachePath = "E:/pySearchCache"
        self.cacheFile = "E:/pySearchCache/st_mtime_cache_file"
        # 缓存类型，是缓存到db还是缓存到文件,DB：缓存到DB，FILE:缓存到文件
        self._chcheType = "DB"
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

    @property
    def chcheType(self):
        return self._chcheType

    @chcheType.name
    def chcheType(self, chcheType):
        self._chcheType = chcheType

    def get_pyCache(self, filename):
        self.lock.acquire()
        try:
            return self.cachemap.get(filename)
        except:
            pass
        finally:
            self.lock.release()

    def get_cachePath(self):
        self.lock.acquire()
        try:
            return self.cachePath
        except:
            pass
        finally:
            self.lock.release()

    def get_cachemap(self):
        self.lock.acquire()
        try:
            return self.cachemap
        except:
            pass
        finally:
            self.lock.release()

    def get_cacheFile(self):
        self.lock.acquire()
        try:
            return self.cacheFile
        except:
            pass
        finally:
            self.lock.release()

    def update_chche(self, filename, action):
        self.lock.acquire()
        try:
            '''
            1: "Created",
            2: "Deleted",
            3: "Updated",
            4: "Renamed from something",
            5: "Renamed to something"
            '''
            if os.path.splitext(filename)[1] == ".doc":
                #                 time.sleep(5)
                #                 self.deal_doc(filename, action)
                self.trancefer_doc(filename, action)

        except:
            pass
        finally:
            self.lock.release()

    # 这份方法为word转docx的标准方法，一步都不不能錯
    def change_doc_to_docx(self, filename):
        doc = None
        cache_docx_full_name = ""
        wordApplication = None
        try:
            pythoncom.CoInitialize()
            wordApplication = wc.DispatchEx('Word.Application')
            filename = filename.replace("\\", "/")
            # 复制到缓存路径下的doc全文件名
            cache_doc_full_name = self.cachePath + "/" + os.path.split(filename)[1]
            if os.path.exists(cache_doc_full_name):
                os.remove(cache_doc_full_name)
            # 为避免在原文件已经打开的情况下操作它， 将原文件复制一份出来，放到缓存目录下
            shutil.copy(filename, self.cachePath)
            # 打开缓存路径下的doc文件
            if cache_doc_full_name.find(" ") != -1: # 如果文件路径中保护空格， wordApplication.Documents.Open将无法处理，这里处理一下空格
                shutil.move(cache_doc_full_name,cache_doc_full_name.replace(" ","_"))
                doc = wordApplication.Documents.Open(cache_doc_full_name)
            # 将缓存路径的doc文件转为docx文件,缓存路径下的docx全路径名
            docx_filename = filename.replace(":", "_").replace("/", "_").replace("\\", "_").replace(".doc", ".docx")
            cache_docx_full_name = self.cachePath + "/" + docx_filename
            if os.path.exists(cache_docx_full_name):
                os.remove(cache_docx_full_name)
            if cache_doc_full_name.find(" ") != -1:
                cache_docx_full_name = cache_docx_full_name.replace(" ","_")
            # save时不能创建目录，所以此处得保证docx_filename 的文件名正确，不能出现让程序生成目录，否则会跑异常
            doc.SaveAs(cache_docx_full_name, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
            # 转换成功后将缓存路径下的doc文件删除
            if os.path.exists(cache_doc_full_name):
                os.remove(cache_doc_full_name)
        except:
            traceback.print_exc()
            pass
        finally:
            if doc:
                try:
                    doc.Close()
                    if wordApplication:
                        wordApplication.Quit()
                except:
                    traceback.print_exc()
                    pass
        # print("cache_docx_full_name=", cache_docx_full_name)
        return cache_docx_full_name

    def trancefer_doc(self, filename, action):
        docx_filename = filename.replace(":", "_").replace("/", "_").replace("\\", "_").replace(".doc", ".docx")
        cache_docx_full_name = self.cachePath + "/" + docx_filename
        if str(action) == "1" or str(action) == "3" or str(action) == "4" or str(
                action) == "5":  # 新增或更新操作：新增或更新缓存路径下的，更新dict
            self.change_doc_to_docx(filename)
            self.cachemap.update({filename: str(os.stat(filename).st_mtime) + "@" + cache_docx_full_name})
        elif str(action) == "2":  # 删除docx文档，更dict
            if os.path.exists(cache_docx_full_name):
                os.remove(cache_docx_full_name)
            del self.cachemap[filename]
        self.persistence_cachemap()

    # 处理doc缓存保含两步，处理缓存路径下的docx文档，同时更新缓存的dict
    def deal_doc(self, filename, action):
        doc = None
        wordApplication = None
        try:
            # pythoncom.CoInitialize() 和 wc.DispatchEx('Word.Application') 顺序别搞反了，pythoncom.CoInitialize()一定要在之前
            pythoncom.CoInitialize()
            wordApplication = wc.DispatchEx('Word.Application')
            filename = filename.replace("\\", "/")
            docx_filename = filename.replace("doc", "docx")
            docx_filename = self.cachePath + "/" + ((os.path.split(docx_filename)[0]).replace("\\", "_")).replace("/",
                                                                                                                  "_").replace(
                ":", "_") + "_" + os.path.split(docx_filename)[1]  # 拼接缓存路径
            if str(action) == "1" or str(action) == "3" or str(action) == "4" or str(
                    action) == "5":  # 新增或更新操作：新增或更新缓存路径下的，更新dict
                if os.path.exists(filename) and os.path.isfile(filename):
                    shutil.copy(filename, self.cachePath)  # 为避免在原doc文档上打卡，操作，造成不必要的异常，这里将原文档复制一份出来
                    #  打开原doc文件，注意，这里一定不能出问题，如果打开失败，该出可能会会多次尝试打开
                    doc = wordApplication.Documents.Open(
                        self.cachePath + "/" + os.path.split(filename)[1])  # 生成的docx文件放到缓存路径下
                    if os.path.exists(docx_filename):
                        os.remove(docx_filename)
                    # save时不能创建目录，所以此处得保证docx_filename 的文件名正确，不能出现让程序生成目录，否则会跑异常
                    doc.SaveAs(docx_filename, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
                self.cachemap.update({filename: str(os.stat(filename).st_mtime) + "@" + docx_filename})
            elif str(action) == "2":  # 删除docx文档，更dict
                if os.path.exists(docx_filename):
                    os.remove(docx_filename)
                del self.cachemap[filename]
            self.persistence_cachemap()
        except:
            # traceback.print_exc()
            pass
        finally:
            if doc:
                try:
                    doc.Close()
                    if wordApplication:
                        wordApplication.Quit()
                except:
                    # traceback.print_exc()
                    pass

    # 将cachemap 刷到磁盘中
    def persistence_cachemap(self):
        try:
            tmp_map = self.cachemap
            map_keys = tmp_map.keys()
            with open(self.cacheFile, "w", encoding="utf-8") as f:  # 类内部嗲用自己的方法不调用自己的同步方法，否则容易产生死锁
                for each in map_keys:
                    f.writelines(str(each) + "==>" + str(tmp_map.get(each)) + ",")
                f.close()
        except:
            traceback.print_exc()
            pass
        finally:
            pass

    # 将指定路径的下的所有文件全路径读入数据库
    def flushFilePathintoDb(self, root_dir):
        """process all files in directory"""
        process_list = []
        try:
            cur_dir = os.path.abspath(root_dir)
            file_list = os.listdir(cur_dir)

            for file in file_list:
                fullfile = cur_dir + "\\" + file
                if os.path.isfile(fullfile):
                    process_list.append(fullfile)
                    if len(process_list) > 10000:
                        self.createCacheDb(process_list)
                        process_list = []
                elif os.path.isdir(fullfile):
                    dir_extra_list = self.get_process_files(fullfile)
                    if len(dir_extra_list) != 0:
                        for x in dir_extra_list:
                            process_list.append(x)
                            if len(process_list) > 10000:
                                self.createCacheDb(process_list)
                                process_list = []
        except:
            pass
        return process_list

    # 写入数据库
    def createCacheDb(self, process_list):
        db = cusMysqlUtils.MysqlUtils().db
        cursor = db.cursor()
        try:
            for each in process_list:
                try:
                    if os.path.splitext(each)[1] != ".tmp" and each.find("~$") == -1:
                        cursor.execute(
                            "insert into t_window_explore_file(full_fileName,current_st_mtime,updateTime) values (%s,%s,%s)",
                            (pymysql.escape_string(each.replace("\\", "/")), os.stat(each).st_mtime,
                             datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
                        # 提交到数据库执行
                        db.commit()
                except:
                    # 如果发生错误则回滚
                    db.rollback()
        except:
            pass
        finally:
            cursor.close()
            db.close()

    # updateCacheDb
    '''
        operate_type = args[0] # Moved Created Deleted Modified ,这里的moved指的是重命名，而不是移动
        file_type = args[1] # file directory
        src_name = args[2] # file or directory name
        des_src_name = ""
        if len(args) > 3:
            des_src_name = args[3] # 只有moved的情况下才存在该参数
        if operate_type == "Moved":
            # 重命名的情况下，文件的时间戳不会变化，所以可以根据时间戳更新数据库
    '''

    # 通过操作mysql 存过程，更新缓存
    def updateCacheDbByProc(self, *args):
        operate_type = args[0]  # Moved Created Deleted Modified ,这里的moved指的是重命名，而不是移动
        file_type = args[1]  # file directory
        src_name = args[2]  # file or directory name
        current_st_mtime = ""
        des_src_name = ""
        if len(args) > 3:
            des_src_name = args[3]  # 只有moved的情况下才存在该参数
            if os.path.isfile(des_src_name) or os.path.isdir(des_src_name):
                current_st_mtime = os.stat(des_src_name).st_atime
        else:
            if os.path.isfile(des_src_name) or os.path.isdir(des_src_name):
                current_st_mtime = os.stat(src_name).st_atime

        db = cusMysqlUtils.MysqlUtils().db
        cusor = db.cursor()
        try:
            cusor.callproc("p_window_explore_log", (operate_type, file_type, src_name, des_src_name, current_st_mtime))
            print(1111)
        except:
            db.rollback()
            traceback.print_exc()
        finally:
            cusor.close()
            db.close()

    # 直接通过sql语句操作数据库，更新缓存
    def updateCacheDb(self, *args):
        operate_type = args[0]  # Moved Created Deleted Modified ,这里的moved指的是重命名，而不是移动
        file_type = args[1]  # file directory
        src_name = args[2]  # file or directory name
        des_src_name = ""
        if len(args) > 3:
            des_src_name = args[3]  # 只有moved的情况下才存在该参数
        db = cusMysqlUtils.MysqlUtils().db
        cursor = db.cursor()
        try:
            if file_type == "file":
                if len(args) == 4:
                    if operate_type == "Moved":
                        cursor.execute(
                            "update t_window_explore_file set full_fileName = %s,updateTime = %s where current_st_mtime = %s",
                            ([pymysql.escape_string(des_src_name), datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                              os.stat(des_src_name).st_atime]))
                elif len(args) == 3:
                    if operate_type == "Created":
                        cursor.execute(
                            "insert into t_window_explore_file(full_fileName,current_st_mtime,updateTime) values (%s,%s,%s)",
                            ([pymysql.escape_string(src_name), os.stat(src_name).st_atime,
                              datetime.datetime.now().strftime("%Y%m%d%H%M%S")]))
                    elif operate_type == "Deleted":
                        cursor.execute("delete from t_window_explore_file where full_fileName = %s",
                                       pymysql.escape_string(src_name))
                    elif operate_type == "Modified":
                        cursor.execute(
                            "update t_window_explore_file set current_st_mtime = %s, updateTime = %s where full_fileName = %s",
                            ([os.stat(src_name).st_atime, datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                              pymysql.escape_string(src_name)]))
            db.commit()
        except:
            db.rollback()
            traceback.print_exc()
            pass
        finally:
            cursor.close()
            db.close()

    '''
        operate_type = args[0] # Moved Created Deleted Modified ,这里的moved指的是重命名，而不是移动
        file_type = args[1] # file directory
        src_name = args[2] # file or directory name
        des_src_name = ""
        if len(args) > 3:
            des_src_name = args[3] # 只有moved的情况下才存在该参数
    '''

    def update_chche_1(self, *args):
        # self.updateCacheDb(*args)
        self.updateCacheDbByProc(*args)

    # 从数据库查询缓存map
    def get_pyCache_FromDb(self, filename):
        db = cusMysqlUtils.MysqlUtils().db
        cursor = db.cursor()
        result = ""
        try:
            cursor.execute("select st_mtime,doc_cache_path from t_window_doc_cache_map where file_path = %s",
                           pymysql.escape_string(filename))
            sqlReuslt = cursor.fetchone()
            if sqlReuslt:
                result = sqlReuslt[0] + "@" + sqlReuslt[1]
        except:
            traceback.print_exc()
            pass
        finally:
            cursor.close()
            db.close()
        return result

    def update_docCache_Db(self, filename, st_mtime, docx_filename):
        db = cusMysqlUtils.MysqlUtils().db
        cursor = db.cursor()
        try:
            if self.get_pyCache_FromDb(filename):
                cursor.execute("update t_window_doc_cache_map set st_mtime = %s,updateTime = %s where file_path = %s", (
                    [st_mtime, datetime.datetime.now().strftime("%Y%m%d%H%M%S"), pymysql.escape_string(filename)]))
            else:
                cursor.execute(
                    "insert into t_window_doc_cache_map (updateTime,file_path,doc_cache_path,st_mtime) values (%s,%s,%s,%s)",
                    (
                        [datetime.datetime.now().strftime("%Y%m%d%H%M%S"), pymysql.escape_string(filename),
                         pymysql.escape_string(docx_filename), st_mtime]))
            db.commit()
        except:
            db.rollback()
            traceback.print_exc()
            pass
        finally:
            cursor.close()
            db.close()

    def query_fileList_fromDb(self, root_dir):
        db = cusMysqlUtils.MysqlUtils().db
        cursor = db.cursor()
        file_List = []
        try:
            cursor.execute("select full_fileName from t_window_explore_file where full_fileName like %s",
                           ("%" + pymysql.escape_string(root_dir) + "%"))
            result = cursor.fetchall()
            for each in result:
                file_List.append(each[0])
            print(file_List)
        except:
            db.rollback()
            traceback.print_exc()
            pass
        finally:
            cursor.close()
            db.close()
        return file_List

    # 对象销毁调用方法,将map序列化到缓存文件中
    def __del__(self):
        try:
            tmp_map = self.get_cachemap()
            map_keys = tmp_map.keys()
            with open(self.get_cacheFile(), "w", encoding="utf-8") as f:
                for each in map_keys:
                    f.writelines(str(each) + "==>" + str(tmp_map.get(each)) + ",")
                f.close()
        except:
            traceback.print_exc()
            pass
