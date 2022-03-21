import hoshino 
from hoshino import Service, priv, R, util
from hoshino.typing import CQEvent
import random
from hoshino.util import FreqLimiter
from aiocqhttp.message import MessageSegment
from . import GroupFreqLimiter as freq

sv_help = '''
看看谁是那位幸运的天弃之子
'''.strip()

sv = Service('谁是天弃之子', visible = True, enable_on_default = True, help_ = sv_help)

class UsedFlag:
    def __init__(self, flag = 0):
        self.flag = 0

    def check(self, gid):
        if freq.check_reload_group(group_id = gid, _type = 'boolean'):
            return True
        else:
            self.flag = 0
            return False

emmm = f"{R.img('无语.png').cqcode}"
_time = 30 # 冷却时间(秒)
used = UsedFlag()

@sv.on_fullmatch('天弃之子')
async def weather_son_punish(bot, ev):
    gid = ev.group_id
    sid = ev.self_id
    uid = ev.user_id
    self_info = await bot.get_group_member_info(user_id = sid, group_id = gid, no_cache = True)
    role = self_info['role']
    if role == 'member':
        await bot.send(ev, '冰祈不是管理员啦' + emmm)
        return
    if freq.check_reload_group(group_id = gid, _type = 'boolean'): # 整个群的冷却 
        await bot.send(ev, f'唤雷咏唱冷却中...({freq.check_reload_group(gid)}s)')
        return
    await bot.send(ev, f'冰祈咏唱中...')
    freq.set_reload_group(group_id = gid, _time = _time)
    group_info = await bot.get_group_member_list(group_id = gid)
    member_list = [member['user_id'] for member in group_info]
    member_list.remove(sid)
    son = int(random.choice(member_list))
    son_info = await bot.get_group_member_info(user_id = son, group_id = gid, no_cache = True)
    son_nickname = son_info['nickname']
    son_role = son_info['role']
    time = random.randrange(1, 181)
    if role == 'admin':
        if son_role == 'member':
            if random.randrange(101) < 95:
                await bot.set_group_ban(group_id = gid, user_id = son, duration = time)
                await bot.send(ev, f"一道闪电从天降下，劈中了{MessageSegment.at(son)}!")
            else:
                await bot.send(ev, f"一道闪电从天降下，但是{son_nickname}幸运地避开了!")
            return
        if son_role == 'admin':
            await bot.send(ev, f"一道闪电从天降下，但{son_nickname}以管理之力驱散了闪电!")
            return
        if son_role == 'owner':
            await bot.send(ev, f"一道闪电从天降下，但{son_nickname}以群主之力将闪电送回了天上!")
            return
    if role == 'owner':
        if random.randrange(101) < 95:
            await bot.set_group_ban(group_id = gid, user_id = son, duration = time)
            await bot.send(ev, f"一道闪电从天降下，劈中了{MessageSegment.at(son)}!")
        else:
            await bot.send(ev, f"一道闪电从天降下，但是{MessageSegment.at(son)}幸运地避开了!")
        return
