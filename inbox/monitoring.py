import os
import sys

import win32file
import win32con
from pyCache import SearchCache
import pymysql  # pip install pymysql
import datetime
import cusMysqlUtils
import traceback


class exploreMonitor():
    searchCache = SearchCache()

    # 打开数据库连接
    db = pymysql.connect("127.0.0.1", "jones", "jones", "test")

    ACTIONS = {
        1: "Created",
        2: "Deleted",
        3: "Updated",
        4: "Renamed from something",
        5: "Renamed to something"
    }

    FILE_LIST_DIRECTORY = 0x0001

    path_to_watch = "E:/java/ideaWorkspace/pythonTest/tmp"
    print('Watching changes in', path_to_watch)
    hDir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while 1:

        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None)
        for action, filename in results:
            full_filename = os.path.join(path_to_watch, filename)
            # print ("1111",full_filename, ACTIONS.get(action, "Unknown"))
            if os.path.splitext(full_filename)[1] != ".tmp" and full_filename.find("~$") == -1 and action == 3:
                print("22222", full_filename, ACTIONS.get(action, "Unknown"))
                searchCache.update_chche(full_filename, action)
                cursor = db.cursor()
                try:
                    # cursor.execute(
                    #     "insert into t_window_explore_update_log(updateTime,full_name,updateType) values (%s,%s,%s)", (
                    #         str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), pymysql.escape_string(full_filename.replace("\\","/")), 4))
                    cursor.execute(
                        "insert into t_window_explore_update_log(updateTime,full_name,updateType) values (%s,%s,%s)",
                        (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), pymysql.escape_string(full_filename.replace("\\", "/")), 4))
                    # 提交到数据库执行
                    db.commit()
                except:
                    traceback.print_exc()
                    # 如果发生错误则回滚
                    db.rollback()

    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    exploreMonitor = exploreMonitor()
