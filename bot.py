#!/usr/bin/python
'''
https://bangumi.github.io/api/
'''

import json
import telebot
import requests
import datetime

from config import BOT_TOKEN, APP_ID, APP_SECRET, WEBSITE_BASE, BOT_USERNAME

# 请求TG Bot api
bot = telebot.TeleBot(BOT_TOKEN)

# 检测命令
@bot.message_handler(commands=['start'])
def send_start(message):
    if message.chat.type == "private": # 当私人聊天
        test_id = message.from_user.id
        if data_seek_get(test_id) == 'yes':
            bot.send_message(message.chat.id, "已绑定", timeout=20)
        else:
            text = {'请绑定您的Bangumi'}
            url= f'{WEBSITE_BASE}oauth_index?tg_id={test_id}'
            markup = telebot.types.InlineKeyboardMarkup()    
            markup.add(telebot.types.InlineKeyboardButton(text='绑定Bangumi',url=url))
            bot.send_message(message.chat.id, text=text, parse_mode='Markdown', reply_markup=markup ,timeout=20)
    else:
        bot.send_message(message.chat.id, '请私聊我进行Bangumi绑定', parse_mode='Markdown' ,timeout=20)

# 查询 Bangumi 用户收藏统计
@bot.message_handler(commands=['my'])
def send_my(message):
    test_id = message.from_user.id
    if data_seek_get(test_id) == 'no':
        bot.send_message(message.chat.id, "未绑定Bangumi，请私聊使用[/start](https://t.me/"+BOT_USERNAME+"?start=none)进行绑定", parse_mode='Markdown', timeout=20)
    else:
        bot.send_message(message.chat.id, "正在查询请稍后...", reply_to_message_id=message.message_id, parse_mode='Markdown', timeout=20)
        access_token = user_data_get(test_id).get('access_token')
        params = {'app_id': APP_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Authorization': 'Bearer ' + access_token}

        url = 'https://api.bgm.tv/user/' + str(user_data_get(test_id).get('user_id')) + '/collections/status'
        r = requests.get(url=url, params=params, headers=headers)
        startus_data = json.loads(r.text)
        if startus_data == None:
            bot.delete_message(message.chat.id, message_id=message.message_id+1, timeout=20)
            bot.send_message(message.chat.id, text='您没有观看记录，快去bgm上点几个格子吧~', parse_mode='Markdown', timeout=20)
        else:
            book = None
            book_do = 0
            book_collect = 0
            for i in startus_data:
                if i.get('name') == 'book':
                    book = i.get('collects')
                    for i in book:
                        if i.get('status').get('type') == 'do':
                            book_do = i.get('count')
                        if i.get('status').get('type') == 'collect':
                            book_collect = i.get('count')
            anime = None
            anime_do = 0
            anime_collect = 0
            for i in startus_data:
                if i.get('name') == 'anime':
                    anime = i.get('collects')
                    for i in anime:
                        if i.get('status').get('type') == 'do':
                            anime_do = i.get('count')
                        if i.get('status').get('type') == 'collect':
                            anime_collect = i.get('count')
            music = None
            music_do = 0
            music_collect = 0
            for i in startus_data:
                if i.get('name') == 'music':
                    music = i.get('collects')
                    for i in music:
                        if i.get('status').get('type') == 'do':
                            music_do = i.get('count')
                        if i.get('status').get('type') == 'collect':
                            music_collect = i.get('count')
            game = None
            game_do = 0
            game_collect = 0
            for i in startus_data:
                if i.get('name') == 'game':
                    game = i.get('collects')
                    for i in game:
                        if i.get('status').get('type') == 'do':
                            game_do = i.get('count')
                        if i.get('status').get('type') == 'collect':
                            game_collect = i.get('count')

            text = {'*Bangumi 用户数据统计：\n\n'+ 
                    nickname_data(test_id) +'*\n'
                    '➤ 动画：`'+ str(anime_do) +'在看，'+ str(anime_collect) +'看过`\n'
                    '➤ 图书：`'+ str(book_do)  +'在读，'+ str(book_collect)  +'读过`\n'
                    '➤ 音乐：`'+ str(music_do) +'在听，'+ str(music_collect) +'听过`\n'
                    '➤ 游戏：`'+ str(game_do)  +'在玩，'+ str(game_collect)  +'玩过`\n\n'

                    '[🏠 个人主页](https://bgm.tv/user/'+ str(user_data_get(test_id).get('user_id')) +')\n'
                    }
            
            img_url = 'https://bgm.tv/chart/img/' + str(user_data_get(test_id).get('user_id'))

            bot.delete_message(message.chat.id, message_id=message.message_id+1, timeout=20)
            bot.send_photo(chat_id=message.chat.id, photo=img_url, caption=text, parse_mode='Markdown')
            # bot.send_message(message.chat.id, text=text, parse_mode='Markdown', timeout=20)

# 查询 Bangumi 用户在看动画
@bot.message_handler(commands=['anime'])
def send_anime(message):
    test_id = message.from_user.id
    if data_seek_get(test_id) == 'no':
        bot.send_message(message.chat.id, "未绑定Bangumi，请私聊使用[/start](https://t.me/"+BOT_USERNAME+"?start=none)进行绑定", parse_mode='Markdown', timeout=20)
    else:
        bot.send_message(message.chat.id, "正在查询请稍后...", reply_to_message_id=message.message_id, parse_mode='Markdown', timeout=20)
        access_token = user_data_get(test_id).get('access_token')
        params = {'app_id': APP_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Authorization': 'Bearer ' + access_token}

        url = 'https://api.bgm.tv/user/' + str(user_data_get(test_id).get('user_id')) + '/collections/anime'
        try:
            r = requests.get(url=url, params=params, headers=headers)
        except requests.ConnectionError:
            r = requests.get(url=url, params=params, headers=headers)
        anime_data = json.loads(r.text)

        if anime_data == None:
            bot.delete_message(message.chat.id, message_id=message.message_id+1, timeout=20)
            bot.send_message(message.chat.id, text='您没有观看记录，快去bgm上点几个格子吧~', parse_mode='Markdown', timeout=20)
        else:
            anime = None
            anime_do_list = None
            anime_count = 0
            subject_id_li = None
            subject_data_li = None
            for i in anime_data:
                if i.get('name') == 'anime':
                    anime = i.get('collects')
                    for i in anime:
                        if i.get('status').get('type') == 'do':
                            anime_count = i.get('count')
                            anime_do_list = i.get('list')
                            for i in anime_do_list:
                                subject_id_li = [i['subject_id'] for i in anime_do_list]
                                subject_data_li = [i['subject']['name_cn'] for i in anime_do_list]
            
            if subject_id_li and subject_data_li == None:
                bot.delete_message(message.chat.id, message_id=message.message_id+1, timeout=20)
                bot.send_message(message.chat.id, text='出错啦，用于您的隐私设置我无法获取到您的在看', parse_mode='Markdown', timeout=20)
            else:    
                markup = telebot.types.InlineKeyboardMarkup()
                for item in list(zip(subject_data_li,subject_id_li)):
                    markup.add(telebot.types.InlineKeyboardButton(text=item[0],callback_data=str(test_id)+'subject_id'+str(item[1])))

                eps_li = [eps_get(test_id, subject_id)['watched'] for subject_id in subject_id_li]

                anime_data = ''.join([a +' `['+ b +']`\n\n' for a,b in zip(subject_data_li,eps_li)])

                text = {'*'+ nickname_data(test_id) +' 在看的动画*\n\n'+
                        anime_data +
                        '共'+ str(anime_count) +'部'}

                bot.delete_message(message.chat.id, message_id=message.message_id+1, timeout=20)
                bot.send_message(message.chat.id, text=text, parse_mode='Markdown', reply_markup=markup , timeout=20)

# 判断是否绑定Bangumi
def data_seek_get(test_id):
    with open('bgm_data.json') as f:                        # 打开文件
        data_seek = json.loads(f.read())                    # 读取
    data_li = [i['tg_user_id'] for i in data_seek]          # 写入列表
    if int(test_id) in data_li:                             # 判断列表内是否有被验证的UID
        data_back = 'yes'
    else:
        data_back = 'no'
    return data_back

# 获取用户数据
def user_data_get(test_id):
    with open('bgm_data.json') as f:
        data_seek = json.loads(f.read())
    user_data = None
    for i in data_seek:
        if i.get('tg_user_id') == test_id:
            expiry_time = i.get('expiry_time')
            now_time = datetime.datetime.now().strftime("%Y%m%d")
            if now_time >= expiry_time:   # 判断密钥是否过期
                user_data = expiry_data_get(test_id)
            else:
                user_data = i.get('data',{})
    return user_data

# 更新过期用户数据
def expiry_data_get(test_id):
    with open('bgm_data.json') as f:
        data_seek = json.loads(f.read())
    refresh_token = None
    for i in data_seek:
        if i.get('tg_user_id') == test_id:
            refresh_token = i.get('data',{}).get('refresh_token')
    CALLBACK_URL = f'{WEBSITE_BASE}oauth_callback'
    resp = requests.post(
        'https://bgm.tv/oauth/access_token',
        data={
            'grant_type': 'refresh_token',
            'client_id': APP_ID,
            'client_secret': APP_SECRET,
            'refresh_token': refresh_token,
            'redirect_uri': CALLBACK_URL,
        },
        headers = {
        "User-Agent": "",
        }
    )
    access_token = json.loads(resp.text).get('access_token')    #更新access_token
    refresh_token = json.loads(resp.text).get('refresh_token')  #更新refresh_token
    expiry_time = (datetime.datetime.now()+datetime.timedelta(days=7)).strftime("%Y%m%d")#更新过期时间
    
    # 替换数据
    if access_token or refresh_token != None:
        with open("bgm_data.json", 'r+', encoding='utf-8') as f:
            data = json.load(f)
            for i in data:
                if i['tg_user_id'] == test_id:
                    i['data']['access_token'] = access_token
                    i['data']['refresh_token'] = refresh_token
                    i['expiry_time'] = expiry_time
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()
    
    # 读取数据
    with open('bgm_data.json') as f:
        data_seek = json.loads(f.read())
    user_data = None
    for i in data_seek:
        if i.get('tg_user_id') == test_id:
            user_data = i.get('data',{})
    return user_data

# 获取用户昵称
def nickname_data(test_id):
    access_token = user_data_get(test_id).get('access_token')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}
    url = 'https://api.bgm.tv/user/' + str(user_data_get(test_id).get('user_id'))
    try:
        r = requests.get(url=url, headers=headers)
    except requests.ConnectionError:
        r = requests.get(url=url, headers=headers)

    nickname = json.loads(r.text).get('nickname')
    return nickname

# 获取用户观看eps
def eps_get(test_id, subject_id):
    access_token = user_data_get(test_id).get('access_token')
    params = {
        'subject_id': subject_id,
        'type': 0}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}
    url = 'https://api.bgm.tv/v0/episodes'

    try:
        r = requests.get(url=url, params=params, headers=headers)
    except requests.ConnectionError:
        r = requests.get(url=url, params=params, headers=headers)

    data_eps = json.loads(r.text).get('data')
    epsid_li = [i['id'] for i in data_eps] # 所有eps_id

    params = {
        'subject_id': subject_id}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}
    url = 'https://api.bgm.tv/user/' + str(user_data_get(test_id).get('user_id')) + '/progress'
    try:
        r = requests.get(url=url, params=params, headers=headers)
    except requests.ConnectionError:
        r = requests.get(url=url, params=params, headers=headers)
    
    try:
        data_watched = json.loads(r.text).get('eps')
    except AttributeError:
        watched_id_li = [0] # 已观看 eps_id
    else:
        watched_id_li = [i['id'] for i in data_watched] # 已观看 eps_id

    eps_n = len(set(epsid_li)) # 总集数
    watched_n = len(set(epsid_li) & set(watched_id_li)) # 已观看了集数
    
    unwatched_id = list(set(epsid_li) - set(watched_id_li))

    # 输出
    eps_data = {'watched': str(watched_n) + '/' + str(eps_n),
                'watch': str(watched_n),
                'unwatched_id': unwatched_id}

    return eps_data

# 剧集信息获取
def subject_info_get(test_id, subject_id):
    access_token = user_data_get(test_id).get('access_token')
    params = {
        'responseGroup': 'large'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}
    url = f'https://api.bgm.tv/subject/{subject_id}'

    try:
        r = requests.get(url=url, params=params, headers=headers)
    except requests.ConnectionError:
        r = requests.get(url=url, params=params, headers=headers)
    
    info_data = json.loads(r.text)
    
    name = info_data.get('name') # 剧集日文名
    name_cn = info_data.get('name_cn') # 剧集中文名
    air_date = info_data.get('air_date') # 放送开始日期
    air_weekday = str(info_data.get('air_weekday')).replace('1', '星期一').replace('2', '星期二').replace('3', '星期三').replace('4', '星期四').replace('5', '星期五').replace('6', '星期六').replace('7', '星期日') # 放送日期
    score = info_data.get('rating').get('score') # 评分
    # 输出
    subject_info_data = {'name' : name,
                         'name_cn': name_cn,
                         'air_date': air_date,
                         'air_weekday': air_weekday,
                         'score': score}
    return subject_info_data

# 更新收视进度为看过
def eps_status_get(test_id, eps_id):
    access_token = user_data_get(test_id).get('access_token')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}

    url = f'https://api.bgm.tv/ep/{eps_id}/status/watched'

    r = requests.get(url=url, headers=headers)
    
    return r

# 更新收藏状态
def collection_post(test_id, subject_id, status, rating):
    access_token = user_data_get(test_id).get('access_token')
    params = {"status": (None, status),"rating": (None, rating)}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}

    url = f'https://api.bgm.tv/collection/{subject_id}/update'

    r = requests.post(url=url, files=params, headers=headers)

    return r

# 获取用户评分
def user_rating_get(test_id, subject_id):
    access_token = user_data_get(test_id).get('access_token')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Authorization': 'Bearer ' + access_token}

    url = f'https://api.bgm.tv/collection/{subject_id}'

    r = requests.get(url=url, headers=headers)
    user_rating_data = json.loads(r.text)
    user_rating = user_rating_data.get('rating')

    return user_rating

# 动画简介图片获取
def anime_img(test_id, subject_id):
    anime_name = subject_info_get(test_id, subject_id)['name']
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search) {
                id
                title {
                    romaji
                }
            }
        }
    }
    '''
    variables = {
        'search': anime_name,
        'page': 1,
        'perPage': 1
    }
    url = 'https://graphql.anilist.co'
    try:
        r = requests.post(url, json={'query': query, 'variables': variables})
    except requests.ConnectionError:
        r = requests.post(url, json={'query': query, 'variables': variables})
    
    anilist_data = json.loads(r.text).get('data').get('Page').get('media')
    anilist_id = [i['id'] for i in anilist_data][0]
    
    img_url = f'https://img.anili.st/media/{anilist_id}'

    return img_url

# 回调数据查询
@bot.callback_query_handler(func=lambda call: True)
def callback_handle(call):
    call_data = call.data
    tg_from_id = call.from_user.id

    # 动画再看详情
    if 'subject_id' in call_data:
        test_id = int(call_data.split('subject_id')[0])
        if tg_from_id == test_id:
            subject_id = call_data.split('subject_id')[1]
            img_url = anime_img(test_id, subject_id)

            text = {'*'+ subject_info_get(test_id, subject_id)['name_cn'] +'*\n\n'

                    'BGM ID：`' + str(subject_id) + '`\n'
                    '➤ BGM 平均评分：`'+ str(subject_info_get(test_id, subject_id)['score']) +'`🌟\n'
                    '➤ 您的评分：`'+ str(user_rating_get(test_id, subject_id)) +'`🌟\n'
                    '➤ 放送开始：`'+ subject_info_get(test_id, subject_id)['air_date'] + '`\n'
                    '➤ 放送星期：`'+ subject_info_get(test_id, subject_id)['air_weekday'] + '`\n'
                    '➤ 观看进度：`'+ eps_get(test_id, subject_id)['watched'] + '`\n\n'
                    
                    '💬 [吐槽箱](https://bgm.tv/subject/'+ str(subject_id) +'/comments)\n'}

            markup = telebot.types.InlineKeyboardMarkup()
            unwatched_id = eps_get(test_id, subject_id)['unwatched_id']
            if unwatched_id == []:
                markup.add(telebot.types.InlineKeyboardButton(text='返回',callback_data=str(test_id)+'anime_back'+str(subject_id)),telebot.types.InlineKeyboardButton(text='评分',callback_data=str(test_id)+'rating0'))
            else:    
                markup.add(telebot.types.InlineKeyboardButton(text='返回',callback_data=str(test_id)+'anime_back'+str(subject_id)),telebot.types.InlineKeyboardButton(text='评分',callback_data=str(test_id)+'rating0'),telebot.types.InlineKeyboardButton(text='已看最新',callback_data=str(test_id)+'anime_eps'+str(unwatched_id[0])))
            bot.delete_message(chat_id=call.message.chat.id , message_id=call.message.message_id, timeout=20)
            bot.send_photo(chat_id=call.message.chat.id, photo=img_url, caption=text, parse_mode='Markdown', reply_markup=markup)
            # bot.edit_message_text(text=text, parse_mode='Markdown', chat_id=call.message.chat.id , message_id=call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, text='和你没关系，别点了~', show_alert=True)

    # 评分
    if 'rating' in call_data:
        test_id = int(call_data.split('rating')[0])
        if tg_from_id == test_id:
            rating_data = int(call_data.split('rating')[1])
            try:
                subject_id = call.message.reply_markup.keyboard[0][0].callback_data.split('anime_back')[1]
            except IndexError:
                subject_id = call.message.reply_markup.keyboard[0][0].callback_data.split('subject_id')[1]
                
            def rating_text():
                
                text = {'*'+ subject_info_get(test_id, subject_id)['name_cn'] +'*\n\n'

                        'BGM ID：`' + str(subject_id) + '`\n\n'

                        '➤ BGM 平均评分：`'+ str(subject_info_get(test_id, subject_id)['score']) +'`🌟\n'
                        '➤ 您的评分：`'+ str(user_rating_get(test_id, subject_id)) +'`🌟\n\n'

                        '➤ 观看进度：`'+ eps_get(test_id, subject_id)['watched'] + '`\n\n'

                        '💬 [吐槽箱](https://bgm.tv/subject/'+ str(subject_id) +'/comments)\n\n'

                        '请点按下列数字进行评分'}

                markup = telebot.types.InlineKeyboardMarkup()       
                markup.add(telebot.types.InlineKeyboardButton(text='返回',callback_data=str(test_id)+'subject_id'+str(subject_id)),telebot.types.InlineKeyboardButton(text='1',callback_data=str(test_id)+'rating1'),telebot.types.InlineKeyboardButton(text='2',callback_data=str(test_id)+'rating2'),telebot.types.InlineKeyboardButton(text='3',callback_data=str(test_id)+'rating3'),telebot.types.InlineKeyboardButton(text='4',callback_data=str(test_id)+'rating4'),telebot.types.InlineKeyboardButton(text='5',callback_data=str(test_id)+'rating5'),telebot.types.InlineKeyboardButton(text='6',callback_data=str(test_id)+'rating6'),telebot.types.InlineKeyboardButton(text='7',callback_data=str(test_id)+'rating7'),telebot.types.InlineKeyboardButton(text='8',callback_data=str(test_id)+'rating8'),telebot.types.InlineKeyboardButton(text='9',callback_data=str(test_id)+'rating9'),telebot.types.InlineKeyboardButton(text='10',callback_data=str(test_id)+'rating10'))
                bot.edit_message_caption(caption=text, chat_id=call.message.chat.id , message_id=call.message.message_id, parse_mode='Markdown', reply_markup=markup)
                
            if rating_data == 0:
                rating_text()
            status = 'do'
            if rating_data == 1:
                rating = '1'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 2:
                rating = '2'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 3:
                rating = '3'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 4:
                rating = '4'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 5:
                rating = '5'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 6:
                rating = '6'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 7:
                rating = '7'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 8:
                rating = '8'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 9:
                rating = '9'
                collection_post(test_id, subject_id, status, rating)
                rating_text()
            if rating_data == 3:
                rating = '10'
                collection_post(test_id, subject_id, status, rating) 
                rating_text()          
        else:
            bot.answer_callback_query(call.id, text='和你没关系，别点了~', show_alert=True)

    # 已看最新
    if 'anime_eps' in call_data:
        test_id = int(call_data.split('anime_eps')[0])
        if tg_from_id == test_id:
            eps_id = int(call_data.split('anime_eps')[1])
            eps_status_get(test_id, eps_id) # 更新观看进度
            subject_id = call.message.reply_markup.keyboard[0][0].callback_data.split('anime_back')[1]
            rating = user_rating_get(test_id, subject_id)

            text = {'*'+ subject_info_get(test_id, subject_id)['name_cn'] +'*\n\n'

                    'BGM ID：`' + str(subject_id) + '`\n'
                    '➤ BGM 平均评分：`'+ str(subject_info_get(test_id, subject_id)['score']) +'`🌟\n'
                    '➤ 您的评分：`'+ str(rating) +'`🌟\n'
                    '➤ 放送开始：`'+ subject_info_get(test_id, subject_id)['air_date'] + '`\n'
                    '➤ 放送星期：`'+ subject_info_get(test_id, subject_id)['air_weekday'] + '`\n'
                    '➤ 观看进度：`'+ eps_get(test_id, subject_id)['watched'] + '`\n\n'
                    
                    '💬 [吐槽箱](https://bgm.tv/subject/'+ str(subject_id) +'/comments)\n'
                    '📝 [第' + eps_get(test_id, subject_id)['watch'] +' 话评论](https://bgm.tv/ep/'+ str(eps_id) +')\n'}

            markup = telebot.types.InlineKeyboardMarkup()
            unwatched_id = eps_get(test_id, subject_id)['unwatched_id']
            if unwatched_id == []:
                status = 'collect'
                collection_post(test_id, subject_id, status, rating) # 看完最后一集自动更新收藏状态为看过
                markup.add(telebot.types.InlineKeyboardButton(text='返回',callback_data=str(test_id)+'anime_back'+str(subject_id)),telebot.types.InlineKeyboardButton(text='评分',callback_data=str(test_id)+'rating0'))
            else:    
                markup.add(telebot.types.InlineKeyboardButton(text='返回',callback_data=str(test_id)+'anime_back'+str(subject_id)),telebot.types.InlineKeyboardButton(text='评分',callback_data=str(test_id)+'rating0'),telebot.types.InlineKeyboardButton(text='已看最新',callback_data=str(test_id)+'anime_eps'+str(unwatched_id[0])))
            bot.edit_message_caption(caption=text, chat_id=call.message.chat.id , message_id=call.message.message_id, parse_mode='Markdown', reply_markup=markup)
            # bot.edit_message_text(text=text, parse_mode='Markdown', chat_id=call.message.chat.id , message_id=call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, text='和你没关系，别点了~', show_alert=True)

    # 动画再看详情页返回
    if 'anime_back' in call_data:
        test_id = int(call_data.split('anime_back')[0])
        if tg_from_id == test_id:
            access_token = user_data_get(test_id).get('access_token')
            params = {'app_id': APP_ID}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                'Authorization': 'Bearer ' + access_token}

            url = 'https://api.bgm.tv/user/' + str(user_data_get(test_id).get('user_id')) + '/collections/anime'

            try:
                r = requests.get(url=url, params=params, headers=headers)
            except requests.ConnectionError:
                r = requests.get(url=url, params=params, headers=headers)
            
            anime_data = json.loads(r.text)
            anime = None
            anime_do_list = None
            anime_count = 0
            subject_id_li = None
            subject_data_li = None
            for i in anime_data:
                if i.get('name') == 'anime':
                    anime = i.get('collects')
                    for i in anime:
                        if i.get('status').get('type') == 'do':
                            anime_count = i.get('count')
                            anime_do_list = i.get('list')
                            for i in anime_do_list:
                                subject_id_li = [i['subject_id'] for i in anime_do_list]
                                subject_data_li = [i['subject']['name_cn'] for i in anime_do_list]

            markup = telebot.types.InlineKeyboardMarkup()
            for item in list(zip(subject_data_li,subject_id_li)):
                markup.add(telebot.types.InlineKeyboardButton(text=item[0],callback_data=str(test_id)+'subject_id'+str(item[1])))

            eps_li = [eps_get(test_id, subject_id)['watched'] for subject_id in subject_id_li]

            anime_data = ''.join([a +' `['+ b +']`\n\n' for a,b in zip(subject_data_li,eps_li)])

            text = {'*'+ nickname_data(test_id) +' 在看的动画*\n\n'+
                    anime_data +
                    '共'+ str(anime_count) +'部'}

            bot.delete_message(chat_id=call.message.chat.id , message_id=call.message.message_id, timeout=20)
            bot.send_message(text=text, parse_mode='Markdown', chat_id=call.message.chat.id , reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, text='和你没关系，别点了~', show_alert=True)


# 开始启动
if __name__ == '__main__':
    bot.polling()