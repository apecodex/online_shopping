# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 下午11:10
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : Register.py
# @Software: PyCharm

import hashlib
try:
    import sql
except ModuleNotFoundError:
    from . import sql

# md5加密)
def get_md5(key):
    return hashlib.md5(key.encode("utf-8")).hexdigest()

class HashMd5():

    def __init__(self,username, password):
        self.salt = "".join([str(ord(i)) for i in username])  # 遍历username并且获取对应的ascii，没学算法，随机生成的没办法保存
        self.password = get_md5(password+self.salt)  # 加盐

class RegisterSystem():

    def __init__(self, db):
        self.username = db['username']
        self.age = db['age']
        self.gender = db['gender']
        self.password = db['password']
        self.mail = db['mail']
        self.db = {}
        self.sql = sql.AdminSQL()

    def saveUsername(self,):
        self.db['username'] = self.username

    def saveAge(self):
        self.db['age'] = self.age

    def saveGender(self):
        self.db["gender"] = self.gender

    def savePassword(self):
        self.db["password"] = self.password

    def saveMail(self):
        self.db["mail"] = self.mail

    def save(self):
        self.saveUsername()
        self.saveAge()
        self.saveGender()
        self.savePassword()
        self.saveMail()
        self.sql.saveUserDB(self.db)
        self.db = {}  # 清空数据
        return None

# r = RegisterSystem("aaaeeeq",12,"0","abc123","14730@qq.com")
# r.save()
# print(HashMd5("aaafff", "abc123").password)