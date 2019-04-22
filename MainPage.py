from view import *  # 菜单栏对应的各个子页面


class MainPage(object):
    def __init__(self, master=None, db=None, user=None, password=None):
        self.root = master  # 定义内部变量root
        self.db = db
        self.user = user
        self.password = password
        self.root.geometry('%dx%d' % (800, 600))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.inputPage = InputFrame(self.root, self.db, self.user, self.password)  # 创建不同Frame
        self.queryPage = QueryFrame(self.root, self.db, self.user, self.password)
        self.alterPage = AlterFrame(self.root, self.db, self.user, self.password)
        self.advancePage = AdvanceFrame(self.root, self.db, self.user, self.password)
        self.aboutPage = AboutFrame(self.root)
        self.userPage = UserFrame(self.root)
        self.queryPage.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='查询', command=self.queryData)
        menubar.add_command(label='录入导出', command=self.inputData)
        menubar.add_command(label='高级', command=self.advanceData)
        menubar.add_command(label='修改', command=self.alterDatabase)
        menubar.add_command(label='用户管理', command=self.userDisp)
        menubar.add_command(label='关于', command=self.aboutDisp)
        self.root['menu'] = menubar  # 设置菜单栏

    def queryData(self):
        self.queryPage.pack()
        self.inputPage.pack_forget()
        self.advancePage.pack_forget()
        self.aboutPage.pack_forget()
        self.alterPage.pack_forget()
        self.userPage.pack_forget()

    def inputData(self):
        self.queryPage.pack_forget()
        self.inputPage.pack()
        self.advancePage.pack_forget()
        self.aboutPage.pack_forget()
        self.alterPage.pack_forget()
        self.userPage.pack_forget()

    def advanceData(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.advancePage.pack()
        self.aboutPage.pack_forget()
        self.alterPage.pack_forget()
        self.userPage.pack_forget()

    def aboutDisp(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.advancePage.pack_forget()
        self.aboutPage.pack()
        self.alterPage.pack_forget()
        self.userPage.pack_forget()

    def alterDatabase(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.advancePage.pack_forget()
        self.aboutPage.pack_forget()
        self.alterPage.pack()
        self.userPage.pack_forget()

    def userDisp(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.advancePage.pack_forget()
        self.aboutPage.pack_forget()
        self.alterPage.pack_forget()
        self.userPage.pack()