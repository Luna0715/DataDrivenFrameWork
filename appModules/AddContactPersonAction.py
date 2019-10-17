#encoding = utf-8
from pageObjects.HomePage import HomePage
from pageObjects.AddressBookPage import AddressBookPage
import traceback
import time
class AddContactPerson(object):

    def __init__(self):
        print("add contact person")

    @staticmethod
    def add(driver,contactName,contactEmail,isStar,contactPhone,contactComment):
        try:
            #创建主页实例对象
            hp = HomePage(driver)
            #单击通讯录链接
            hp.addressLink().click()
            time.sleep(3)
            #创建添加联系人页实例对象
            apb =AddressBookPage(driver)
            apb.createContactPersonButton().click()
            if contactName:
                #非必填项
                apb.contactPersonName().send_keys(contactName)
            #必填项
            apb.contactPersonEmail().send_keys(contactEmail)
            if isStar == "是":
                #非必填项
                apb.starContacts().click()
            if contactPhone:
                #非必填项
                apb.contactPersonMobile().send_keys(contactPhone)
            if contactComment:
                #非必填项
                apb.contactPersonComment().send_keys(contactComment)
            apb.saveContactPerson().click()
        except Exception as e:
            #打印堆栈异常信息
            print(traceback.print_exc())
            raise e

if __name__ =='__main__':
    from appModules.LoginAction import LoginAction
    from selenium import webdriver
    import time
    #启动Chrome浏览器
    driver = webdriver.Chrome(executable_path="D:\\driver\\chromedriver")
    #访问163邮箱首页
    driver.get("http://mail.163.com")
    driver.maximize_window()
    time.sleep(5)
    LoginAction.login(driver,username='Lyazhou715',password="XXX")
    time.sleep(5)
    AddContactPerson.add(driver,"张三","zs@qq.com","是","","")
    time.sleep(3)
    assert "张三" in driver.page_source
    driver.quit()