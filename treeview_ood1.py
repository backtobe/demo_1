from tkinter import *
from tkinter.ttk import *  # 导入内部包
from PIL import Image,ImageTk


class SelfTreeView(Treeview):

    def __init__(self, master=None, column_name=[], data=[], cursor=None):
        Treeview.__init__(self, master)
        self.root = master
        self.column_name = column_name
        self.data = data
        self.cursor = cursor
        self.flag = 0
        self.text = None
        # print(self.column_name, self.data)
        self.createTreeView1()


    def createTreeView1(self):
        list1 = []
        for i in self.column_name:
            list1.append(i)
        Label(self.root, width=10).pack(side=LEFT)
        Label(self.root, width=10).pack(side=RIGHT)
        self.tree = Treeview(self.root, columns=list1, show='headings', height=30)

        for i, j in zip(list1, self.column_name):
            self.tree.column(i, width=150, anchor='center')
            self.tree.heading(i, text=j)

        for i in self.data:
            self.tree.insert('', 'end', values=i)
        # self.tree.pack(side=BOTTOM)
        # self.tree.grid(row=1, column=0, sticky=SE)

        # y滚动条

        yscrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)

        self.tree.configure(yscrollcommand=yscrollbar.set)

        yscrollbar.pack(side=RIGHT, fill=Y)

        # x滚动条

        xscroll = Scrollbar(self.root, orient=HORIZONTAL, command=self.tree.xview)

        self.tree.configure(xscrollcommand=xscroll.set)

        xscroll.pack(side=BOTTOM, fill=X)

        self.tree.pack(side=TOP, expand=0, fill=BOTH,anchor=CENTER)

        self.tree.bind('<Double-1>', self.treeviewDoubleClick)

        for col in list1:  # 给所有标题加（循环上边的“手工”）

            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column( _col, False))


    def treeviewDoubleClick(self, event):  # 单击
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            self.text =item_text
            if self.column_name[0] == "Database":
                # print("顶级库列表")
                pass
            elif self.column_name[0].startswith("Tables"):
                # print(self.column_name)
                # print("在表列表中")
                pass
            else:
                try:
                    self.column_name.index("table_level")
                except:
                    pass
                else:
                    # try:
                    #     self.column_name.index("url")
                    # except:
                    #     pass
                    # else:
                    #     Image.open("G:/code/python3/bishe/parent_images/1.jpg").show()
                    if int(item_text[1]) == 0 and str(type(self.master)).split(".")[1].startswith("Frame"):
                        if len(item_text[2]) != 0:
                            filial_name = item_text[2].split(",")
                            for name in filial_name:
                                self.cursor.execute("select * from " + name + " where parent_id = " + item_text[0] )
                                col = self.cursor.description
                                column = []
                                for i in range(len(col)):
                                    column.append(col[i][0])
                                data = self.cursor.fetchall()
                                if len(data) != 0:
                                    tl = Toplevel(self.root)
                                    tl.title("与"+name+"关联"+str(self.cursor.rowcount)+"条数据")
                                    width = 300
                                    height = 180
                                    screenwidth = self.root.winfo_screenwidth()
                                    screenheight = self.root.winfo_screenheight()
                                    alignstr = '%dx%d+%d+%d' % (
                                    width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                                    tl.geometry(alignstr)
                                    SelfTreeView(tl, column, data, self.cursor)
                    elif int(item_text[1]) == 1:
                        if len(item_text[2]) != 0 and self.cursor is not None:
                            self.cursor.execute("select * from " + item_text[2] + " where id = " + item_text[3])
                            col = self.cursor.description
                            column = []
                            for i in range(len(col)):
                                column.append(col[i][0])
                            data = self.cursor.fetchall()
                            if len(data) != 0:
                                tl = Toplevel(self.root)
                                tl.title("与"+item_text[2]+"关联"+str(self.cursor.rowcount)+"条数据")
                                width = 300
                                height = 180
                                screenwidth = self.root.winfo_screenwidth()
                                screenheight = self.root.winfo_screenheight()
                                alignstr = '%dx%d+%d+%d' % (
                                    width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                                tl.geometry(alignstr)
                                SelfTreeView(tl, column, data, self.cursor)
                        if len(item_text[4]) != 0:
                            filial_name = item_text[4].split(",")
                            for name in filial_name:
                                self.cursor.execute("select * from " + name + " where parent_id = " + item_text[0] )
                                # self.cursor.execute("select * from " + name)
                                col = self.cursor.description
                                column = []
                                for i in range(len(col)):
                                    column.append(col[i][0])
                                data = self.cursor.fetchall()
                                if len(data) != 0:
                                    tl = Toplevel(self.root)
                                    tl.title("与"+name+"关联"+str(self.cursor.rowcount)+"条数据")
                                    width = 300
                                    height = 180
                                    screenwidth = self.root.winfo_screenwidth()
                                    screenheight = self.root.winfo_screenheight()
                                    alignstr = '%dx%d+%d+%d' % (
                                    width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                                    tl.geometry(alignstr)
                                    SelfTreeView(tl, column, data)






                        # for item in self.tree.selection():
                        #     item_text = self.tree.item(item, "values")
                        # print(item_text)  # 输出所选行的第一列的值

    def treeview_sort_column(self, col, reverse):  # Treeview、列名、排列方式

        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        for i in l:
            if i[0].isdigit():
                self.flag = self.flag + 1

        if self.flag == len(l):
            l = sorted(l, key=lambda x: int(x[0]), reverse=reverse)
        else:
            l.sort(reverse=reverse)


        # print(tv.get_children(''))

        # l.sort(reverse=reverse)  # 排序方式


        # rearrange items in sorted positions

        for index, (val, k) in enumerate(l):  # 根据排序后索引移动

            self.tree.move(k, '', index)

            # print(k)

        self.tree.heading(col, command=lambda: self.treeview_sort_column( col, not reverse))  # 重写标题，使之成为再点倒序的标题
        self.flag = 0

def arrIndex(arr, str):
    try:
        arr.index(str)
    except:
        return -1
    else:
        return arr.index(str)











