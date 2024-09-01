import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import traceback
import math
import random

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # リアクション用絵文字の登録
    number_emojis=["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣","????"]

    # TLの全角→半角変換の登録
    trans_table = str.maketrans({"０":"0", "１":"1", "２":"2", "３":"3", "４":"4", "５":"5", "６":"6", "７":"7", "８":"8", "９":"9", "：":":"})

    # 受信したメッセージが"ro"だったら持越し時間を返す
    if message.content.startswith('ro ') or message.content.startswith('!ro '):
        val = message.content.split(' ')

        # 引数1つの場合、各持越し秒数に必要なダメージを返す（カズマサ仕様）
        if len(val) == 2:
            if val[1].isdecimal():
                outmes = "```それぞれの持越しに必要なダメージじゃい！\n"
                outmes += "20秒: " + val[1] + "万ダメージ"

                motikosi_times = [25, 30, 35, 40, 50, 60, 70, 80, 90]
                for time in motikosi_times:
                    damage = math.ceil(int(val[1]) / (1 - (time - 20) / 90))
                    outmes += "\n" + str(time) + "秒: " + str(damage) + "万ダメージ"

                outmes += "```"
                await message.channel.send(outmes)

        # 引数2つ以上の場合、残りHPに対する与えたダメージの持越し時間を返す
        elif len(val) > 2:
            if val[1].isdecimal() and val[2].isdecimal():
                outmes = "```残りHP" + val[1] + "万、与ダメージ" + val[2] + "万"

                # 引数3つの場合、残り時間を加算する
                if len(val) > 3 and val[3].isdecimal():
                    nokori_time = int(val[3])
                    outmes += "、残り" + val[3] + "秒"
                else:
                    nokori_time = 0
                outmes += "の持越しは、"

                time = math.floor((1 - int(val[1]) / int(val[2])) * 90 + nokori_time + 20)
                if time > 90:
                    time = 90
                outmes += str(time) + "秒じゃい！```"
                await message.channel.send(outmes)

    # 受信したメッセージが"calc"だったら計算結果を返す
    if message.content.startswith('calc ') or message.content.startswith('!calc '):
        val = message.content.split('calc ')

        if len(val) > 0:
            num = eval(val[1])
            outmes = "```" + val[1] + " = " + str(num) + "```"
            await message.channel.send(outmes)
                
    # 受信したメッセージが"kuji"だったら引数から1つ選んで返す
    if message.content.startswith('kuji ') or message.content.startswith('!kuji '):
        val = message.content.split(' ')

        if len(val) > 2:
            outmes = "```選ばれたのは " + val[random.randrange(start=1, stop=len(val), step=1)] + " でした。```"
            await message.channel.send(outmes)

    # 受信したメッセージが"!te"だったら凸先アンケートを表示
    if message.content == '!te':
        outmes = "```凸先アンケート```"
        reply = await message.channel.send(outmes)

        await reply.add_reaction(number_emojis[0])
        await reply.add_reaction(number_emojis[1])
        await reply.add_reaction(number_emojis[2])
        await reply.add_reaction(number_emojis[3])
        await reply.add_reaction(number_emojis[4])

    if message.content.startswith('!te '):
        outmes = "```凸先アンケート```"
        reply = await message.channel.send(outmes)

        val = message.content.split('te ')

        # 引数が2つ以上の場合、指定された凸先のみリアクションをつける
        if len(val) > 1:
            if "1" in val[1]:
                await reply.add_reaction(number_emojis[0])
            if "2" in val[1]:
                await reply.add_reaction(number_emojis[1])
            if "3" in val[1]:
                await reply.add_reaction(number_emojis[2])
            if "4" in val[1]:
                await reply.add_reaction(number_emojis[3])
            if "5" in val[1]:
                await reply.add_reaction(number_emojis[4])

    # 受信したメッセージが"kyuen"か"kyujo"だったら救助依頼
    if message.content.startswith('kyuen ') or message.content.startswith('kyujo ') or \
       message.content.startswith('kyuuen ') or message.content.startswith('kyuujo ') or \
       message.content.startswith('!kyuen ') or message.content.startswith('!kyujo ') or \
       message.content.startswith('!kyuuen ') or message.content.startswith('!kyuujo '):
        val = message.content.split(' ')

        if len(val) > 1:
            CHANNEL_ID = 0
            
            # ギルドIDは当BOTのgetgidコマンドで取得可能
            # 探検同盟
            if message.guild.id == 1212306629043814400:
                # コメント先チャンネルIDの指定
                # チャンネルIDは当BOTのgetcidコマンドで取得可能
                # クラバト進行
                #CHANNEL_ID = 612823446010986526
                # クラン依頼
                #CHANNEL_ID = 670530208855621632
 
                if val[1] == "1":
                    # 1ボス
                    CHANNEL_ID = 1212306629882810410
                elif val[1] == "2":
                    # 2ボス
                    CHANNEL_ID = 1212306629882810411
                elif val[1] == "3":
                    # 3ボス
                    CHANNEL_ID = 1212306629882810412
                elif val[1] == "4":
                    # 4ボス
                    CHANNEL_ID = 1212306629882810413
                elif val[1] == "5":
                    # 5ボス
                    CHANNEL_ID = 1212306629882810414
                else:
                    # ボス番号が1～5以外の場合、チャンネルID=0としてエラーにする
                    CHANNEL_ID = 0
               
                # ロールIDは@ロール名の前に\を付けてコメントするとIDに変換される（例：\@探検同盟）
                # 尚メンションが跳んでしまうので注意。

                # 探検同盟ロールの指定
                ROLE_ID = "<@&1212306629081440259>"
                #ROLE_ID = ""
            
            # 園芸士鯖
            elif message.guild.id == 1257014658771193907:
 
                if val[1] == "1":
                    # 1ボス
                    CHANNEL_ID = 1257229498425016413
                elif val[1] == "2":
                    # 2ボス
                    CHANNEL_ID = 1279664781258919976
                elif val[1] == "3":
                    # 3ボス
                    CHANNEL_ID = 1279664806416351253
                elif val[1] == "4":
                    # 4ボス
                    CHANNEL_ID = 1279664837529702431
                elif val[1] == "5":
                    # 5ボス
                    CHANNEL_ID = 1279664855384719422
                else:
                    # ボス番号が1～5以外の場合、チャンネルID=0としてエラーにする
                    CHANNEL_ID = 0
               
                # ロールIDは@ロール名の前に\を付けてコメントするとIDに変換される（例：\@探検同盟）
                # 尚メンションが跳んでしまうので注意。

                # 探検同盟ロールの指定
                ROLE_ID = "<@&1279097127489769573>"
                #ROLE_ID = ""

            # 自鯖（デバッグ用、白鳳鯖）
            elif message.guild.id == 673867780956618753:
                CHANNEL_ID = 725471441260118097
                ROLE_ID = "<@&729636032256933959>"
                #ROLE_ID = ""

            # チャンネルIDが0でなければメンションを飛ばす
            if CHANNEL_ID != 0:
                # 引数が2であればコマンドを打ったメンバーの名前、3以上の場合3つ目に指定されたメンバー名を指定
                if len(val) > 2:
                    user_name = val[2]
                else:
                    user_name = message.author.display_name

                outmes = ROLE_ID + " 【" + val[1] + "ボス】【" + user_name + "を救う会】\n"
                outmes += user_name + "ちゃんは生まれつき運にめぐまれず１時間以内に救出が必要です。しかし命をたすけるには莫大な打点がかかります。\n"
                outmes += user_name + "ちゃんを救う為どうか協力をよろしくお願いします。"

                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(outmes)

    # 受信したメッセージが"ctl"だったらTL変換
    if message.content.startswith('TL ') or message.content.startswith('!TL ') or \
       message.content.startswith('tl ') or message.content.startswith('!tl '):
        val = message.content.split('\n')

        # TLが指定されていなければエラー
        if len(val) == 1:
            outmes = "TLが指定されていません。"
            flag = 9

        else:
            mtime = 0   # 持越時間
            ptime = 0   # 減算時間
            outmes = ""
            flag = 0

            # 1行ずつ読み込み時間を変換。1行目はコマンド行なので持越時間を取得
            for i, line in enumerate(val):
                # コマンドの持越時間から減算時間を取得
                if i == 0:
                    tmp = line.split(' ')
                    mtime = int(tmp[1])
                    ptime = 90 - mtime
                    if ptime < 0 or ptime > 90:
                        outmes = "持ち越し時間の指定が正しくありません。"
                        flag = 9
                        break

                else:
                    # 全角数字と：を半角へ変換
                    line = line.translate(trans_table)

                    # TLを1行ずつ読み込み変換
                    min = ""    # 分
                    sec = ""    # 秒

                    # 1文字ずつ読み込み
                    for j, char in enumerate(line):
                        # ":"があれば前後から分と秒を取得
                        if j > 0 and char == ":":
                            if line[j - 1] == "0" or line[j - 1] == "1":
                                min =  line[j - 1]

                            if j + 2 < len(line):
                                tmp = line[j+1:j+3]
                                if tmp.isdecimal():
                                    sec = tmp

                            # 時間を秒に直して減算時間を引く
                            tsec = int(min) * 60 + int(sec) - ptime

                            # 時間が1以下ならタイムアップ
                            if tsec < 1:
                                flag = 1
                                break

                            # 時間を文字列に戻す
                            ttime = ""
                            if tsec > 59:
                                ttime = "1:" + str(tsec - 60).zfill(2)
                            else:
                                ttime = "0:" + str(tsec).zfill(2)

                            # TLの時間を変換
                            line = line[:j-1] + ttime + line[j+3:]

                    if flag == 1:
                        break

                    # 変換したTLを出力
                    outmes += line + "\n"

            if flag < 2:
                outmes = "持ち越し" + str(mtime) + "秒のTLです。\n```" + outmes + "```"

        await message.channel.send(outmes)

        
    # 受信したメッセージが"getgid"だったらギルドID取得
    if message.content.startswith('getgid'):
        await message.channel.send(str(message.guild) + "\n" + str(message.guild.id))

    # 受信したメッセージが"getcid"だったらチャンネルID取得
    if message.content.startswith('getcid'):
        await message.channel.send(str(message.channel) + "\n" + str(message.channel.id))

load_dotenv('.env')
token = os.getenv("DISCORD_BOT_TOKEN", "")
bot.run(token)
