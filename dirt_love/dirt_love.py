import requests, json
from hoshino import Service, R
from hoshino.typing import CQEvent
import hoshino

sv = Service('土味情话生成器', enable_on_default=True, visible=True, help_='''
说什么晚安，听好了，晚上要说我爱你
'''.strip())

apikey = '' # 输入自己的天行apikey,请前往https://www.tianapi.com注册

def get_dirt_love(apikey):
	url = 'http://api.tianapi.com/saylove/index?key=' + apikey
	r = requests.get(url)
	content = r.json()
	if content['code'] == 200:
		tuwei = content['newslist']
		return tuwei[0]['content']
	elif content['code'] == 150:
		alert = '今天冰祈已经想不出新情话了QAQ'
		return alert

@sv.on_fullmatch(('来点情话'))
async def send_dirt_love(bot,ev:CQEvent):
    uid = ev.user_id
    try:
        dirt_love = get_dirt_love(apikey)
        name = ev.sender['nickname']
        dirt_love = dirt_love.replace('XXX', name)
    except Exception as e: 
        hoshino.logger.error(f'土味情话错误：{e}, 请检查')
        dirt_love = f'该功能好像被玩坏了...'
    await bot.send(ev, dirt_love, at_sender = True)
