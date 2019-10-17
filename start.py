#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#创建Chrome浏览器的实例
driver = webdriver.Chrome(executable_path="D:\\driver\\chromedriver")
#最大化浏览器窗口
driver.maximize_window()
#访问163邮箱登录页面
driver.get("https://mail.163.com/")
#切换登录方式为账号密码登录
driver.find_element_by_id("switchAccountLogin").click()
#切换进frame控件
iframe = driver.find_element_by_xpath('//div[@id="loginDiv"]//iframe')
driver.switch_to.frame(iframe)
#获取用户名输入框
userName = driver.find_element_by_xpath('//input[@name="email"]')
#输入用户名
userName.send_keys('Lyazhou715')
#获取密码输入框
pwd = driver.find_element_by_xpath('//input[@name="password"]')
#输入密码
pwd.send_keys('xxx')
#发送一个回车键
pwd.send_keys(Keys.RETURN)
#等待10s，以便登录成功后的页面加载完成
time.sleep(10)
#单击“通讯录”按钮
driver.find_element_by_id("_mail_tabitem_1_4text").click()
time.sleep(2)
#单击“新建联系人”按钮
driver.find_element_by_xpath("//span[text()='新建联系人']").click()
time.sleep(2)
#输入联系人姓名
driver.find_element_by_xpath('//a[@title="编辑详细姓名"]/preceding-sibling::div/input').send_keys("lbb")
time.sleep(2)
#输入联系人电子邮箱
driver.find_element_by_xpath('//*[@id="iaddress_MAIL_wrap"]//input').send_keys("1512663577@qq.com")
driver.find_element_by_xpath("//span[text()='设为星标联系人']/preceding-sibling::span/b").click()
time.sleep(2)
#输入联系人手机号
driver.find_element_by_xpath("//*[@id='iaddress_TEL_wrap']//input").send_keys("16666666666")
time.sleep(2)
#输入备注信息
driver.find_element_by_xpath("//textarea").send_keys("朋友")
time.sleep(2)
#单击“确认”按钮
driver.find_element_by_xpath('//span[text()="确 定"]').click()
time.sleep(5)

driver.quit()