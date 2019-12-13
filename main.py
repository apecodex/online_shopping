# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
from admin import sql
from admin import register
import os
import time

class_sql = sql.AdminSQL() # 实例化
times2 = 300 # 倒计时

class LoginMain():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = {}

    def checkUsername(self):
        if self.username.strip() == "":
            return "请输入用户名!"
        else:
            self.db['username'] = self.username
            return None

    def checkPassword(self):
        if self.password.strip() == "":
            return "请输入密码!"
        else:
            self.db['password'] = self.password
            return None

    def searchSQL(self, db):
        search_username = class_sql.searchAloneUsernameDB(db['username'])     # 查询用户名
        if search_username != None:    # 判断查询的结果是否为None,如果为None,则用户名不存在数据库
            search_password = class_sql.searchAlonePasswordDB(search_username)    # 判断不为None时,开始查询密码
            hashpassword = register.HashMd5(db['username'] ,db['password']).password    # 利用用户输入的生成新的hash
            if hashpassword != search_password:    # 如果新生成的hash与数据库中的不同，则密码错误
                return "用户名或密码有误!"
            else:
                if hashpassword == search_password:
                    return None
        else:
            return "用户名或密码有误!"

class RegisterMain():

    def __init__(self,username, age, gender, password, enter_password, mail):
        self.username = username
        self.age = age
        self.gender = gender
        self.password = password
        self.enter_password = enter_password
        self.mail = mail
        self.re_username = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9]+$')  # 输入的格式只能包含字母和数字,且字母开头
        self.re_password = re.compile(r'^[0-9a-zA-Z]+[0-9a-zA-Z!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
        self.re_mail = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}')  # 匹配邮箱
        self.db = {}

    def checkUsername(self):
        if self.username.strip() == "":
            return "不能为空!"
        elif len(self.username) < 6 or len(self.username) > 15:
            return "太长或太短,请输入6-15个字"
        elif self.re_username.findall(self.username) == [] or len(self.username) != len("".join(self.username.split())):
            return "格式有误,包含字母、数字或特殊字符"
        elif class_sql.searchAloneUsernameDB(self.username) != None:
            return "用户名已存在!"
        else:
            self.db["username"] = self.username
            return None

    def checkAge(self):
        if self.age.strip() == "":
            return "请输入年龄"
        try:
            self.age = int(self.age)
        except ValueError:
            return "请输入正确的年龄"
        if int(self.age) < 0 or int(self.age) > 150:
            return "请输入正确的年龄"
        else:
            self.db['age'] = self.age
            return None

    def checkGender(self):
        self.db['gender'] = self.gender

    def checkPassword(self):
        if self.password.strip() == "":
            return "密码不能为空!"
        elif len(self.password) < 6:
            return "密码太弱，请输入6位数以上"
        elif self.re_password.findall(self.password) == []:  # 如果为空说明匹配失败，输入不符合要求
            return "格式有误,需包含字母、数字或特殊符号"
        else:
            return None

    def checkEnterPassword(self):
        if self.enter_password.strip() == "":
            return "确认密码!"
        elif self.enter_password != self.password:
            return "两次密码不相同!"
        else:
            if self.checkUsername() == None:
                self.db["password"] = register.HashMd5(self.db["username"], self.enter_password).password  # 调用HashMd5对象进行加盐
                return None

    def checkMail(self):
        if self.mail.strip() == "":
            return "请输入邮箱地址"
        elif self.re_mail.findall(self.mail) == []:  # 如果为空,则匹配失败，说明输入有误
            return "邮箱格式有误!"
        elif class_sql.searchAloneMailDB(self.mail) != None:
            return "此邮箱已存在!"
        else:
            self.db["mail"] = self.mail

class FindPassword():

    def __init__(self):
        self.re_password = re.compile(r'^[0-9a-zA-Z]+[0-9a-zA-Z!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
        self.re_mail = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}')  # 匹配邮箱
        self.db = {}

    def checkUsername(self, username):
        if username.strip() == "":
            return "请输入用户名"
        elif class_sql.searchAloneUsernameDB(username) != None:
            self.db['username'] = username
            return None
        else:
            return "用户名不存在!"

    def checkMail(self, mail):
        if mail.strip() == ""   :
            return "请输入邮箱地址"
        elif self.re_mail.findall(mail) == []:  # 如果为空,则匹配失败，说明输入有误
            return "邮箱格式有误!"
        elif class_sql.searchAloneMailDB(mail) != None:
            self.db["mail"] = mail
            return None
        else:
            return "此邮箱不存在!"
    
    # 用户名和邮箱地址是否是绑定正确
    def IsDate(self):
        if self.db == {} or len(self.db) != 2:
            pass
        else:
            username, mail = self.db['username'], self.db['mail']
            record = class_sql.searchFindPassword(username, mail)
            if record != None:
                return None
            else:
                return "用户名或邮箱有误!"

    def checkExists(self, password):
        if password.strip() == "":
            return "密码不能为空!"
        elif len(password) < 6:
            return "密码太弱!"
        elif self.re_password.findall(password) == []:  # 如果为空说明匹配失败，输入不符合要求
            return "字母、数字或特殊符号"
        else:
            return None


class MainSystem():

    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0

    def __init__(self):
        self.default_bg = "#800040"
        self.osname = os.name
        self.root = Tk()   # 实例化
        img = ImageTk.PhotoImage(Image.open("images/head.ico"))
        self.root.tk.call('wm', 'iconphoto', self.root._w, img)    # 设置ico图标
        self.root.title("apecode")
        self.root.wm_attributes('-topmost',1)   # 将窗口顶置~
        self.root.overrideredirect(TRUE)    # 去除边框
        self.root.attributes("-alpha", 0.8)    # 透明度20%,仅对windows有效
        self.ws = self.root.winfo_screenwidth()    # 获取显示器的宽度
        self.hs = self.root.winfo_screenheight()    # 获取显示器的高度
        self.w, self.h = 800, 500    # 设置宽高为800x500
        self.x, self.y = (self.ws / 2) - (self.w / 2), (self.hs / 2) - (self.h / 2)    # 在屏幕正中弹出
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.root.maxsize("800", "500")    # 锁定高度和宽度
        self.root.minsize("800", "500")
        self.root.config(bg=self.default_bg)
        self.exit_photo = PhotoImage(file="images/exit.png")    # 退出的图标
        self.color_photo = PhotoImage(file="images/color.png")    # 更换颜色的图标
        self.welcome_png = PhotoImage(file="images/Welcome.png")    # 欢迎的图标
        self.username_photo = PhotoImage(file="images/username.png")   # 用户名图标
        self.password_photo = PhotoImage(file="images/password.png")   # 密码图标
        self.login_photo = PhotoImage(file="images/login.png")    # 登录图标
        self.register_photo = PhotoImage(file="images/register.png")   # 注册图标
        self.forget_password_photo = PhotoImage(file="images/forgetpassword.png")   # 忘记密码图标
        self.welcomelabe = Label(self.root, image=self.welcome_png, bg=self.default_bg)
        self.welcomelabe.place(x=120,y=-35)
        self.button_var = StringVar()
        self.root.bind('<B1-Motion>', self._on_move)    # 拖动
        self.root.bind('<ButtonPress-1>', self._on_tap)

    # 拖动功能
    def _on_move(self, event):
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.w and self.w:
            geo_str = "%sx%s+%s+%s" % (self.w, self.w, self.abs_x + offset_x, self.abs_y + offset_y)
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        self.root.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y = event.x_root, event.y_root
        self.abs_x, self.abs_y = self.root.winfo_x(), self.root.winfo_y()

    def isPosix(self):
        if self.osname == "posix":
            self.root.overrideredirect(FALSE)    # Linux恢复边框

    # 禁用按钮，防止多次点击
    def disabledAllButton(self):
        self.login_button.config(state=DISABLED)
        self.forget_button.config(state=DISABLED)
        self.register_button.config(state=DISABLED)
        self.change_button.config(state=DISABLED)
        if self.osname == "posix":
            pass
        else:
            self.exit_buttom.config(state=DISABLED)

    # 恢复按钮的正常显示
    def normarlAllButton(self):
        self.login_button.config(state=NORMAL)
        self.forget_button.config(state=NORMAL)
        self.register_button.config(state=NORMAL)
        self.change_button.config(state=NORMAL)
        if self.osname == "posix":
            pass
        else:
            self.exit_buttom.config(state=NORMAL)
        if self.button_var.get() == "1":
            try:
                self.register_window.destroy()
                self.forget_window.destroy()
            except AttributeError:
                pass
        if self.button_var.get() == "2":
            try:
                self.forget_window.destroy()
                self.register_window.destroy()
            except AttributeError:
                pass
        self.root.attributes("-topmost", 1)  # 恢复root窗口的置顶

    # 检查用户信息(输入格式，是否存在)
    def checkInformatsion(self):
        re_username = self.register_username_var.get()
        re_age = self.register_age_var.get()
        re_gender = self.register_gender_var.get()
        re_password = self.register_password_var.get()
        re_enter_password = self.register_enter_password_var.get()
        re_mail = self.register_mail_var.get()
        self.tips_re_username = Label(self.register_center_frame, width=35,bg=self.default_bg, font=("Aiarl",8))
        self.tips_re_age = Label(self.register_center_frame, width=35, bg=self.default_bg, font=("Aiarl",8))
        self.tips_re_password = Label(self.register_center_frame, width=35, bg=self.default_bg, font=("Aiarl",8))
        self.tips_re_enter_password = Label(self.register_center_frame, width=35, bg=self.default_bg, font=("Aiarl",8))
        self.tips_re_mail = Label(self.register_window, width=35, bg=self.default_bg, font=("Aiarl", 8))
        if self.osname == "posix":
            self.tips_re_username.place(x=0,y=45)
            self.tips_re_age.place(x=0, y=100)
            self.tips_re_password.place(x=0, y=200)
            self.tips_re_enter_password.place(x=0, y=250)
            self.tips_re_mail.place(x=0, y=305)
        else:
            self.tips_re_username.place(x=0, y=40)
            self.tips_re_age.place(x=0, y=90)
            self.tips_re_password.place(x=0, y=185)
            self.tips_re_enter_password.place(x=0,y=230)
            self.tips_re_mail.place(x=40,y=280)
        class_register = RegisterMain(re_username, re_age, re_gender, re_password, re_enter_password, re_mail)   # 实例化
        username_record = class_register.checkUsername()    # 获取检查后的用户名结果
        age_record = class_register.checkAge()     # 获取检查后的年龄结果
        gender_record = class_register.checkGender()     # 获取检查后的性别结果
        password_record = class_register.checkPassword()    # 获取检查后的密码结果
        enter_password_record = class_register.checkEnterPassword()    # 获取检查后的确认密码结果
        mail_record = class_register.checkMail()     # 获取检查后的邮箱结果
        # 用户名结果
        if username_record == None:
            self.tips_re_username['text'] = ""
            self.register_username_entry.config(highlightbackground="black")
        else:
            self.tips_re_username['text'] = username_record
            self.register_username_entry.config(highlightbackground="red")
        # 年龄结果
        if age_record == None:
            self.tips_re_age['text'] = ""
            self.register_age_entry.config(highlightbackground="black")
        else:
            self.tips_re_age['text'] = age_record
            self.register_age_entry.config(highlightbackground="red")
        # 密码结果
        if password_record == None:
            self.tips_re_password['text'] = ""
            self.register_passwod_entry.config(highlightbackground="black")
        else:
            self.tips_re_password['text'] = password_record
            self.register_passwod_entry.config(highlightbackground="red")
        # 确认密码结果
        if enter_password_record == None:
            self.tips_re_enter_password['text'] = ""
            self.register_enter_entry.config(highlightbackground="black")
        else:
            self.tips_re_enter_password['text'] = enter_password_record
            self.register_enter_entry.config(highlightbackground="red")
        # 邮箱结果
        if mail_record == None:
            self.tips_re_mail['text'] = ""
            self.register_mail_entry.config(highlightbackground="black")
        else:
            self.tips_re_mail['text'] = mail_record
            self.register_mail_entry.config(highlightbackground="red")
        # 保存数据
        if len(class_register.db) == 5:
            save = register.RegisterSystem(class_register.db)
            record = save.save()
            if record == None:
                self.register_window.wm_attributes("-topmost", 0)
                tips = messagebox.showinfo("提示", "注册成功!欢迎您 \"{}\"".format(class_register.db['username']))
                if tips == True:
                    self.register_window.wm_attributes("-topmost", 1)
                    self.register_enter_button.config(state=DISABLED)    # 屏蔽提交按钮

    def registerCommand(self):
        try:
            self.change_password_window.destroy()
        except AttributeError:
            pass
        self.register_username_img = PhotoImage(file="images/register_username.png")   # 登录图标
        self.register_password_img = PhotoImage(file="images/register_password.png")
        self.register_age_img = PhotoImage(file="images/age.png")
        self.register_gender_img = PhotoImage(file="images/gender.png")
        self.register_enter_password_img = PhotoImage(file="images/enter_password.png")
        self.register_mail_img = PhotoImage(file="images/mail.png")
        self.register_ok_img = PhotoImage(file="images/register_ok.png")
        self.disabledAllButton()
        self.button_var.set("1")    # 是否点击了这个按钮
        self.register_bg = self.default_bg
        self.register_window = Toplevel(self.root)
        self.root.wm_attributes("-topmost", 0) # 将root窗口的置顶取消
        self.register_window.title("注册")
        self.register_window.wm_attributes("-topmost", 1)   # 置顶这个窗口
        self.w, self.h = 280, 380
        self.x, self.y = (self.ws / 2) - (self.w / 2), (self.hs / 2) - (self.h / 2)  # 在屏幕正中弹出
        self.register_window.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.register_window.maxsize("280", "380")
        self.register_window.minsize("280", "380")
        self.register_window.config(bg=self.register_bg)               #  N:北  下 E:东  右 S:南 下 W:西 左 CENTER:中间 
        self.register_center_frame = Frame(self.register_window,bg=self.default_bg)
        self.register_center_frame.pack(side=TOP)
        left_frame = Frame(self.register_center_frame, bg=self.default_bg, padx=5)    # 左容器
        left_frame.pack(side=LEFT)
        right_frame = Frame(self.register_center_frame, bg=self.default_bg)    # 右容器
        right_frame.pack(side=RIGHT)
        self.register_username_lable = Label(left_frame, image=self.register_username_img, bg=self.default_bg).pack(pady=5)    # 用户名图标 x=30,y=10
        self.register_age_lable = Label(left_frame, image=self.register_age_img, bg=self.default_bg).pack(pady=5)     #　年龄图标 x=30, y=52
        self.register_gender_lable = Label(left_frame, image=self.register_gender_img, bg=self.default_bg).pack(pady=8)    # 性别图标 x=30, y=100
        self.register_password_lable = Label(left_frame, image=self.register_password_img, bg=self.default_bg).pack(pady=0)    # 密码图标 x=30,y=150
        self.register_enter_password_lable = Label(left_frame, image=self.register_enter_password_img, bg=self.default_bg).pack(pady=15)    # 确认密码图标 x=30,y=195
        self.register_mail_lable = Label(left_frame, image=self.register_mail_img, bg=self.default_bg).pack(pady=1)     # 邮箱图标 x=30,y=248
        self.register_username_var = StringVar()    # 用户名的值
        self.register_age_var = StringVar()    # 年龄值
        self.register_gender_var = IntVar()    # 性别值
        self.register_password_var = StringVar()    # 密码值
        self.register_enter_password_var = StringVar()    # 确认密码值
        self.register_mail_var = StringVar()     # 邮箱值
        self.register_username_entry = Entry(right_frame, textvariable=self.register_username_var, font=("Aiarl", 15),relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)    # 用户名输入框
        self.register_username_entry.pack(pady=15)    # x=90,y=16
        self.register_age_entry = Entry(right_frame, textvariable=self.register_age_var, font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)    # 年龄输入框
        self.register_age_entry.pack(pady=10)    # (x=90, y=60
        gender_frame = Frame(right_frame, bg=self.default_bg)    # 性别容器
        gender_frame.pack(pady=13)
        self.register_gender_radiobutton_male = Radiobutton(gender_frame, text="男", variable=self.register_gender_var, value=0,bg=self.default_bg, relief="flat", highlightbackground=self.default_bg)   # 性别选择：男
        self.register_gender_radiobutton_male.pack(side=LEFT, padx=15)    # x=100, y= 108
        self.register_gender_radiobutton_girl = Radiobutton(gender_frame, text="女", variable=self.register_gender_var, value=1, bg=self.default_bg, relief="flat", highlightbackground=self.default_bg)    # 性别选择：女
        self.register_gender_radiobutton_girl.pack(side=RIGHT, padx=15)    # x=200, y=108
        self.register_passwod_entry = Entry(right_frame, textvariable=self.register_password_var, show="*", font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)    # 密码输入框
        self.register_passwod_entry.pack(pady=8)    # x=90,y=160
        self.register_enter_entry = Entry(right_frame, textvariable=self.register_enter_password_var, show="*", font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)    # 确认密码输入框
        self.register_enter_entry.pack(pady=15)    # x=90,y=207
        self.register_mail_entry = Entry(right_frame, textvariable=self.register_mail_var, font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)    # 邮箱输入框
        self.register_mail_entry.pack(pady=10)    # x=90, y=253
        self.register_enter_button = Button(self.register_window, image=self.register_ok_img, bg=self.default_bg, relief="flat", command=self.checkInformatsion)
        if self.osname == "posix":
            self.register_enter_button.pack(side=BOTTOM, pady=2)
        else:
            self.register_enter_button.pack(side=BOTTOM, pady=10)
        self.register_window.protocol("WM_DELETE_WINDOW", self.normarlAllButton)

    def register(self):
        self.register_button = Button(self.root, image=self.register_photo, bg=self.default_bg, relief="flat",command=self.registerCommand)
        self.register_button.place(x=500,y=350)

    def saveChangePassword(self):
        class_find = FindPassword()
        record1 = class_find.checkExists(self.change_password_var.get())
        record2 = class_find.checkExists(self.change_password_entry_var.get())
        if record1 == None:
            self.c_password_entry_tips['text'] = ""
        else:
            self.c_password_entry_tips['text'] = record1
        if record2 == None:
            self.c_password_again_tips['text'] = ""
        else:
            self.c_password_again_tips['text'] = record2
        if record1 == None and record2 == None:
            if self.change_password_var.get() == self.change_password_entry_var.get():
                self.userdata['password'] = self.change_password_entry_var.get()
                print(self.userdata)
            else:
                self.c_password_again_tips['text'] = "两次密码不相同!"

    def changePassword(self):
        self.forget_window.destroy()
        self.change_password_window = Toplevel()
        self.change_password_window.title("Change Password")
        self.change_password_window.wm_attributes("-topmost", 1)   # 置顶这个窗口
        self.w, self.h = 250, 150
        self.x, self.y = (self.ws / 2) - (self.w / 2), (self.hs / 2) - (self.h / 2)    # 在屏幕正中弹出
        self.change_password_window.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.change_password_window.maxsize("250", "150")
        self.change_password_window.minsize("250", "150")
        self.change_password_window.config(bg=self.default_bg)
        change_password_frame = Frame(self.change_password_window, bg=self.default_bg)
        change_password_frame.pack(side=TOP)
        change_password_left_frame = Frame(change_password_frame, bg=self.default_bg)
        change_password_left_frame.pack(side=LEFT, anchor=N, pady=10)
        change_password_right_frame = Frame(change_password_frame, bg=self.default_bg)
        change_password_right_frame.pack(side=TOP, padx=10,pady=10)
        self.c_password_lable = Label(change_password_left_frame, text="密  码", bg=self.default_bg, font=("Aiarl", 12), relief="solid")
        self.c_password_lable.pack(anchor=E, pady=3)
        self.c_password_entry_lable = Label(change_password_left_frame, text="确认密码", bg=self.default_bg, font=("Aiarl", 12), relief="solid")
        self.c_password_entry_lable.pack(pady=20)
        self.change_password_var = StringVar()
        self.change_password_entry_var = StringVar()
        self.c_password_entry = Entry(change_password_right_frame,textvariable=self.change_password_var, show="*", font=("Aiarl", 12), relief="solid", width=12, bg=self.default_bg)
        self.c_password_entry.pack()
        self.c_password_entry_tips = Label(change_password_right_frame, font=("Aiarl", 10), relief="flat", bg=self.default_bg)
        self.c_password_entry_tips.pack()
        self.c_password_again_entry = Entry(change_password_right_frame,textvariable=self.change_password_entry_var, show="*", font=("Aiarl", 12), relief="solid", width=12, bg=self.default_bg)
        self.c_password_again_entry.pack()
        self.c_password_again_tips = Label(change_password_right_frame, font=("Aiarl", 10), relief="flat", bg=self.default_bg)
        self.c_password_again_tips.pack()
        self.c_password_button = Button(self.change_password_window, image=self.find_password_img, relief="flat", bg=self.default_bg, command=self.saveChangePassword)
        self.c_password_button.pack(side=TOP)
        self.login_button.config(state=NORMAL)
        self.forget_button.config(state=NORMAL)
        self.register_button.config(state=NORMAL)
        self.change_button.config(state=NORMAL)
        if self.osname == "posix":
            pass
        else:
            self.exit_buttom.config(state=NORMAL)

    def sendCode(self):
        self.randint_code_var = StringVar()
        get_random = "".join([chr(randint(48, 57)) for i in range(6)])
        print(get_random)
        self.randint_code_var.set(get_random)

    def changeUserInformations(self):
        self.userdata = {}
        resord = FindPassword()
        username_resord = resord.checkUsername(self.find_username_var.get())    # usernmae return resord
        mail_resord = resord.checkMail(self.find_mail_var.get())    # mail return resord
        exists_resord = resord.IsDate()
        if username_resord == None:
            self.find_username_tips['text'] = ""
            # self.find_username_tips.config(highlightbackground="black")
        else:
            self.find_username_tips['text'] = username_resord
            # self.find_username_tips.config(highlightbackground="red")
        if mail_resord == None:
            self.find_mail_tips['text'] = ""
            # self.find_mail_tips.config(highlightbackground="black")
        else:
            self.find_mail_tips['text'] = mail_resord
            # self.find_mail_tips.config(highlightbackground="red")
        if username_resord == None and mail_resord == None:
            if exists_resord == None:
                self.code_tips['text'] = ""
            else:
                self.code_tips['text'] = exists_resord
        # self.changePassword()
        try:
            # print(self.find_code_var.get(), self.randint_code_var.get())
            if self.find_code_var.get() == self.randint_code_var.get():
                self.code_tips['text'] = ""
                self.userdata['username'] = self.find_username_var.get()
                self.userdata['mail'] = self.find_mail_var.get()
                self.changePassword()
            else:
                self.code_tips['text'] = "code error"
        except AttributeError:
            self.code_tips['text'] = "no code"

    def forgetPasswordCommand(self):
        self.find_username_img = PhotoImage(file="images/find_username.png")
        self.find_mail_img = PhotoImage(file="images/find_mail.png")
        self.find_code_img = PhotoImage(file="images/code.png")
        self.find_password_img = PhotoImage(file="images/find_password.png")
        self.disabledAllButton()
        self.button_var.set("2")    # 是否点击了这个按钮
        self.forget_bg = self.default_bg
        self.forget_window = Toplevel(self.root)
        self.root.wm_attributes("-topmost",0)   # 将root窗口的置顶取消
        self.forget_window.title("找回密码")
        self.forget_window.wm_attributes("-topmost", 1)   # 置顶这个窗口
        self.w, self.h = 250, 250
        self.x, self.y = (self.ws / 2) - (self.w / 2), (self.hs / 2) - (self.h / 2)    # 在屏幕正中弹出
        self.forget_window.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.forget_window.maxsize("250", "250")
        self.forget_window.minsize("250", "250")
        self.forget_window.config(bg=self.forget_bg)
        self.forget_center_frame = Frame(self.forget_window, bg=self.default_bg)
        self.forget_center_frame.pack(side=TOP)
        left_frame = Frame(self.forget_center_frame, bg=self.default_bg, padx=5)    # 左容器
        left_frame.pack(side=LEFT)
        right_frame = Frame(self.forget_center_frame, bg=self.default_bg)    # 右容器
        right_frame.pack(side=TOP, pady=15)
        self.find_username_lable = Label(left_frame, image=self.find_username_img, bg=self.default_bg, relief="flat").pack(pady=10)
        self.find_mail_lable = Label(left_frame, image=self.find_mail_img, bg=self.default_bg, relief="flat").pack(pady=10)
        self.find_code = Label(left_frame, image=self.find_code_img, bg=self.default_bg, relief="flat").pack(pady=10)
        self.find_username_var = StringVar()
        self.find_mail_var = StringVar()
        self.find_code_var = StringVar()
        self.find_username_entry = Entry(right_frame, textvariable=self.find_username_var, font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)
        self.find_username_entry.pack(pady=5)
        self.find_username_tips = Label(right_frame, font=("Aiarl", 10), bg=self.default_bg)
        self.find_username_tips.pack()
        self.find_mail_entry = Entry(right_frame, textvariable=self.find_mail_var, font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=15)
        self.find_mail_entry.pack(pady=10)
        self.find_mail_tips = Label(right_frame, font=("Aiarl", 10), bg=self.default_bg)
        self.find_mail_tips.pack()
        self.find_code_entry = Entry(right_frame, textvariable=self.find_code_var, font=("Aiarl", 15), relief="solid", bg=self.default_bg, highlightbackground=self.default_bg, width=6)
        self.find_code_entry.pack(anchor=W ,pady=5)
        self.find_get_code_button = Button(right_frame, text="验证码", bg=self.default_bg, relief="flat", width=5, command=self.sendCode)
        if self.osname == "posix":
            self.find_get_code_button.place(x=100, y=135)
        else:
            self.find_get_code_button.place(x=90,y=120)
        self.code_tips = Label(self.forget_window, font=("Aiarl", 10), bg=self.default_bg,)
        self.find_button = Button(self.forget_window, image=self.find_password_img, relief="flat", bg=self.default_bg, command=self.changeUserInformations)
        if self.osname == "posix":
            self.code_tips.place(x=50,y=185)
            self.find_button.pack(side=BOTTOM, pady=5)
        else:
            self.code_tips.pack(side=TOP)
            self.find_button.pack(side=BOTTOM, pady=5)
        self.forget_window.protocol("WM_DELETE_WINDOW", self.normarlAllButton)

    def forgetPassword(self):
        self.forget_button = Button(self.root, text=self.button_var,image=self.forget_password_photo, bg=self.default_bg, relief="flat", height=15,command=self.forgetPasswordCommand)
        if os.name == "posix":
            self.forget_button.place(x=610, y=320)
            self.forget_button.config(height=28)
        else:
            self.forget_button.place(x=530,y=310)

    def loginCommand(self):
        class_login = LoginMain(self.var_username.get(), self.var_password.get())    # 实例化
        username_record = class_login.checkUsername()
        password_record = class_login.checkPassword()
        self.tips_username = Label(self.root,bg=self.default_bg, width=15)
        self.tips_username.place(x=280, y=245)
        self.tips_password = Label(self.root,bg=self.default_bg, width=15)
        self.tips_password.place(x=280,y=320)
        if username_record == None:
            self.tips_username['text'] = ""
            self.username_entry.config(highlightbackground="black")
        else:
            self.tips_username['text'] = username_record
            self.username_entry.config(highlightbackground="red")    # 高亮边框
        if password_record == None:
            self.tips_password['text'] = ""
            self.password_entry.config(highlightbackground="black")
        else:
            self.tips_password['text'] = password_record
            self.password_entry.config(highlightbackground="red")    # 高亮边框
        if len(class_login.db) == 2:
            record = class_login.searchSQL(class_login.db)
            if record == None:
                tips = messagebox.showinfo("提示", "欢迎回来! \"{}\"".format(class_login.db['username']))
            else:
                self.tips_password['text'] = record
                self.password_entry.config(highlightbackground="red")    # 高亮边框

    def login(self):
        self.var_username = StringVar()
        self.var_password= StringVar()
        self.username_lable = Label(self.root, image=self.username_photo, bg=self.default_bg)
        self.username_lable.place(x=200,y=190)
        self.password_lable = Label(self.root, image=self.password_photo, bg=self.default_bg)
        self.password_lable.place(x=200,y=260)
        self.username_entry = Entry(self.root, show=None, textvariable=self.var_username, bg=self.default_bg, fg="black", font=("Airal", 24), relief="solid")
        self.username_entry.place(x=280,y=200)
        self.password_entry = Entry(self.root, show="*", textvariable=self.var_password, bg=self.default_bg, fg="black", font=("Airal", 24), relief="solid")
        self.password_entry.place(x=280, y=270)
        self.login_button = Button(self.root, image=self.login_photo, bg=self.default_bg, relief="flat",command=self.loginCommand)
        self.login_button.place(x=300,y=350)

    # 选择主题颜色
    def chooserColor(self):
        color_data = colorchooser.askcolor()    # 调用windows的颜色选择器
        self.default_bg = color_data[-1]
        if color_data[-1] == "#000000":    # 太黑了就看不见了~
            messagebox.askokcancel("提示", "选黑色你就看不见呐！")
        else:
            self.root.config(bg=color_data[-1])
            self.change_button.config(bg=color_data[-1])
            self.clock.config(bg=color_data[-1])
            if self.osname == "posix":
                pass
            else:
                self.exit_buttom.config(bg=color_data[-1])
            self.welcomelabe.config(bg=color_data[-1])
            # 登录界面按钮的颜色
            self.username_lable.config(bg=color_data[-1])
            self.password_lable.config(bg=color_data[-1])
            self.username_entry.config(bg=color_data[-1])
            self.password_entry.config(bg=color_data[-1])
            self.login_button.config(bg=color_data[-1])
            self.register_button.config(bg=color_data[-1])
            self.forget_button.config(bg=color_data[-1])
            try:
                self.tips_username.config(bg=color_data[-1])
                # 注册的颜色
                self.register_window.config(bg=color_data[-1])
                self.register_username_lable.config(bg=color_data[-1])
                self.register_age_lable.config(bg=color_data[-1])
                self.register_gender_lable.config(bg=color_data[-1])
                self.register_password_lable.config(bg=color_data[-1])
                self.register_mail_lable.config(bg=color_data[-1])
                self.register_username_entry.config(bg=color_data[-1])
                self.register_gender_radiobutton_male.config(bg=color_data[-1])
                self.register_gender_radiobutton_girl.config(bg=color_data[-1])
                self.register_passwod_entry.config(bg=color_data[-1])
                self.register_enter_entry.config(bg=color_data[-1])
                self.register_mail_entry.config(bg=color_data[-1])
                self.register_enter_button.config(bg=color_data[-1])
                # 找回密码界面颜色
            except AttributeError:
                pass

    def changebg(self):
        self.change_button = Button(self.root,image=self.color_photo,bg=self.default_bg, relief="flat", command=self.chooserColor)
        if self.osname == "posix":
            self.change_button.place(x=1, y=1)
        else:
            self.change_button.place(x=30,y=0)

    # 退出时调用
    def exit_root(self):
        result = messagebox.askokcancel("退出", "确定退出吗？")
        if result == True:
            self.root.quit()
        else:
            pass

    # 退出
    def exitRoot(self):
        self.exit_buttom = Button(self.root, command=self.exit_root, image=self.exit_photo, bg=self.default_bg, relief="flat")
        self.exit_buttom.place(x=1,y=1)

    def get_time(self):
        '''显示当前时间'''
        global time1
        time1 = ''
        time2 = time.strftime('%Y-%m-%d %H:%M:%S')
        # 能动态显示系统时间
        if time2 != time1:
            time1 = time2
            self.clock = Label(self.root, text=time1, font=28, bg=self.default_bg)
            self.clock.configure(text=time2)
            self.clock.place(x=620,y=1)
            self.clock.after(200, self.get_time)

    # main
    def main(self):
        if os.name == "posix":
            self.isPosix()
        self.get_time()
        self.exitRoot()
        self.changebg()
        self.login()
        self.register()
        self.forgetPassword()
        self.root.mainloop()    # 窗口持久化

if __name__ == "__main__":
    run = MainSystem()
    run.main()
