from treeview_ood2 import *
from tkinter.tix import *
from tkinter import filedialog
import xlwings as xw
from numpy import *
from tkinter.messagebox import *

class QueryFrame(Frame):  # 继承Frame类
    def __init__(self, master=None, db=None, user=None, password=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.db = db
        self.cursor = self.db.cursor()
        self.user = user
        self.password = password
        self.data = []
        self.column = []
        self.databaseName = StringVar()
        self.tableName = StringVar()
        self.fuzzycontent = StringVar()
        self.accuratecontent = StringVar()
        self.myColumnName = StringVar()
        self.filePath = StringVar()
        self.createPage()

    def createPage(self):
        self.frame_top = Frame(self)
        self.frame_top.pack()
        self.frame_mid = Frame(self)
        self.frame_mid.pack()
        self.frame_mid1 = Frame(self)
        self.frame_mid1.pack()
        self.frame_bottom = Frame(self)
        self.frame_bottom.pack()
        Label(self.frame_top, text='查询界面').grid()
        Label(self.frame_mid, text='你要查询的库: ').grid(row=0,column=0,padx=10,pady=10)
        Entry(self.frame_mid, textvariable=self.databaseName).grid(row=0,column=1,padx=10,pady=10)
        Button(self.frame_mid, text='查询库', command=self.selectdatabase).grid(row=0,column=2,padx=10,pady=10)
        Button(self.frame_mid, text='返回数据库列表', command=self.returnDataBaseList).grid(row=0, column=3, padx=10, pady=10)
        Label(self.frame_mid, text='你要查询的表: ').grid(row=1,column=0,padx=10,pady=10)
        Entry(self.frame_mid, textvariable=self.tableName).grid(row=1,column=1,padx=10,pady=10)
        Button(self.frame_mid, text='查询表', command=self.selecttable).grid(row=1,column=2,padx=10,pady=10)
        Button(self.frame_mid, text='返回表名列表', command=self.returnTableBaseList).grid(row=1, column=3, padx=10, pady=10)
        Label(self.frame_mid, text='查看的字段名: ').grid(row=2, column=0, padx=10, pady=10)
        Entry(self.frame_mid, textvariable=self.myColumnName).grid(row=2, column=1, padx=10, pady=10)
        Label(self.frame_mid, text='模糊查询内容: ').grid(row=3, column=0, padx=10, pady=10)
        Entry(self.frame_mid, textvariable=self.fuzzycontent).grid(row=3, column=1, padx=10, pady=10)
        Button(self.frame_mid, text='模糊交集查询', command=self.fuzzyIntersectionQuery).grid(row=3, column=2, padx=10, pady=10)
        Button(self.frame_mid, text='模糊并集查询', command=self.fuzzyUnionQuery).grid(row=3, column=3, padx=10, pady=10)
        Label(self.frame_mid, text='精确查询条件: ').grid(row=4, column=0, padx=10, pady=10)
        Entry(self.frame_mid, textvariable=self.accuratecontent).grid(row=4, column=1, padx=10, pady=10)
        Button(self.frame_mid, text='精确查询', command=self.accuratequery).grid(row=4, column=2, padx=10, pady=10)
        Label(self.frame_mid, text='导出的文件名: ').grid(row=5, column=0, padx=10, pady=10)
        e1 = Entry(self.frame_mid, textvariable=self.filePath)
        e1.grid(row=5, column=1, padx=10, pady=10)
        e1.bind('<Double-Button-1>', self.saveAsFile)
        Button(self.frame_mid, text='数据导出',command=self.download).grid(row=5, column=2, padx=10, pady=10)

        self.cursor.execute("show databases")
        col = self.cursor.description
        column = []
        for i in range(len(col)):
            column.append(col[i][0])

        # 使用fetchall()获取全部数据
        data = self.cursor.fetchall()
        self.tree = SelfTreeView(self.frame_bottom, column, data)

    def download(self):
        file = str(self.filePath.get())
        if len(self.filePath.get()) == 0:
            showinfo(title="提醒", message="请选择存储路径")
            return
        if(len(self.column) == 0 or len(self.data) == 0):
            showinfo(title="提醒", message="导出数据为空")
        try:
            app = xw.App(visible=False, add_book=False)
            wb = app.books.add()
            wb.sheets['sheet1'].range('A1').value = self.column
            wb.sheets['sheet1'].range('A2').value = self.data
            wb.save(file)
            wb.close()
            app.quit()
            app.kill()
        except:
            info = list(sys.exc_info())
            showinfo(title="失败", message="导出数据失败"+str(info[1]))
        else:
            showinfo(title="成功", message="成功从表"+str(self.databaseName)+"."+str(self.tableName)+"导出"+str(self.cursor.rowcount)+"条数据")
            self.filePath = ""

    def saveAsFile(self, event):
        xlfname = filedialog.asksaveasfilename(title='选择存储路径',filetypes=[('EXECL工作簿', '*.xlsx'), ('EXECL工作簿', '*.xls'),
                                                        ('All Files', '*')])
        self.filePath.set(xlfname)

    def accuratequery(self):
        content = self.accuratecontent.get()
        if len(self.tableName.get()) * len(self.databaseName.get()) == 0:
            return
        if len(content) == 0:
            content = "1"
        myColumnName = self.myColumnName.get()
        smyColumnName = myColumnName.strip().lstrip().rstrip()
        amyColumnName = smyColumnName.split(",")
        acolumn = []
        for column in amyColumnName:
            if len(column) != 0:
                acolumn.append(column)
        if len(acolumn) != 0:
            column_condition = ""
            for i in range(0, len(acolumn) - 1):
                column_condition += acolumn[i] + ","
            if len(acolumn[-1]) != 0:
                column_condition += acolumn[-1]
        else:
            column_condition = "*"
        sql = "select "+ column_condition +" from "+self.tableName.get()+" where " + content
        print(sql)
        try:
            self.cursor.execute("use "+self.databaseName.get())
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title='错误', message=str(info[1]))
        else:
            col = self.cursor.description
            column = []
            for i in range(len(col)):
                column.append(col[i][0])

            # 使用fetchall()获取全部数据
            data = self.cursor.fetchall()
            self.column = column
            self.data = data
            if self.cursor.rowcount != 0:
                tl = Toplevel(self.root)
                tl.title("在表" + self.tableName.get() + "精确查找" + content + "后共有" + str(self.cursor.rowcount) + "条的结果")
                self.tree1 = SelfTreeView(tl, column, data)
            else:
                showinfo(title="通知", message="没有匹配项")
        pass

    def returnTableBaseList(self):
        content = self.databaseName.get()
        if len(self.databaseName.get()) == 0:
            return
        try:
            self.cursor.execute("use " + content)
            self.cursor.execute("show tables")
        except:
            info = list(sys.exc_info())
            showinfo(title='错误', message=str(info[1]))
        else:
            col = self.cursor.description
            column = []
            for i in range(len(col)):
                column.append(col[i][0])

            # 使用fetchall()获取全部数据
            data = self.cursor.fetchall()
            self.tree.master.pack_forget()
            self.frame_bottom = Frame(self)
            self.frame_bottom.pack()
            self.tree = SelfTreeView(self.frame_bottom, column, data, self.cursor)

    def fuzzyIntersectionQuery(self):
        content = self.fuzzycontent.get()
        scontent = content.strip().lstrip().rstrip()
        acontent = scontent.split(",")
        if(len(self.databaseName.get()) == 0 or len(self.tableName.get()) == 0):
            return
        self.cursor.execute("use " + self.databaseName.get())
        self.cursor.execute("desc " + self.tableName.get())
        data = self.cursor.fetchall()
        concat = "(concat("
        for i in range(0, len(data) - 2):
            concat = concat + data[i][0] + ",'-',"
        concat = concat + data[-1][0] + ",'-')"
        myColumnName = self.myColumnName.get()
        smyColumnName = myColumnName.strip().lstrip().rstrip()
        amyColumnName = smyColumnName.split(",")
        acolumn = []
        for column in amyColumnName:
            if len(column) != 0:
                acolumn.append(column)
        if len(acolumn) != 0:
            column_condition = ""
            for i in range(0, len(acolumn) - 1):
                column_condition += acolumn[i] + ","
            if len(acolumn[-1]) != 0:
                column_condition += acolumn[-1]
        else:
            column_condition = "*"
        print(column_condition)
        sql_start = "select " + column_condition + " from " + self.tableName.get() + " where "
        sql_middle = ""

        for i in range(0, len(acontent) - 1):
            if len(str(acontent[i])) != 0:
                sql_middle = concat + " like '%" + acontent[i] + "%') and "
        sql_middle = sql_middle + concat + " like '%" + acontent[-1] + "%')"
        sql = sql_start + sql_middle
        print(sql)
        try:
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title='错误', message=str(info[1]))
        else:

            col = self.cursor.description
            column = []
            for i in range(len(col)):
                column.append(col[i][0])

            # 使用fetchall()获取全部数据
            data = self.cursor.fetchall()
            self.column = column
            self.data = data
            if self.cursor.rowcount != 0:
                tl = Toplevel(self.root)
                tl.title("在表" + self.tableName.get() + "模糊并集查找" + scontent + "后共有" + str(self.cursor.rowcount) + "条的结果")
                self.tree1 = SelfTreeView(tl, column, data)
            else:
                showinfo(title="通知", message="没有匹配项")

    def fuzzyUnionQuery(self):
        content = self.fuzzycontent.get()
        scontent = content.strip().lstrip().rstrip()
        acontent = content.split(",")
        if (len(self.databaseName.get()) == 0 or len(self.tableName.get()) == 0):
            return
        self.cursor.execute("use " + self.databaseName.get())
        self.cursor.execute("desc " + self.tableName.get())
        data = self.cursor.fetchall()
        concat = "(concat("
        for i in range(0, len(data) - 2):
            concat = concat + data[i][0] + ",'-',"
        concat = concat + data[-1][0] + ",'-')"
        myColumnName = self.myColumnName.get()
        smyColumnName = myColumnName.strip().lstrip().rstrip()
        amyColumnName = smyColumnName.split(",")
        acolumn = []
        for column in amyColumnName:
            if len(column) != 0:
                acolumn.append(column)
        if len(acolumn) != 0:
            column_condition = ""
            for i in range(0, len(acolumn) - 1):
                column_condition += acolumn[i] + ","
            if len(acolumn[-1]) != 0:
                column_condition += acolumn[-1]
        else:
            column_condition = "*"
        sql_start = "select "+column_condition+" from " + self.tableName.get() + " where "
        sql_middle = ""

        for i in range(0, len(acontent)-1):
            if len(str(acontent[i])) != 0:
                sql_middle = concat + " like '%" + acontent[i] + "%') or "
        sql_middle = sql_middle + concat + " like '%" + acontent[-1] + "%')"
        sql = sql_start + sql_middle
        print(sql)

        self.cursor.execute(sql)
        col = self.cursor.description
        column = []
        for i in range(len(col)):
            column.append(col[i][0])

        # 使用fetchall()获取全部数据
        data = self.cursor.fetchall()
        self.column = column
        self.data = data
        if self.cursor.rowcount != 0:
            tl = Toplevel(self.root)
            tl.title("在表" + self.tableName.get() + "模糊交集查找" + scontent + "后共有" + str(self.cursor.rowcount) + "条的结果")
            self.tree1 = SelfTreeView(tl, column, data)
        else:
            showinfo(title="通知", message="没有匹配项")
        pass

    def selectdatabase(self):
        content = self.databaseName.get()

        if(len(self.databaseName.get()) == 0):
            return
        try:
            self.cursor.execute("use " + content)
            self.cursor.execute("show tables")
        except:
            info = list(sys.exc_info())
            showinfo(title='错误', message='输入错误'+str(info[1]))
        else:
            self.tree.master.pack_forget()
            self.frame_bottom = Frame(self)
            self.frame_bottom.pack()
            col = self.cursor.description
            column = []
            for i in range(len(col)):
                column.append(col[i][0])

            # 使用fetchall()获取全部数据
            data = self.cursor.fetchall()
            self.tree = SelfTreeView(self.frame_bottom, column, data, self.cursor)

    def selecttable(self):
        content = self.tableName.get()
        if len(self.tableName.get()) * len(self.databaseName.get()) == 0:
            return
        myColumnName = self.myColumnName.get()
        smyColumnName = myColumnName.strip().lstrip().rstrip()
        amyColumnName = smyColumnName.split(",")
        print(len(amyColumnName))
        acolumn = []
        for column in amyColumnName:
            if len(column) != 0:
                acolumn.append(column)
        if len(acolumn) != 0:
            column_condition = ""
            for i in range(0, len(acolumn) - 1):
                column_condition += acolumn[i] + ","
            if len(acolumn[-1]) != 0:
                column_condition += acolumn[-1]
        else:
            column_condition = "*"
        try:
            self.cursor.execute("use "+self.databaseName.get())
            self.cursor.execute("select "+column_condition+" from " + content)
        except:
            info = list(sys.exc_info())
            showinfo(title='错误', message='输入错误' + str(info[1]))
        else:
            self.tree.master.pack_forget()
            self.frame_bottom = Frame(self)
            self.frame_bottom.pack()
            col = self.cursor.description
            column = []
            for i in range(len(col)):
                column.append(col[i][0])

            # 使用fetchall()获取全部数据
            data = self.cursor.fetchall()
            self.column = column
            self.data = data
            self.tree = SelfTreeView(self.frame_bottom, column, data, self.cursor)


            # list3=[]
            # for j in range(0,2*len(column)):
            #     list3.append(str(j+1))
            #     list3[j] = StringVar
            # for j in range(0,len(column)):
            #     Label(self.frame_mid1, text=column[j]).grid(row=0, rowspan=2, column=2 * j)
            #     Entry(self.frame_mid1, textvariable=list3[2 * j], width=5).grid(row=0, column=2 * j + 1, pady=5)
            #     Entry(self.frame_mid1, textvariable=list3[2 * j + 1],width=5).grid(row=1, column=2 * j + 1, pady=5)




    def returnDataBaseList(self):
        self.frame_mid1.pack_forget()
        self.frame_mid1 = Frame(self)
        self.frame_mid1.pack()
        self.cursor.execute("show databases")
        self.tree.master.pack_forget()
        self.frame_bottom = Frame(self)
        self.frame_bottom.pack()
        col = self.cursor.description
        column = []
        for i in range(len(col)):
            column.append(col[i][0])
        data = self.cursor.fetchall()
        self.tree = SelfTreeView(self.frame_bottom, column, data,self.cursor)




class InputFrame(Frame):
    # 继承Frame类
    def __init__(self, master=None, db=None, user=None, password=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.db = db
        self.cursor = self.db.cursor()
        self.user = user
        self.password = password
        self.databaseName = StringVar()
        self.tableName = StringVar()
        self.filePath = StringVar()
        self.filePathNames = StringVar()
        self.createPage()

    def createPage(self):
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='请输入你要操作的数据库: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.databaseName).grid(row=1, column=1, stick=E)
        Label(self, text='请输入你要操作的表: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.tableName).grid(row=2, column=1, stick=E)
        Label(self, text='请输入你要操作的Excel:').grid(row=3, stick=W, pady=10)
        e2 = Entry(self, textvariable=self.filePath)
        e2.grid(row=3, column=1, stick=E)
        # Button(self, text='录入', command=self.upload).grid(row=4, column=1, stick=W, pady=10)
        Button(self, text='导出', command=self.download).grid(row=3, column=2, stick=E, pady=10)
        Label(self, text='批量导入多个Excel文件: ').grid(row=4, stick=W, pady=10)
        e1 = Entry(self, textvariable=self.filePathNames)
        e1.grid(row=4, column=1, stick=E)
        Button(self, text='提交', command=self.uploadmany).grid(row=4, column=2, stick=E, pady=10)
        e1.bind('<Double-Button-1>', self.selectfile)
        e2.bind('<Double-Button-1>', self.saveAsFile)
    #
    # def upload(self):
    #     database = str(self.databaseName.get())
    #     table = str(self.tableName.get())
    #     file = str(self.filePath.get())
    #     app = xw.App(visible=False, add_book=False)
    #     app.display_alerts = True
    #     app.screen_updating = True
    #     wb = app.books.open(file)
    #     list1 = []
    #     for sht in wb.sheets:
    #         a = sht.range('A2').expand().value
    #         for i in range(len(a)):
    #             a[i][0] = str(int(a[i][0]))
    #             list1.append(tuple(a[i]))
    #     wb.save()
    #     wb.close()
    #     app.quit()
    #     app.kill()
    #     try:
    #         self.cursor.execute("use " + database)
    #         sql = "insert into " + table + " (id_xl,time_UTC,MMIS,LNG,LNT,LOS,WOS,TP,TOS,SOS,COG,Nationality,Img_resolution,Cha_number,Cha_name,Satellite) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         self.cursor.executemany(sql, list1)
    #         self.db.commit()
    #     except:
    #         info = list(sys.exc_info())
    #         showinfo(title="错误", message=info[1])
    #         self.db.rollback()
    #     else:
    #         showinfo(title="成功", message='向' + database + '.' + table + '成功插入' + str(self.cursor.rowcount) + '条数据')

    def download(self):
        database = str(self.databaseName.get()).strip().lstrip().rstrip()
        table = str(self.tableName.get()).strip().lstrip().rstrip()
        file = str(self.filePath.get())
        if len(database) == 0 or len(table) == 0:
            showinfo(title="警告", message="请输入数据库名及表名")
            return
        try:
            self.cursor.execute("use " + database)
        except:
            info = list(sys.exc_info())
            showinfo(title="警告", message="请输入正确的数据库名"+str(info[1]))
        else:
            try:
                self.cursor.execute("select * from " + table)
            except:
                info = list(sys.exc_info())
                showinfo(title="警告", message="请输入正确的表名"+str(info[1]))
            else:
                col = self.cursor.description
                column = []
                for i in range(len(col)):
                    column.append(col[i][0])
                data = self.cursor.fetchall()
                try:
                    app = xw.App(visible=False, add_book=False)
                    wb = app.books.add()
                    wb.sheets['sheet1'].range('A1').value = column
                    wb.sheets['sheet1'].range('A2').value = data
                    wb.save(file)
                    wb.close()
                    app.quit()
                    app.kill()
                except:
                    info = list(sys.exc_info())
                    showinfo(title="失败",message="导出数据失败"+str(info[1]))
                else:
                    showinfo(title="成功",message="成功从表"+database+"."+table+"导出"+str(self.cursor.rowcount)+"条数据")

    def uploadmany(self):
        database = str(self.databaseName.get()).strip().lstrip().rstrip()
        table = str(self.tableName.get()).strip().lstrip().rstrip()
        filelist = []
        filelist1 = []
        for i in self.filePathNames.get()[1:-1].split(','):
            filelist.append(i.strip().lstrip().rstrip(' ').replace("/", "\\"))
        for i in filelist:
            filelist1.append(i.strip("''"))
        for file in filelist1:
            if file != '':
                app = xw.App(visible=False, add_book=False)
                app.display_alerts = True
                app.screen_updating = True
                wb = app.books.open(file)
                list1 = []
                for sht in wb.sheets:
                    a = sht.range('A2').expand().value
                    if a is not None:
                        b = array(a)
                        if len(b.shape) == 1:
                            a[0] = int(a[0])
                            list1.append(tuple(a))
                        else:
                            for i in range(len(a)):
                                if i is not None:
                                    a[i][0] = int(a[i][0])
                                    list1.append(tuple(a[i]))
                wb.close()
                app.quit()
                app.kill()
                if len(database) == 0 or len(table) == 0:
                    showinfo(title="警告", message="请输入数据库名及表名")
                    return
                try:
                    self.cursor.execute("use " + database)
                    # 插入数据
                except:
                    showinfo(title="警告", message="请输入正确的数据库名")
                else:
                    try:
                        self.cursor.execute("desc " + table)
                    except:
                        info = list(sys.exc_info())
                        showinfo(title="警告", message="请输入正确的表名"+str(str(info[1])))
                    else:
                        data = self.cursor.fetchall()
                        column_name = " ("
                        format = "("
                        for i in range(1, len(data) - 1):
                            column_name = column_name + str(data[i][0]) + ","
                            format = format + "%s,"
                        column_name = column_name + str(data[i + 1][0]) + ")"
                        format = format + "%s)"
                        sql = "insert into " + table + column_name + " values " + format
                        try:
                            self.cursor.executemany(sql, list1)
                            self.db.commit()
                        except:
                            info = list(sys.exc_info())
                            showinfo(title="错误", message=str(info[1]))
                            self.db.rollback()
                        else:
                            showinfo(title="成功",
                                     message='向' + database + '.' + table + '成功插入' + str(self.cursor.rowcount) + '条数据')

    def selectfile(self, event):
        xlfname = filedialog.askopenfilenames(title='打开EXECL文件',
                                              filetypes=[('EXECL工作簿', '*.xlsx'), ('EXECL工作簿', '*.xls'),
                                                         ('All Files', '*')])
        self.filePathNames.set(xlfname)

    def saveAsFile(self, event):
        xlfname = filedialog.asksaveasfilename(title='选择存储路径',filetypes=[('EXECL工作簿', '*.xlsx'), ('EXECL工作簿', '*.xls'),
                                                        ('All Files', '*')])
        self.filePath.set(xlfname)

class AdvanceFrame(Frame):  # 继承Frame类
    def __init__(self, master=None, db=None, user=None, password=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.db = db
        self.cursor = self.db.cursor()
        self.user = user
        self.password = password
        self.mySQL = StringVar()
        self.createPage()

    def createPage(self):
        self.frame_top = Frame(self)
        self.frame_top.pack()
        self.frame_mid = Frame(self)
        self.frame_mid.pack()
        self.frame_bottom = Frame(self)
        self.frame_bottom.pack()
        Label(self.frame_top, text='高级界面').grid()
        Label(self.frame_mid, text='请输入你的SQL语句: ').grid(row=0, column=0, padx=10, pady=10)
        Entry(self.frame_mid, textvariable=self.mySQL, width=30).grid(row=0, column=1, padx=10, pady=10)
        Button(self.frame_mid, text='提交', command=self.mySQLExecute).grid(row=0, column=2, padx=10, pady=10)
        Label(self.frame_mid, text='MySQL语句历史记录: ').grid(row=1, column=0, padx=10, pady=10)
        self.text = Text(self.frame_mid, width=30, height=10)
        self.text.grid(row=1,column=1,padx=10,pady=10)

        Button(self.frame_mid, text='清除', command=self.clearText).grid(row=1,column=2,padx=10,pady=10)
        self.cursor.execute("show databases")
        col = self.cursor.description
        column = []
        for i in range(len(col)):
            column.append(col[i][0])

        data = self.cursor.fetchall()
        self.tree = SelfTreeView(self.frame_bottom, column, data,self.cursor)

    def mySQLExecute(self):
        mysql = str(self.mySQL.get())
        try:
            self.cursor.execute(mysql)
        except:
            info = list(sys.exc_info())
            showinfo(title="错误", message="重新输入，语句错误"+str(info[1]))
            self.db.rollback()
        else:
            col = self.cursor.description
            if col is not None:
                column = []
                for i in range(len(col)):
                    column.append(col[i][0])
                data = self.cursor.fetchall()

                self.tree.master.pack_forget()
                self.frame_bottom = Frame(self)
                self.frame_bottom.pack()
                self.tree = SelfTreeView(self.frame_bottom, column, data, self.cursor)
            self.text.insert("end", mysql + "\n")


    def clearText(self):
        self.text.delete(0.0, END)


class AlterFrame(Frame):  # 继承Frame类
    def __init__(self, master=None, db=None, user=None, password=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.db = db
        self.cursor = self.db.cursor()
        self.user = user
        self.password = password
        self.newTableName = StringVar()
        self.DBName = StringVar()
        self.columnNameNumber = 0
        self.createPage()

    def createPage(self):
        self.frame_top = Frame(self)
        self.frame_top.pack()
        self.frame_mid = Frame(self)
        self.frame_mid.pack()
        self.frame_bottom = Frame(self)
        self.frame_bottom.pack()

        Label(self.frame_top, text='修改界面').grid()
        Label(self.frame_mid, text='要操作的数据库名').grid()
        Entry(self.frame_mid, textvariable=self.DBName).grid(row=0, column=1, padx=10, pady=10)
        Button(self.frame_mid, text="新建", command=self.createDatabase).grid(row=0, column=2, padx=10, pady=10)
        Button(self.frame_mid, text="删除", command=self.dropDatabase).grid(row=0, column=3, padx=10, pady=10)
        Label(self.frame_mid, text='要操作的表名').grid(row=1, padx=10, pady=10)
        Entry(self.frame_mid, textvariable=self.newTableName).grid(row=1, column=1, padx=10, pady=10)
        Button(self.frame_mid, text="新建", command=self.createTable).grid(row=1, column=2, padx=10, pady=10)
        Button(self.frame_mid, text="删除", command=self.dropTable).grid(row=1, column=3, padx=10, pady=10)
        self.text = Text(self.frame_mid, width=30, height=10, wrap="word")
        self.text.grid(row=3, column=0, rowspan=4, padx=10, pady=10)
        self.labelframe1 = Labelframe(self.frame_mid, text="其他参数")
        self.labelframe1.grid(row=3, column=2, rowspan=4, sticky=W, padx=10, pady=10)
        self.labelframe2 = Labelframe(self.frame_mid, text="字段类型")
        self.labelframe2.grid(row=3, column=1, rowspan=4, sticky=W, padx=10, pady=10)
        Button(self.frame_mid, text='添加列+', command=self.add_column).grid(row=3, column=3, padx=10, pady=10)
        Button(self.frame_mid, text='删除列-', command=self.deleteColumn).grid(row=4, column=3, padx=10, pady=10)
        self.ck1 = BooleanVar()
        Checkbutton(self.labelframe1, variable=self.ck1, text="Not Null").grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.ck2 = BooleanVar()
        Checkbutton(self.labelframe1, variable=self.ck2, text="Auto_increment").grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.ck3 = BooleanVar()
        Checkbutton(self.labelframe1, variable=self.ck3, text="Primary Key").grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.ck4 = BooleanVar()
        Checkbutton(self.labelframe1, variable=self.ck4, text="Default").grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.defaultText = Entry(self.frame_mid)
        self.defaultText.grid(row=6, column=3, sticky=W, padx=10, pady=10)

        LANGS = [('CAHR', 1), ('INT', 2), ('FLOAT', 3), ('DATETIME', 4) ]
        self.v = IntVar()
        for lang, num in LANGS:
            b = Radiobutton(self.labelframe2, text=lang, variable=self.v, value=num)

            # fill=X设置和其父窗口一样宽, 可以使用 fill=X 属性

            b.grid(sticky=W, padx=10, pady=10)


    def createDatabase(self):
        sql = "create database " + self.DBName.get()
        try:
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title="失败",message=self.DBName.get()+"数据库创建失败"+str(info[1]))
        else:
            showinfo(title="成功",message=self.DBName.get()+"数据库创建成功")

    def dropDatabase(self):
        sql = "drop database " + self.DBName.get()
        try:
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title="失败",message=self.DBName.get()+"数据库删除失败"+str(info[1]))
        else:
            showinfo(title="成功",message=self.DBName.get()+"数据库删除成功")

    def createTable(self):
        if (len(self.DBName.get()) == 0) or (len(self.newTableName.get()) == 0):
            showinfo(title="提示", message="请输入表名或数据库名")
            return
        sql_start = "create table "+self.DBName.get()+"."+self.newTableName.get()+"("
        sql_end = ")engine myisam charset utf8;"
        content = self.text.get("0.0", "end").splitlines()
        print(content)
        sql = ""
        for k in range(0, len(content)-2):
            sql = sql+content[k]+","
        sql = sql+content[-2]
        sql = sql_start + sql + sql_end
        print(sql)
        try:
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title="失败", message="表"+self.DBName.get()+"."+self.newTableName.get()+"创建失败"+str(info[1]))
        else:
            showinfo(title="成功", message="表"+self.DBName.get()+"."+self.newTableName.get()+"创建成功")
        self.columnNameNumber = 0

    def dropTable(self):
        sql = "drop table " + self.DBName.get()+"."+self.newTableName.get()
        try:
            self.cursor.execute(sql)
        except:
            info = list(sys.exc_info())
            showinfo(title="失败", message=self.DBName.get()+"."+self.newTableName.get() + "删除失败"+str(info[1]))
        else:
            showinfo(title="成功", message=self.DBName.get()+"."+self.newTableName.get() + "删除成功")

    def add_column(self):
        if self.v.get() == 1:
            cType = " varchar(100)"
            self.ck2.set(0)
            self.ck3.set(0)
        elif self.v.get() == 2:
            cType = " int"
        elif self.v.get() == 3:
            cType = " float(6,2)"
            self.ck2.set(0)
            self.ck3.set(0)
        elif self.v.get() == 4:
            cType = " datetime"
            self.ck2.set(0)
            self.ck3.set(0)
        else:
            showinfo(title="警告", message="请选择数据类型")
        if self.ck2.get() == 1:
            auto_increment_status = " auto_increment"
        else:
            auto_increment_status = ""
        if self.ck3.get() == 1:
            primary_key_status = " primary key"
            null_statue = ""
            auto_increment_status = " auto_increment"
            default_text = ""
        else:
            primary_key_status = ""
            if self.ck1.get() == 1:
                null_statue = " not null"
            else:
                null_statue = " null"
            if self.ck4.get() == 1 and len(self.defaultText.get()) != 0:
                default_text = " default '" + self.defaultText.get() + "'"
            else:
                default_text = ""
        sql = "column_name"+ str(self.columnNameNumber) + cType+primary_key_status\
              + auto_increment_status + null_statue+default_text
        self.text.insert("end", sql + "\n")
        self.text.see(END)
        self.text.update()
        self.columnNameNumber = self.columnNameNumber + 1

    def deleteColumn(self):
        if len(self.text.get("end-1c linestart", END)) == 1:
            self.text.delete('%s - 2 lines' % 'end', END)
        else:
            self.text.delete("end-1c linestart", END)

    def clearText(self):
        self.text.delete(0.0, END)


class AboutFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='关于界面').pack()


class UserFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='用户管理界面').pack()