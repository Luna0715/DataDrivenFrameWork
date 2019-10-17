#encoding=utf-8
from util.ObjectMap import *
from  util.ParseConfigurationFile import ParseCofigFile

class LoginPage(object):
    def __init__(self,driver):
        self.driver = driver
        self.parseCF = ParseCofigFile()
        self.loginOptions = self.parseCF.getItemsSection("163mail_login")
        # print(self.loginOptions)

    def pwdLoginButton(self):
        try:
            #从定位表达式配置文件中读取定位密码登录按钮的定位方式和表达式
            locateType,locatorExpression = self.loginOptions["loginPage.accountloginbutton".lower()].split(">")
            # 获取登录页面的密码登录按钮页面对象，并返回给调用者
            elementObj = getElement(self.driver,locateType,locatorExpression)
            return elementObj
        except Exception as e:
            raise e

    def switchToFrame(self):
        try:
            #从定位表达式配置文件中读取定位frame的定位方式和定位表达式
            locateType,locatorExpression = self.loginOptions["loginPage.frame".lower()].split(">")
            iframe = getElement(self.driver,locateType,locatorExpression)
            self.driver.switch_to.frame(iframe)
        except Exception as e:
            raise e

    def switchToDefaultFrame(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            raise e

    def userNameObj(self):
        try:
            #从定位表达式配置文件中读取定位用户名输入框的定位方式和表达式
            locaterType,locatorExpression = self.loginOptions["loginPage.username".lower()].split(">")
            #获取登录页面的用户名输入框页面对象，并返回给调用者
            elementObj = getElement(self.driver,locaterType,locatorExpression)
            return elementObj
        except Exception as e:
            raise e

    def passwordObj(self):
        try:
            #从定位表达式配置文件中读取定位密码输入框的定位方式和表达式
            locateType,locatorExpression = self.loginOptions["loginPage.password".lower()].split(">")
            #获取登录页面的密码输入框页面对象，并返回给调用者
            elementObj = getElement(self.driver,locateType,locatorExpression)
            return elementObj
        except Exception as e:
            raise e

    def loginButton(self):
        try:
            #从定位表达式配置文件中读取定位登录按钮的定位方式和表达式
            locateType,locatorExpression = self.loginOptions["loginPage.loginbutton".lower()].split(">")
            #获取登录页面的登录按钮页面对象，并返回给调用者
            elementObj = getElement(self.driver,locateType,locatorExpression)
            return elementObj
        except Exception as e:
            raise e

if __name__=='__main__':
    #测试代码
    from selenium import webdriver
    driver = webdriver.Chrome(executable_path='D:\driver\chromedriver.exe')
    driver.get("https://mail.163.com/")
    import time
    login = LoginPage(driver)
    # 切换登录方式为账号密码登录
    login.pwdLoginButton().click()
    # 切换进frame控件
    login.switchToFrame()
    #输入登录用户名
    login.userNameObj().send_keys('Lyazhou715')
    #输入登录密码
    login.passwordObj().send_keys('XXX')
    login.loginButton().click()
    time.sleep(10)
    login.switchToDefaultFrame()
    assert "未读邮件" in driver.page_source
    driver.quit()