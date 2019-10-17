#encoding=utf-8
from pageObjects.LoginPage import LoginPage

class LoginAction(object):
    def __init__(self):
        print("login...")

    @staticmethod
    def login(driver,username,password):
        try:
            login = LoginPage(driver)
            login.pwdLoginButton().click()
            # 将当前焦点切换到登录模块的frame中，以便能进行后续登录操作
            login.switchToFrame()
            # 输入登录用户名
            login.userNameObj().send_keys(username)
            # 输入登录密码
            login.passwordObj().send_keys(password)
            # 单击登录按钮
            login.loginButton().click()
        except Exception as e:
            raise e

if __name__=="__main__":
    from selenium import webdriver
    import time
    #启动Chrome浏览器
    driver = webdriver.Chrome(executable_path="D:\\driver\\chromedriver")
    #访问163邮箱首页
    driver.get("https://mail.163.com/")
    time.sleep(5)
    LoginAction.login(driver,username='Lyazhou715',password="XXX")
    time.sleep(5)
    driver.quit()