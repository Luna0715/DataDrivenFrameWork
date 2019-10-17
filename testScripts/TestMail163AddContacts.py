#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from util.ParseExcel import ParseExcel
from config.VarConfig import *
from appModules.LoginAction import LoginAction
from appModules.AddContactPersonAction import AddContactPerson
import  traceback
from time import sleep
from util.Log import *

# def testMailLogin():
#     try:
#         #启动Chrome浏览器
#         driver = webdriver.Chrome(executable_path="D:\driver\chromedriver")
#
#         driver.maximize_window()
#         time.sleep(5)
#         #登录163邮箱
#         LoginAction.login(driver,username='Lyazhou715',password="XXX")
#         time.sleep(5)
#         assert "未读邮件" in driver.page_source
#     except Exception as e:
#         raise e
#     finally:
#         #退出浏览器
#         driver.quit()

#创建解析Excel对象
excelObj = ParseExcel()
#将Excel数据文件加载到内存
excelObj.loadWorkBook(dataFilePath)

def LaunchBrowser():
    #创建Chrome浏览器的一个Options实例对象
    chrome_options = Options()
    #向Options实例中添加禁用扩展插件的设置参数项
    chrome_options.add_argument("--disable-extensions")
    #添加屏蔽--ignore-certificate-errors提示信息的设置参数项
    chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    #添加浏览器最大化的设置参数项，一启动就最大化
    chrome_options.add_argument('--start-maximized')
    #启动带有自定义设置的Chrome浏览器
    driver = webdriver.Chrome(executable_path="D:\\driver\\chromedriver",chrome_options = chrome_options)
    # 访问163邮箱首页
    driver.get("https://mail.163.com/")
    sleep(3)
    return driver

def aatest163MailAddContacts():
    logging.info("163邮箱添加联系人数据驱动测试开始...")
    try:
        #根据Excel文件中的sheet名称获取此sheet对象
        userSheet = excelObj.getSheetByName("163账号")
        #获取163账号sheet中是否执行列
        isExecuteUser = excelObj.getColumn(userSheet,account_isExecute)
        #获取163账号sheet中的数据表列
        dataBookColumn = excelObj.getColumn(userSheet,account_dataBook)

        for idx,i in enumerate(isExecuteUser[1:]):
            #循环遍历163账号表中的账号，为需要执行的账号添加联系人
            if i.value == "y":#表示要执行
                #获取第idx+2行的数据
                userRow = excelObj.getRow(userSheet,idx+2)
                #获取第idx+2行中的用户名
                username = userRow[account_username - 1].value
                #获取第idx+2行中的密码
                password = str(userRow[account_password -1].value)
                print(username,password)

                #创建浏览器实例对象
                driver = LaunchBrowser()
                logging.info("启动浏览器，访问163邮箱主页")

                #登录163邮箱
                LoginAction.login(driver,username,password)
                #等待3s，让登录跳转完成，以便正常进行后续操作
                sleep(3)
                try:
                    #断言登录后跳转的页面是否包含“收信”
                    assert "收 信" in driver.page_source
                    logging.info("用户 %s 登录后，断言页面关键字“收信”成功" %username)
                except AssertionError as e:
                    logging.debug("用户 %s 登录后，断言页面关键字“收信”失败，异常信息：%s" %(username,str(traceback.format_exc())))
                #获取为第idx+2行中用户添加的联系人数据表sheet名
                dataBookName = dataBookColumn[idx+1].value
                #获取对应的数据表对象
                datasheet = excelObj.getSheetByName(dataBookName)
                #获取联系人数据表中是否执行列对象
                isExecuteData = excelObj.getColumn(datasheet,contacts_isExecute)
                contactNum = 0#记录添加成功联系人个数
                isExecuteNum = 0#记录需要执行联系人个数
                for id,data in enumerate(isExecuteData[1:]):
                    #循环遍历是否执行添加联系人列，如果被设置为添加，则进行联系人添加操作
                    if data.value =="y":
                        #如果第id+2行的联系人被设置为执行，则isExecuteNum自增1
                        isExecuteNum += 1
                        #获取联系人表第id+2行对象
                        rowContent = excelObj.getRow(datasheet,id+2)
                        #获取了联系人姓名
                        contactPersonName = rowContent[contacts_contactPersonName - 1].value
                        #获取联系人邮箱
                        contactPersonEmail = rowContent[contacts_contactPersonEmail - 1].value
                        #获取是否设置为星标联系人
                        isStar = rowContent[contacts_isStar -1].value
                        #获取联系人手机号
                        contactPersonPhone = rowContent[contacts_contactPersonMobile -1].value
                        #获取联系人备注信息
                        contactPersonComment = rowContent[contacts_contactPersonComment -1].value
                        #添加联系人成功后，断言的关键字
                        assertKeyWord = rowContent[contacts_assertKeyWords -1].value
                        print(contactPersonName,contactPersonEmail,assertKeyWord,contactPersonPhone,contactPersonComment,isStar)
                        #执行新建联系人操作
                        AddContactPerson.add(driver,contactPersonName,contactPersonEmail,isStar,contactPersonPhone,contactPersonComment)
                        sleep(1)
                        logging.info("添加联系人 %s 成功" %contactPersonEmail)
                        #在联系人工作表中写入添加联系人执行时间
                        excelObj.writeCellCurrentTime(datasheet,rowNo=id+2,colsNo=contacts_runtime)
                        try:
                            #断言给定的关键字是否出现在页面中
                            assert assertKeyWord in driver.page_source
                        except AssertionError as e:
                            #断言失败，在联系人工作表中写入添加联系人测试失败信息
                            excelObj.writeCell(datasheet,"faild",rowNo=id+2,colsNo=contacts_testResult,style="red")
                            logging.info("断言关键字 “%s” 失败" %assertKeyWord)
                        else:
                            #断言成功，写入添加联系人成功信息
                            excelObj.writeCell(datasheet,"pass",rowNo=id+2,colsNo=contacts_testResult,style="green")
                            contactNum += 1
                            logging.info("断言关键字 “%s” 成功" %assertKeyWord)
                    else:
                        logging.info("联系人%s被忽略执行" %contactPersonEmail)
                # print("contactNum = %s,isExecuteNum = %s" %(contactNum,isExecuteNum))
                if contactNum == isExecuteNum:
                    #如果成功添加的联系人数与需要添加的联系人数相等，说明给第i个用户添加联系人测试用例执行成功，在163账号工作表中写入成功信息，否则写入失败信息
                    excelObj.writeCell(userSheet,"pass",rowNo=idx + 2,colsNo=account_testResult,style="green")
                    # print("为用户 %s 添加%d 个联系人,测试通过！" %(username,contactNum))
                else:
                    excelObj.writeCell(userSheet,"faild",rowNo=idx+2,colsNo=account_testResult,style="red")
                logging.info("为用户%s添加%d个联系人，%d个成功\n" %(username,isExecuteNum,contactNum))
            else:
                # print("用户 %s 被设置为忽略执行！" %excelObj.getCellOfValue(userSheet,rowNo=idx+2,colsNo=account_username))
                #获取被忽略执行的用户名
                ignoreUserName = excelObj.getCellOfValue(userSheet,rowNo=idx+2,colsNo=account_username)
                logging.info("用户%s被忽略执行\n" %ignoreUserName)
            driver.quit()
    except Exception as e:
        logging.debug("数据驱动框架主程序执行过程发生异常，异常信息为：%s" %str(traceback.format_exc()))

if __name__=="__main__":
    # testMailLogin()
    aatest163MailAddContacts()
    print("登录163邮箱成功")
