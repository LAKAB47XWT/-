#所需要的库
import time
import requests
import json
import schedule
import datetime
from bs4 import BeautifulSoup

#填写自己的测试公众号的参数，也就https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index中的参数。
# 从测试号信息获取
appID = "XXX替换内容XXX"
appSecret = "XXX替换内容XXX"

#收信人ID即 用户列表中的微信号，可以加入多个
#格式参考，openId_list = ["openIDA","openIDB"]
openId_list = ["XXX替换内容XXX"]

# 天气预报模板ID，每换一个新的模板都需要再修改模板ID
weather_template_id = "XXX替换内容XXX"


#以下到结束是具体代码区域！！！！！！！！
def get_weather(my_city):
    # 爬取天气  勿动！！！！！！！！！
    urls = [
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml"
    ]
    for url in urls:
        resp = requests.get(url)
        text = resp.content.decode("utf-8")
        soup = BeautifulSoup(text, 'html5lib')
        div_conMidtab = soup.find("div", class_="conMidtab")
        tables = div_conMidtab.find_all("table")
        for table in tables:
            trs = table.find_all("tr")[2:]
            for index, tr in enumerate(trs):
                tds = tr.find_all("td")
                # 这里倒着数，因为每个省会的td结构跟其他不一样
                city_td = tds[-8]
                this_city = list(city_td.stripped_strings)[0]
                if this_city == my_city:
                    high_temp_td = tds[-5]
                    low_temp_td = tds[-2]
                    weather_type_day_td = tds[-7]
                    weather_type_night_td = tds[-4]
                    wind_td_day = tds[-6]
                    wind_td_day_night = tds[-3]

                    high_temp = list(high_temp_td.stripped_strings)[0]
                    low_temp = list(low_temp_td.stripped_strings)[0]
                    weather_typ_day = list(weather_type_day_td.stripped_strings)[0]
                    weather_type_night = list(weather_type_night_td.stripped_strings)[0]

                    wind_day = list(wind_td_day.stripped_strings)[0] + list(wind_td_day.stripped_strings)[1]
                    wind_night = list(wind_td_day_night.stripped_strings)[0] + list(wind_td_day_night.stripped_strings)[1]

                    # 如果没有白天的数据就使用夜间的
                    temp = f"{low_temp}——{high_temp}摄氏度" if high_temp != "-" else f"{low_temp}摄氏度"
                    weather_typ = weather_typ_day if weather_typ_day != "-" else weather_type_night
                    wind = f"{wind_day}" if wind_day != "--" else f"{wind_night}"
                    return this_city, temp, weather_typ, wind

def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token

def get_daily_love():
   # 每日一句情话，直接不要输出，情侣建议不要加这个，请不要问为什么，最后输出的时候，不要输出这个就行，无需注释，否则可能会影响程序完整运行。
    url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
    r = requests.get(url)
    all_dict = json.loads(r.text)
    sentence = all_dict['returnObj'][0]
    daily_love = sentence
    return daily_love

def generate_dressing_advice(avg_temp, weather_type):
    # 根据平均温度和天气类型给出穿衣建议(话不能太长否则微信端输出，可能无法全部输出完，有字数限制)
    advice = ""
    if avg_temp >= 30:
        advice += "非常热，建议穿轻薄透气的衣服。"        #可以改
    elif 20 <= avg_temp < 30:
        advice += "气温适中，可以选择穿着衬衫和牛仔裤。"           #可以改
    elif 10 <= avg_temp < 20:
        advice += "气温较凉爽，建议穿上长袖衣服和外套。"          #可以改
    elif 0 <= avg_temp < 10:
        advice += "气温较低，建议穿上厚外套，带帽子和手套。"             #可以改
    else:
        advice += "气温非常低，建议穿上羽绒服。"              #可以改
    return advice

def generate_travel_advice(weather_type):
    # 根据天气类型给出额外建议(话不能太长否则微信端输出，可能无法全部输出完，有字数限制)
    advice = ""
    if "雨" in weather_type or "雪" in weather_type:
        advice += "请注意带伞或雨具，雨天湿滑记得注意安全呀！！！！"             #可以改
    elif "雾" in weather_type or "霾" in weather_type:
        advice += "空气质量较差，减少户外活动，必要时佩戴口罩。"         #可以改
    elif "晴" in weather_type:
        advice += "天气晴朗，记得防晒哟，宝贝。"           #可以改
    elif "阴" in weather_type:
        advice += "天气阴沉，建议携带雨具以防突然下雨。"                   #可以改
    return advice

def send_weather(access_token, weather):
    # touser 就是 openID
    # template_id 就是模板ID
    # url 就是点击模板跳转的url
    # data就按这种格式写，time和text就是之前{{time.DATA}}中的那个time，value就是你要替换DATA的值

    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    calculator = BirthdayCalculator(2000, 1, 01)  # BirthdayCalculator(XXXX, X, XX)定义生日的日期

    try:
        low_temp, high_temp = map(int, weather[1][:-3].split('——'))
    except ValueError:
        # 单一温度格式处理
        temp_value = int(weather[1][:-3])
        low_temp = temp_value
        high_temp = temp_value

    avg_temp = (low_temp + high_temp) / 2
    dressing_advice = generate_dressing_advice(avg_temp, weather[2])
    travel_advice = generate_travel_advice(weather[2])

    for openId in openId_list:
        body = {
            "touser": openId.strip(),
            "template_id": weather_template_id.strip(),
            "url": "http://www.nmc.cn/publish/forecast/AJS/",
             #更多信息点进去的网站
        #以下是输出的内容，必须和你模板一致，否则会出现运行，但是没有输出你要的参数。
            "data": {
                "date": {
                    "value": today_str
                },
                "region": {
                    "value": weather[0]
                },
                "weather": {
                    "value": weather[2]
                },
                "temp": {
                    "value": weather[1]
                },
                "wind_dir": {
                    "value": weather[3]
                },
                "today_note": {
                    "value": get_daily_love()
                },
                "zhouji": {
                    "value": get_date()
                },
                "birthday1": {
                    "value": calculator.get_herbirthday()
                },
                "love_day": {
                    "value": get_loveday()
                },
                "dressing_advice": {  # 新增穿衣建议字段
                    "value": dressing_advice
                },
                "travel_advice": {  # 新增出行建议字段
                    "value": travel_advice
                }
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
        print(requests.post(url, json.dumps(body)).text)

def weather_report(city):
    # 1. 获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather(city)
    print(f"天气信息： {weather}")
    # 3. 发送消息
    send_weather(access_token, weather)

def timetable(message):
    # 1. 获取access_token
    access_token = get_access_token()
    # 3. 发送消息
    send_timetable(access_token, message)

def get_date():
    """
    这些都是datetime库中的用法
    若零基础可以去python的开发文档中查阅
    """

    sysdate = datetime.date.today()  # 只获取日期
    now_time = datetime.datetime.now()  # 获取日期加时间
    week_day = sysdate.isoweekday()  # 获取周几
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    return week[week_day - 1]
    #这个是输出具体星期几


class BirthdayCalculator:
    def __init__(self, birth_year, birth_month, birth_day):
        self.birth_date = datetime.date(birth_year, birth_month, birth_day)

    def get_herbirthday(self):
        """
        获取宝贝的生日，计算距离下一次生日的天数
        """
        today = datetime.date.today()  # 获取现在时间信息
        herbirthDay = datetime.date(today.year, self.birth_date.month, self.birth_date.day)

        if herbirthDay > today:  # 如果ta的生日日期比今天靠后则直接计算这两天的序号之差
            difference = herbirthDay - today
            return f"距离bb生日,还有 {difference.days} 天。"
        elif herbirthDay < today:  # 如果ta的生日日期比今天靠前则给ta的生日加上一年再计算这两天的序号之差
            herbirthDay = herbirthDay.replace(year=today.year + 1)
            difference = herbirthDay - today
            return f"距离bb生日,还有 {difference.days} 天。"
        else:
            return '生日快乐bb！！'

def get_loveday():
    """用法同上"""
    today = datetime.datetime.now()
    oneDay = datetime.date(2010, 1, 01)  # datetime.date(xxxx,x,xx)  你们纪念日的日期
    d = today.toordinal() - oneDay.toordinal()
    return (" %d 天。\n%d 年 %d 个月 %d 天。\n%d 个月 %d 天。\n%d 周 %d 天。" % (
        d, d // 365, (d % 365) // 30, (d % 365) % 30, d // 30, d % 30, d // 7, d % 7))

if __name__ == '__main__':
    weather_report("南京")
    # 具体地区，天气推送也是按照这个来的，可以修改
