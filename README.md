本模板是使用Python编写的！！！！
仅限于学习使用！！！！！！！！可以用来学习，给女朋友做的玩，不用于任何盈利！！！！！！！！！
（参考了部分别人的代码）（纯小白，大佬轻喷！！！）

#前提先安装Python3.8（百度自己下载去）
 python -m ensurepip --default-pip           #pip的安装
 python -m pip install --upgrade pip         #pip的升级

#安装运行所需要库：
 import time
 import requests
 import json
 import schedule
 import datetime
 from bs4 import BeautifulSoup

#“天气推送模板.py”中的所有：（XXX替换内容XXX）是需要你自己更改为自己所需信息的地方，其他别改!!!!!
#微信公众测试号申请：
https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index
。。。。。。。。。。。更多请查看上面的说明.txt文件

效果图：
![image](https://github.com/user-attachments/assets/4fb289c3-a14b-41cb-bf47-181947d1809c)


关于自动化执行py程序，实现每天定点发送，
说明一下，我这里“天气推送模板.py”是单纯写了一个程序，你运行一次才，能发一次，并不能定时发送
有钱的可以借助服务器，我穷逼借助的GitHub的actions。上面文件里也有提到。
actions中还需要再次查阅一下，你上面写的py程序中的库，所以需要单独把你需要的库单独列出来。（参考：kun.txt）

再次声明！！！
这整个仅是我自己学习使用，可以用来学习，给女朋友做的玩，不用于任何盈利！！！！！！！！！
代码根据自己实际情况进行修改。
