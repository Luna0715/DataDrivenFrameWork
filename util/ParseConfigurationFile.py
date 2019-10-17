#encoding=utf-8
from configparser import ConfigParser
from config.VarConfig import pageElementLocatorPath

class ParseCofigFile(object):

    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read(pageElementLocatorPath,encoding="utf-8")

    def getItemsSection(self,sectionName):
        #获取配置文件中指定section下的所有option键值对，并以字典类型返回给调用者
        """注意：使用self.cf.items(sectionName)此种方法获取到的配置文件中的options内容均被转换成小写,比如,loginPage.frame被转换成了loginpage.frame"""
        optionsDict = dict(self.cf.items(sectionName))
        return optionsDict

    def getOptionValue(self,sectionName,optionName):
        #获取指定section下的指定option的值
        value = self.cf.get(sectionName,optionName)
        return value

if __name__=='__main__':
    pc = ParseCofigFile()
    print(pc.getItemsSection("163mail_login"))
    print(pc.getOptionValue("163mail_login","loginPage.frame"))