import hoshino 
from hoshino import Service, priv, R, util
from hoshino.typing import CQEvent
import random
from hoshino.util import FreqLimiter
from aiocqhttp.message import MessageSegment

sv_help = '''
看看谁是那位幸运的天弃之子
'''.strip()

sv = Service('谁是天弃之子', visible = True, enable_on_default = True, help_ = sv_help)

_flmt = FreqLimiter(30)

@sv.on_fullmatch('天弃之子')
async def weather_son_punish(bot, ev):
    gid = ev.group_id
    sid = ev.self_id
    self_info = await bot.get_group_member_info(user_id = sid, group_id = gid)
    role = self_info['role']
    if role == 'member':
        await bot.send(ev, '我不是管理员啦')
        return
    if not _flmt.check(gid):
        await bot.send(ev, f'唤雷咏唱冷却中...({round(_flmt.left_time(gid))}s)')
        return
    await bot.send(ev, f'bot咏唱中...')
    group_info = await bot.get_group_member_list(group_id = gid)
    member_list = [member['user_id'] for member in group_info]
    member_list.remove(sid)
    son = int(random.choice(member_list))
    son_info = await bot.get_group_member_info(user_id = son, group_id = gid)
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
            _flmt.start_cd(gid)
            return
        if son_role == 'admin':
            await bot.send(ev, f"一道闪电从天降下，但{son_nickname}以管理之力驱散了闪电!")
            _flmt.start_cd(gid)
            return
        if son_role == 'owner':
            await bot.send(ev, f"一道闪电从天降下，但{son_nickname}以群主之力将闪电送回了天上!")
            _flmt.start_cd(gid)
            return
    if role == 'owner':
        if random.randrange(101) < 95:
            await bot.set_group_ban(group_id = gid, user_id = son, duration = time)
            await bot.send(ev, f"一道闪电从天降下，劈中了{MessageSegment.at(son)}!")
        else:
            await bot.send(ev, f"一道闪电从天降下，但是{MessageSegment.at(son)}幸运地避开了!")
        _flmt.start_cd(gid)
        return
