# SelectorToXpath
## css转换成xpath，用于selenium自动化测试等对HTML操作  
-----------------------------------------------------------------------------------------------
### 转换说明：
####            直接子元素                 
                Xpath:          //div/a                                             
                CSS Path:       div > a

####            子元素或后代元素                                                      
                Xpath:          //div//a 
                CSS Path:       div a
                
####            以id定位                                           
                Xpath:          //div[@id=’idValue’]//a   
                CSS Path:       div#idValue a

####            以class定位                                  
                Xpath:          //div[@class=’classValue’]//a   
                CSS Path:       div.classValue a

####            同级弟弟元素                     
                Xpath:          //ul/li[@class=’first’]/following-sibling::li
                CSS Path:       ul>li.first + li

####            属性                                           
                Xpath:          //form/input[@name=’username’]  
                CSS Path:       form input[name=’username’]

####            多个属性                         
                Xpath:          //input[@name=’continue’ and @type=‘button’] 
                CSS Path:       input[name=’continue’][type=’button’]

####            第4个子元素                                             
                Xpath:          //ul[@id=’list’]/li[4]
                CSS Path:       ul#list li:nth-child(4)

####            第1个子元素                                            
                Xpath:          //ul[@id=’list’]/li[1] 
                CSS Path:       ul#list li:first-child

####            最后1个子元素                                       
                Xpath:          //ul[@id=’list’]/li[last()]
                CSS Path:       ul#list li:last-child

####            属性包含某字段                                  
                Xpath:          //div[contains(@title,’Title’)]
                CSS Path:       div[title*=”Title”]

####            属性以某字段开头                             
                Xpath:          //input[starts-with(@name,’user’)]
                CSS Path:       input[name^=”user”]

####            属性以某字段结尾                              
                Xpath:          //input[ends-with(@name,’name’)]
                CSS Path:       input[name$=”name”]

####            text中包含某字段                                
                Xpath:          //div[contains(text(), ‘text’)]
                CSS Path:       无法定位

####            元素有某属性                                                      
                Xpath:          //div[@title]
                CSS Path:       div[title]

####            父节点                                                               
                Xpath:          //div/.. 
                CSS Path:       无法定位

####            同级哥哥节点                                    
                Xpath:          //li/preceding-sibling::div[1]
                CSS Path:       无法定位
-----------------------------------------------------------------------------------------------
### 脚本说明：

#### parser.out 与 parsetab.py 为自动生成的文件

#### selector_to_xpath.py 为执行文件

#### 脚本中的ply包可以通过 pip install ply 安装

#### PLY (Python Lex-Yacc) 使用说明请参考： https://github.com/dabeaz/ply
-----------------------------------------------------------------------------------------------
