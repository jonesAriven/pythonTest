import wx
import os
import traceback
import sys
from win32com import client as wc
import xlrd


class DirDialog(wx.Frame):
    def __init__(self):
        """Constructor"""
        super(DirDialog, self).__init__()
        wx.Frame.__init__(self, None, wx.ID_ANY, "文件浏览器", pos=(0, 0), size=(730, 580))
        self.Center()
        panel = wx.Panel(parent=self)  # 面板
        b = wx.Button(panel, -1, '浏览', pos=(600, 90))

        c = wx.Button(panel, -1, '更新搜索范围', pos=(600, 160))

        a = wx.Button(panel, -1, '搜索', pos=(600, 50))
        self.Bind(wx.EVT_BUTTON, self.search_file, a)
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.Bind(wx.EVT_BUTTON, self.update_db, c)

        self.inputText1 = wx.TextCtrl(panel, -1, '', pos=(87, 50), size=(500, 30), name='TC01', style=wx.ALIGN_LEFT)
        self.inputText2 = wx.TextCtrl(panel, -1, '', pos=(87, 90), size=(500, 30), name='TC02', style=wx.ALIGN_LEFT)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        statictext1 = wx.StaticText(parent=panel, pos=(20, 55), label='查找内容:')
        statictext2 = wx.StaticText(parent=panel, pos=(20, 95), label='输入路径:')
        statictext3 = wx.StaticText(parent=panel, pos=(609, 200), label='输入路径范围\n以更新数据库')
        statictext4 = wx.StaticText(parent=panel, pos=(85, 135), label='文件名称')
        statictext5 = wx.StaticText(parent=panel, pos=(286, 135), label='文件路径')

        self.listb1 = wx.ListBox(panel, -1, pos=(85, 160), size=(200, 340),
                                 style=wx.LB_SINGLE)  # style=wx.LB_SINGLE单选

        self.listb = wx.ListBox(panel, -1, pos=(286, 160), size=(300, 340),
                                style=wx.LB_SINGLE)  # style=wx.LB_SINGLE单选
        self.Bind(wx.EVT_LISTBOX, self.on_list, self.listb1)
        self.Bind(wx.EVT_LISTBOX, self.on_list, self.listb)

        hbox1.Add(statictext1, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        hbox1.Add(statictext2, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        hbox1.Add(statictext3, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        hbox1.Add(statictext4, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
        hbox1.Add(statictext5, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)

        hbox1.Add(self.listb1, 1, flag=wx.ALL | wx.EXPAND)
        hbox1.Add(self.listb, 1, flag=wx.ALL | wx.EXPAND)

    #
    #  # 更新数据库
    def update_db(self,event):
        pass
    #     if (isExistDB == False):
    #         #tkinter.messagebox.showwarning("警告", "数据不存在，将更新数据库文件！")
    #         try:
    #             mycursor = connection.cursor()
    #             #file_sql = "delete from table where id in (select id from table order by id limit 0, 20)"
    #             file_sql = "create table filepath('file_path' text,'file_name' text not null)"
    #             mycursor.execute(file_sql)
    #             mycursor.close()
    #             self.insert_db()
    #             sys.stdout.flush()
    #         except:
    #             wx.MessageBox('数据库发生异常', '错误提示', wx.OK | wx.ICON_INFORMATION)
    #             return
    #     else:
    #         mycursor = connection.cursor()
    #         wx.MessageBox('正在删除原数据表', '错误提示', wx.OK | wx.ICON_INFORMATION)
    #         drp_tb_sql = "drop table if exists filepath"
    #         file_sql = "create table filepath('file_path' text,'file_name' text not null)"
    #         mycursor.execute(drp_tb_sql)
    #         mycursor.execute(file_sql)
    #         self.insert_db()
    #         sys.stdout.flush()
    #
    #
    # def obtain_all_files(self,filepath, cursor):
    #
    #     try:
    #         files = os.listdir(filepath)
    #
    #         for fi in files:
    #             fi_d = os.path.join(filepath, fi)
    #             print('测试' + fi)
    #             print('测试' + fi_d)
    #             print('测试' + filepath)
    #             if os.path.isdir(fi_d):
    #                 print('测试' + fi_d)
    #                 sqlAdd1 = "insert into filepath (file_path,file_name) values ('" + fi_d + "','" + fi + "')"
    #                 cursor.execute(sqlAdd1)
    #
    #                 print("sqlAdd", sqlAdd1)
    #                 self.obtain_all_files(fi_d, cursor)
    #             else:
    #
    #                 path = os.path.join(filepath, fi_d)
    #
    #                 #update_progress.set(filepath)
    #
    #                 print("目录", filepath)
    #                 print("目录", path)
    #                 sqlAdd = "insert into filepath (file_path,file_name) values ('" + path + "','" + fi + "')"
    #
    #                 print("sqlAdd", sqlAdd)
    #                 cursor.execute(sqlAdd)
    #     except Exception as e:
    #         traceback.print_exc()
    #         print("扫描文件出异常了，点击确定跳过继续扫描")
    #         wx.MessageBox('扫描出现异常', '错误提示', wx.OK | wx.ICON_INFORMATION)
    #
    #
    # def scan_file(self):
    #     print("开始扫描文件")
    #     #   del myArr[:]
    #     connection.execute("BEGIN TRANSACTION;")  # 关键点
    #     cursor = connection.cursor()
    #
    #     entry_text1 = self.inputText2.GetValue()
    #
    #     self.obtain_all_files(entry_text1, cursor)
    #
    #     print("扫描完成...")
    #     wx.MessageBox('扫描完成,您可以开始搜索', '温馨提示', wx.OK | wx.ICON_INFORMATION)
    #     connection.execute("COMMIT;")  # 关键点
    #     connection.commit()
    #     #connection.close()
    #
    #
    #
    # def insert_db(self):
    #     t1 = threading.Thread(target = self.scan_file)
    #     t1.setDaemon(True)
    #     t1.start()
    #
    #
    # # 文件名搜素pass
    def search_file(self, event):
        pass

#
#     print("数据库是否存在: ", isExistDB)
#     if (isExistDB == False):
#         wx.MessageBox('数据不存在,将更新文件', '提示', wx.OK | wx.ICON_INFORMATION)
#         try:
#             mycursor = connection.cursor()
#             file_sql = "create table filepath('file_path' text,'file_name' text not null)"
#             mycursor.execute(file_sql)
#             mycursor.close()
#             self.insert_db()
#         except:
#             wx.MessageBox('数据库发生异常', '错误提示', wx.OK | wx.ICON_INFORMATION)
#             return
#     else:
#         print("开始搜索")
#
#         del myArr[:]
#         #self.listb.delete(0, wx.constants.END)
#
#         #self.listb1.delete(0, wx.constants.END)
#         self.listb.Clear()
#         self.listb1.Clear()
#         mycursor = connection.cursor()
#         mycursor2 = connection.cursor()
#         #entry_text2=inputText2.get()
#         entry_text = self.inputText1.GetValue()
#
#         search_sql = "select file_path from filepath where file_name like '%" + entry_text + "%'"
#         search_name="select file_name from filepath where file_name like '%" + entry_text + "%'"
#         files = mycursor.execute(search_sql)
#         names = mycursor2.execute(search_name)
#         entry_text1 = self.inputText2.GetValue()
#         s=self.main(entry_text, entry_text1)
#         #print(s)
#         #listb.insert(tkinter.constants.END, s)
#
#         print(myArr)
#         for f in files:
#
#             print(f)
#             myArr.append(f)
#
#             # self.listb.insert(tkinter.constants.END, f)
#             self.listb.Append(f)
#         for n in names:
#             print(n)
#
#             myArr.append(n)
#
#             # self.listb1.insert(tkinter.constants.END, n)
#             self.listb1.Append(n)
#         mycursor.close()
#         mycursor2.close()
#
#
# # word 和 excel 内部搜素
# def checkdocx(self,dstStr,fn):
#     document=Document(fn)
#     for p in document.paragraphs:
#         if dstStr in p.text:
#             global h
#             h=p.text
#
#             #return p.text
#             return True
#     for table in document.tables:
#         for row in table.rows:
#             for cell in row.cells:
#                 if dstStr in cell.text:
#
#                     h = cell.text
#
#                     return p.text
#                     return True
#     return False
#
# def checkxlsx(self,dstStr,fn):
#     wb=load_workbook(fn)
#     for ws in wb.worksheets:
#         for row in ws.rows:
#             for cell in row:
#                 try:
#                     if re.search( dstStr, cell.value, re.M|re.I):
#                         #if dstStr in cell.value:
#                         # m=re.search( dstStr, cell.value, re.M|re.I)
#                         # m.span(0)
#                         # print(m)
#                         #h = cell.value
#
#                         return cell.value
#                         return True
#                 except:
#                     pass
#     return False
#
# # 主函数
# def main(self,dstStr,flag):
#
#     dirs=[flag]
#     while dirs:
#         currentDir=dirs.pop(0)
#         #print(currentDir)
#         for fn in listdir(currentDir):
#             path=join(currentDir,fn)
#             if isfile(path):
#                 if path.endswith('.docx')and self.checkdocx(dstStr,path):
#
#                     print(path)
#                     e = tuple(path.split(","))
#                     myArr.append(e)
#                     entry_text = self.inputText1.GetValue()
#
#                     (filepath, tempfilename) = os.path.split(path+'(从内部搜索到)')
#                     t=tuple(tempfilename.split(","))
#                     # self.listb1.insert(tkinter.constants.END, t)
#                     # self.listb.insert(tkinter.constants.END, e)
#                     self.listb1.Append(t)
#                     self.listb.Append(e)
#                 elif path.endswith('.xlsx') and self.checkxlsx(dstStr,path):
#                     print(path)
#                     e = tuple(path.split(","))
#                     myArr.append(e)
#
#                     # self.listb.insert(tkinter.constants.END, e)
#                     self.listb.Append(e)
#                     entry_text = self.inputText1.GetValue()
#
#                     (filepath, tempfilename) = os.path.split(path + '(从内部搜索到)')
#                     t = tuple(tempfilename.split(","))
#                     # self.listb1.insert(tkinter.constants.END, t)
#                     self.listb1.Append(t)
#             elif flag and isdir(path):
#                 dirs.append(path)
#
#
# # OS操作,通过点击路径打开文件
    def on_list(self,event):
        pass
#     listbox = event.GetEventObject()
#     print("选择{0}".format(listbox.GetSelection()))
#     index=listbox.GetSelection()
#     start_directory = str(myArr[index])
#     print(start_directory[2:-3])
#     os.startfile(start_directory[2:-3])
#
# # 浏览文件夹添加路径
    def OnButton(self, event):
        pass


#     """"""
#     dlg = wx.DirDialog(self, u"选择文件夹", style = wx.DD_DEFAULT_STYLE)
#     if dlg.ShowModal() == wx.ID_OK:
#         print(
#             dlg.GetPath())
#         # 文件夹路径
#         d=dlg.GetPath()
#         self.inputText2.AppendText(d)
#     dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(0)
    DirDialog()
    app.MainLoop()
