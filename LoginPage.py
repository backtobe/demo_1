from MainPage import *
from pymysql import *


class LoginPage(object):
    def __init__(self, master=None):

        self.root = master

        # 窗口居中显示
        width = 300
        height = 180
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        # self.window.geometry("300x180")
        # 不能调动大小
        # self.root.resizable(0, 0)
        self.user = None
        self.psword = None
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=1, stick=E)

    def loginCheck(self):
        self.user = str(self.username.get())

        self.psword = str(self.password.get())
        try:
            # connect("localhost", str(self.username.get()), str(self.password.get()), "empty")
            self.db = connect("localhost", str(self.username.get()), str(self.password.get()), "empty")
        except:
            showinfo(title="失败", message="账户名或密码错误!")
        else:
            showinfo(title="成功", message="登陆成功")
            self.page.destroy()
            MainPage(self.root, self.db, self.user, self.psword)
            self.root.title('船只遥感数据管理系统 -u '+self.user)