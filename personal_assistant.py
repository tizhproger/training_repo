import os
from telethon import TelegramClient, events

from animations import Animations
from modules.quotes import mQuotesMod
from modules.lovemagic import ILYMod
from modules.notes import NotesMod
from modules.qrcode import QRtoolsMod
from modules.squotes import ShitQuotesMod
from modules.hostinf import InfoMod
from modules.yesno import YesNoMod
from modules.whois import WhoIsMod
from modules.aniquote import AnimatedQuotesMod
from modules.textonphoto import TextOnPhotoMod
from modules.weather import WeatherMod
from modules.nedoquotes import NedoQuotesMod
from modules.tag import TagMod
from modules.lmgtfy import LMGTFYMod
from modules.ytdownload import YtDlMod
from modules.information import WhoIsMod
from modules.chat import ChatMod
from modules.arts import ArtsMod
from modules.tempmail import TempMailMod
from modules.demot import DemotivatorMod
from modules.dotify import DotifyMod
from modules.typer import TyperMod
from modules.insta_loader import Instload
from modules.Circles import CirclesMod
from modules.v2a import Video2Audio
from modules.database import DB


mode = False
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
client = TelegramClient(os.environ.get('SESSION_NAME'), api_id, api_hash).start()

squote = {}
db = DB('telehelper.json')

animate = Animations(client)
quotes = mQuotesMod(client)
love = ILYMod()
note = NotesMod(client, db)
qr = QRtoolsMod()
squotes = ShitQuotesMod(client, squote)
hostinfo = InfoMod()
choice = YesNoMod()
aniquote = AnimatedQuotesMod(client)
tag = TagMod()
phototext = TextOnPhotoMod()
weather = WeatherMod()
nedoquotes = NedoQuotesMod()
lmgt = LMGTFYMod()
ytdwnl = YtDlMod()
info = WhoIsMod()
chats = ChatMod()
arts = ArtsMod()
tmail = TempMailMod()
dmot = DemotivatorMod(client)
dotify = DotifyMod()
typer = TyperMod()
inst = Instload()
circle = CirclesMod()
vids = Video2Audio(client)

banwords = db.getwords()
arguments_msg = '**Set correct argument!**'

async def commands(message):
    global banwords, inst
    params = message.text.split()
    
    if message.text.startswith('.inst'):
        if len(params) > 1:
            if 'https' in params[1]:
                await message.edit('**Loading story...**')
                link = inst.download_story(message.text)
                if 'video' in link:
                    await client.send_file(message.chat_id, link['video'], caption=f"[Story link]({params[1]})")
                    await message.delete()
                    return True

                elif 'photo' in link:
                    await client.send_file(message.chat_id, link['photo'], caption=f"[Story link]({params[1]})")
                    await message.delete()
                    return True

                else:
                    await message.edit('**' + link['error'] + '**')
                    return True
            else:
                await message.edit('**Collecting stories...**')
                links = inst.all_stories(params[1])
                if 'error' in links:
                    await message.edit('**' + links['error'] + '**')
                    return True
                    
                else:
                    for link in links:
                        await client.send_file(message.chat_id, link, caption=f"[Profile link](https://instagram.com/{params[1]})")
                    await message.delete()
                    return True
            
        await message.edit('**Specify correct insta data!**')
   
    if message.text.startswith('.chatmodes'):
        modes = db.getmodes(message.chat_id)
        if modes:
            desc = "Безполитики: " + ('Вкл' if modes[1] else 'Выкл') + '\nПолитмут: ' + ('Вкл' if modes[2] else 'Выкл') + '\nАвтобан: ' + ('Вкл' if modes[3] else 'Выкл') + '\nАвтоварн: ' + ('Вкл' if modes[4] else 'Выкл')
            await message.reply(desc)
        else:
            await message.reply('Чат не найден...')
        return True
    
    if message.text.startswith('.enable'):
        if len(params) > 1:
            for word in params[1:]:
                if not db.addmode(message.chat_id, word, True):
                    await message.reply('Режим не найден: ' + word)
                    params.remove(word)
            
            if len(params) > 1:
                await message.reply('Режимы включены: ' + ' '.join(params[1:]))
            return True
        else:
            await message.reply('Укажите режимы!')
            return True
    
    if message.text.startswith('.disable'):
        if len(params) > 1:
            for word in params[1:]:
                if not db.addmode(message.chat_id, word, False):
                    await message.reply('Режим не найден: ' + word)
                    params.remove(word)
            
            if len(params) > 1:
                await message.reply('Режимы выключены: ' + ' '.join(params[1:]))
            return True
        else:
            await message.reply('Укажите режимы!')
            return True
    
    if message.text.startswith('.banwords'):
        banwords = db.getwords()
        if banwords:
            await message.reply('Банворды: ' + ' '.join(banwords))
        else:
            await message.reply('Банвордов нет...')
        return True
    
    if message.text.startswith('.addword'):
        for word in params[1:]:
            if not db.checkword(word):
                db.addword(word)
                banwords.append(word)
            else:
                params.remove(word)
        await message.reply('Банворды добавлены: ' + ' '.join(params[1:]))
        return True
    
    if message.text.startswith('.delword'):
        for word in params[1:]:
            if db.checkword(word):
                db.delword(word)
                banwords.remove(word)
            else:
                params.remove(word)
        await message.reply('Банворды удалены: ' + ' '.join(params[1:]))
        return True
    
    if message.text.startswith('.round'):
        await circle.roundcmd(message)
        return True
    
    if message.text.startswith('.conv'):
        await vids.v2acmd(message)
        return True

    if message.text.startswith('.wave'):
        await vids.waveform(message)
        return True

    if message.text.startswith('.sq'):
        """
        Использование:

        • .sq <кол-во сообщений> + <реплай> + <!file - скидывает файлом (по желанию)> + <цвет (по желанию)>
        >>> .sq
        >>> .sq 2 #2d2d2d
        >>> .sq red
        >>> .sq !file
        """
        await squotes.sqcmd(message)
        return True
    
    if message.text.startswith('.fsq'):
        """
        Использование:

        • .fsq <@ или ID> + <текст> - квота от юзера с @ или ID + указанный текст
        >>> .fsq @onetimeusername Вам пизда

        • .fsq <реплай> + <текст> - квота от юзера с реплая + указанный текст
        >>> .fsq Я лох

        • .fsq <@ или ID> + <текст> + -r + <@ или ID> + <текст> - квота с фейковым реплаем
        >>> .fsq @Fl1yd спасибо -r @onetimeusername Ты крутой

        • .fsq <@ или ID> + <текст> + -r + <@ или ID> + <текст>; <аргументы> - квота с фейковыми мульти сообщениями
        >>> .fsq @onetimeusername Пацаны из @sh1tchannel, ждите награду за ахуенный ботнет; @guslslakkaakdkab чево; @Fl1yd НАШ БОТНЕТ ЛУЧШИЙ -r @guslslakkaakdkab чево
        """
        await squotes.fsqcmd(message)
        return True

    if message.text.startswith('.qt'):
        """Quote a message. Args: ?<count> ?file"""
        await quotes.quotecmd(message)
        return True
    
    if message.text.startswith('.fqt'):
        """Fake message quote. Args: @<username>/<id>/<reply> <text>"""
        await quotes.fquotecmd(message)
        return True
    
    if message.text.startswith('.qrm'):
        """.qrm <text or reply>"""
        await qr.makeqrcmd(message)
        return True
    
    if message.text.startswith('.qrr'):
        """.qrr <qrcode or reply to qrcode>"""
        await qr.readqrcmd(message)
        return True
    
    if message.text.startswith('.inf'):
        """.inf to get host info"""
        await hostinfo.infocmd(message)
        return True
    
    if message.text.startswith('.ily'):
        txt = message.text.split()
        if len(txt) > 1:
            await love.ilycmd(message, ' '.join(txt[1:]))
        else:
            await love.ilycmd(message)
        return True
    
    if message.text.startswith('.ht'):
        if len(params) > 2:
            await animate.animation(message=message, times=int(params[1]), reverse=True if params[2] == '1' else False, mode='hearts')
        elif len(params) > 1:
            await animate.animation(message=message, times=int(params[1]), mode='hearts')
        else:
            await animate.animation(message=message, mode='hearts')
        return True

    if message.text.startswith('.pls'):
        if len(params) > 2:
            await animate.animation(message=message, times=int(params[1]), reverse=True if params[2] == '1' else False, mode='pulse')
        elif len(params) > 1:
            await animate.animation(message=message, times=int(params[1]), mode='pulse')
        else:
            await animate.animation(message=message, mode='pulse')
        return True
    
    if message.text.startswith('.love'):
        if len(params) > 2:
            await animate.animation(message=message, times=int(params[1]), reverse=True if params[2] == '1' else False, mode='love')
        elif len(params) > 1:
            await animate.animation(message=message, times=int(params[1]), mode='love')
        else:
            await animate.animation(message=message, mode='love')
        return True
    
    if message.text.startswith('.choice'):
        await choice.yesnocmd(message)
        return True
    
    if message.text.startswith('.nt'):
        await note.notecmd(message, 'notes')
        return True
    
    if message.text.startswith('.dn'):
        await note.delnotecmd(message, 'notes')
        return True
    
    if message.text.startswith('.sn'):
        await note.savecmd(message, 'notes')
        return True
    
    if message.text.startswith('.dan'):
        await note.delallnotescmd(message, 'notes')
        return True
    
    if message.text.startswith('.an'):
        await note.notescmd(message, 'notes')
        return True
    
    if message.text.startswith('.aq'):
        """.aq quote on animated sticker"""
        await aniquote.aniqcmd(message)
        return True
    
    if message.text.startswith('.taga'):
        """.taga text, mention all users in chat"""
        await tag.tagallcmd(message)
        return True
    
    if message.text.startswith('.tag'):
        """.tag @user text, for hidden mention"""
        await tag.tagcmd(message)
        return True
    
    if message.text.startswith('.txb'):
        """.txb text on bottom of img/sticker"""
        await phototext.bottomcmd(message)
        return True
    
    if message.text.startswith('.txp'):
        """.txp text on top of img/sticker"""
        await phototext.topcmd(message)
        return True
    
    if message.text.startswith('.txc'):
        """.txc text in center of img/sticker"""
        await phototext.centercmd(message)
        return True
    
    if message.text.startswith('.pw'):
        """.pw cirty. get weather in ascii image"""
        await weather.pwcmd(message)
        return True
    
    if message.text.startswith('.nq'):
        """.nq text/reply, generate meme pic with quote"""
        await nedoquotes.nqcmd(message)
        return True
    
    if message.text.startswith('.lmg'):
        """.nq text/reply, generate meme pic with quote"""
        await lmgt.lmgtfycmd(message)
        return True

    if message.text.startswith('.ytd'):
        """.nq text/reply, generate meme pic with quote"""
        await ytdwnl.ripvcmd(message)
        return True
    
    if message.text.startswith('.chatis'):
        """.nq text/reply, generate meme pic with quote"""
        await info.chatinfocmd(message)
        return True
    
    if message.text.startswith('.whois'):
        """.nq text/reply, generate meme pic with quote"""
        await info.userinfocmd(message)
        return True
    
    if message.text.startswith('.dmot'):
        """.nq text/reply, generate meme pic with quote"""
        await dmot.demoticmd(message)
        return True
    
    if message.text.startswith('.quote'):
        """.nq text/reply, generate meme pic with quote"""
        await dmot.mqcmd(message)
        return True
    
    if message.text.startswith('.type'):
        """.type text/reply, slowly type text"""
        
        await typer.typecmd(message)
        return True
    
    if message.text.startswith('.chat'):
        args = message.text.split()
        if len(args) > 1:
            cmd = args[1]
            args.remove(cmd)
            text = ' '.join(args)

            if cmd == 'id':
                msg = await message.edit(text)
                await chats.chatidcmd(msg)
                return True
            
            if cmd == 'user':
                if message.is_reply or ('@' in message.text):
                    msg = await message.edit(text)
                    await chats.useridcmd(msg)
                    return
                await message.edit('Works with tag or reply!')
                return True
            
            if cmd == 'users':
                msg = await message.edit(text)
                await chats.userscmd(msg)
                return True
            
            if cmd == 'admins':
                msg = await message.edit(text)
                await chats.adminscmd(msg)
                return True
            
            if cmd == 'bots':
                msg = await message.edit(text)
                await chats.botscmd(msg)
                return True
            
            if cmd == 'common':
                if message.is_reply or ('@' in message.text):
                    msg = await message.edit(text)
                    await chats.commoncmd(msg)
                    return True
                await message.edit('Works with tag or reply!')
                return True
            
            if cmd == 'dump':
                """.chatdump <n> <m> <s>
                    Дамп юзеров чата
                    <n> - Получить только пользователей с открытыми номерами
                    <m> - Отправить дамп в избранное
                    <s> - Тихий дамп
                """
                msg = await message.edit(text)
                await chats.chatdumpcmd(msg)
                return True
            
            if cmd == 'help':
                text = "Availible commands:\n`id` / `user` / `users` / `admins` / `bots` / `common` / `dump`"
                await message.edit(text)
                return True
            
        await message.edit(arguments_msg)
    
    if message.text.startswith('.art'):
        args = message.text.split()
        if len(args) > 1:
            cmd = args[1]
            args.remove(cmd)
            text = ' '.join(args)

            if cmd == 'vjuh':
                msg = await message.edit(text)
                await arts.vjuhcmd(msg)
                return True
            
            if cmd == 'cow':
                msg = await message.edit(text)
                await arts.cowsaycmd(msg)
                return True
            
            if cmd == 'lol':
                msg = await message.edit(text)
                await arts.lolcmd(msg)
                return True
            
            if cmd == 'fuk':
                msg = await message.edit(text)
                await arts.fuckyoucmd(msg)
                return True
            
            if cmd == 'hello':
                msg = await message.edit(text)
                await arts.hellocmd(msg)
                return True
            
            if cmd == 'coffee':
                msg = await message.edit(text)
                await arts.coffeecmd(msg)
                return True
            
            if cmd == 'bruh':
                msg = await message.edit(text)
                await arts.bruhcmd(msg)
                return True
            
            if cmd == 'uno':
                msg = await message.edit(text)
                await arts.unocmd(msg)
                return True
            
            if cmd == 'imp':
                if message.is_reply or ('@' in message.text):
                    msg = await message.edit(text)
                    await arts.impscmd(msg)
                    return
                await message.edit('**Works with tag or reply!**')
                return True
            
            if cmd == 'f':
                msg = await message.edit(text)
                await arts.fcmd(msg)
                return True
            
            if cmd == 'help':
                text = "Availible arts:\n`vjuh` / `cow` / `lol` / `fuk` / `hello` / `coffee` / `bruh` / `uno` / `imp` / `f`"
                await message.edit(text)
                return True
            
        await message.edit(arguments_msg)
    
    if message.text.startswith('.tmail'):
        args = message.text.split()
        if len(args) > 1:
            cmd = args[1]
            args.remove(cmd)
            text = ' '.join(args)

            if cmd == 'get':
                msg = await message.edit(text)
                await tmail.getmailcmd(msg)
                return True
            
            if cmd == 'look':
                msg = await message.edit(text)
                await tmail.lookmailcmd(msg)
                return True
            
            if cmd == 'read':
                msg = await message.edit(text)
                await tmail.readmailcmd(msg)
                return True
            
            if cmd == 'help':
                text = "Availible commands:\n`get` / `look` / `read`"
                await message.edit(text)
                return True
        
        await message.edit(arguments_msg)
    
    if message.text.startswith('.dot'):
        args = message.text.split()
        if len(args) > 1:
            cmd = args[1]
            args.remove(cmd)

            if cmd == 'bw':
                await dotify.dotifycmd(message, True)
                return True
                
        await dotify.dotifycmd(message)
        return True
    
    if message.text.startswith('.suka'):
        await message.edit(chr(1103)+chr(32)+chr(1089)+chr(1091)+chr(1082)+chr(1072)+chr(32)+chr(1077)+chr(1073)+chr(1091)+chr(1095)+chr(1072)+chr(1103))
        return True
    
    if message.text.startswith('.help'):
        await client.edit_message(message.chat, message,
    """
    __**Personal assistant commands**__
  `.sq` - __quote message__:
         **(reply)** __(just quote reply message)__
         **(reply + number)** __(quote with number of replies on it)__
         
  `.fsq` - __fake quote__
         **(reply + txt)** __(fake text reply)__
         **(tag + txt)** __(fake text)__
         **(tag + txt -r tag + txt)** __(fake reply chain)__
         **(tag + txt; tag + txt)** __(fake messages)__
         
  `.qt` - __quote message (no reply)__:
         **(reply)** __(just quote reply message)__
         
  `.fqt` - __fake quote (no reply)__:
         **(tag + txt)** __(fake user quote)__
         
  `.qrm` - __qr code from text__:
         **(reply or text)**
         
  `.qrr` - __text from qr code__:
         **(reply)**
         
  `.spd` - __host speetest__
  `.inf` - __host info__
  `.ily` - __I love you animation__:
         **(reply or empty)** __(love animation)__
         **(reply or empty + text)** __(love aniation with text end)__
         
  `.ht` - __heart animation__:
         **(number)** __(number of times)__
         **(number + 1 or 0)** __(times + reverse or normal)__
         
  `.pls` - __pulse animation__:
         **(number)** __(number of times)__
         **(number + 1 or 0)** __(times + reverse or normal)__
         
  `.love` - __love animation__:
         **(number)** __(number of times)__
         **(number + 1 or 0)** __(times + reverse or normal)__
         
  `.choice` - __choice answer__:
        **(reply or empty)**
        
  `.aq` **text** - __anim stick with text__
  `.taga` - __tag all chat hidden__
  `.tag` **@tag** - __user hidden tag__
  `.txb` **reply_photo** - __bottom text on photo__
  `.txp` **reply_photo** - __top text on photo__
  `.txc` **reply_photo** - __center text on photo__
  `.pw` **city** - __city weather (ascii)__
  `.nq` **text/reply** - __quote on meme__:
        **(reply or empty)**
        
  `.wsh` **link/reply** - __link webshot__
  `.lmg` **text** - __how to google__:
        **(reply or empty)**
        
  `.ytd` **link/reply** - __youtube download **320**__
        **(reply or empty)**
    
  `.chatis` - __get chat info__
        **(reply or empty)**
   
  `.whois` - __get user info__
        **(reply or empty)**
        
  `.dmot` **reply** - __demotivator from pic__
        **(reply on photo)**
   
  `.quote` **reply** - __quote with user photo__
        **(reply on message)**
        
  `.type` **text** - __slow text typing__
        **(text)**
   
  `.suka` - __fuking text__
  
  `.chat` **option** - __chat features by options__
        `id` - __get chat id__
        `user` - __get user id__
        `users` - __get all chat users__
        `admins` - __get all chat admins__
        `bots` - __get all chat bots__
        `common` - __get common chat with user__
        `dump` - __dump chat users__
            (n - open numbers, m - dump to favorite, s - silent dump)
        `help` - __all availible options__
   
   `.art` **option** + text - __arts by options__
        `vjuh` - __vjuh with text__
        `cow` - __cow with text__
        `lol` - __LOL__
        `fuk` - __FUK__
        `hello` - __Hello__
        `coffee` - __cup of coffee__
        `bruh` - __BRUH__
        `uno` - __uno switch card__
        `imp` - __impostor__
        `f` - __press F__
        `help` - __all options__
   
   `.tmail` **option** - __temporary mail__
        `get` - __get temporary mail__
        `look` - __look for new letters__
        `read` - __read letters from mail__
        `help` - __all options__
   
   `.dot` **option** - __create photo from dots__
        `bw` - __black and white dots__
        without bw - __color dots__
""")
        return True

@client.on(events.NewMessage(outgoing=True))
async def outgoing(event):
    msg = event.message

    if msg.is_reply:
        usr_id = (await event.message.get_reply_message()).sender.id
        if msg.text.startswith('.add'):
            if db.allowed(usr_id):
                await msg.edit('Доступ уже открыт')
            elif db.add_user(usr_id):
                await msg.edit('Доступ: `открыт`')
            else:
                await msg.edit('Что-то не так...')
            return

        if msg.text.startswith('.del'):
            if not db.allowed(usr_id):
                await msg.edit('Доступа нет')
            elif db.del_user(usr_id):
                await msg.edit('Доступ: `закрыт`')
            else:
                await msg.edit('Что-то не так...')
            return
    
    if msg.text.startswith('.reveal'):
        await note.notecmd(msg, 'vault')
        return
    
    if msg.text.startswith('.remove'):
        await note.delnotecmd(msg, 'vault')
        return
    
    if msg.text.startswith('.vault'):
        await note.savecmd(msg, 'vault')
        await msg.delete()
        return
    
    if msg.text.startswith('.clean'):
        await note.delallnotescmd(msg, 'vault')
        return
    
    if msg.text.startswith('.stored'):
        await note.notescmd(msg, 'vault')
        return

    await commands(msg)


@client.on(events.NewMessage(incoming=True))
async def incoming(event):
    if db.checkchat(event.message.chat_id):
        if db.checkmode(event.message.chat_id, 'nopolitics'):
            for el in banwords:
                if el in event.message.text.lower():
                    if db.checkmode(event.message.chat_id, 'autoban'):
                        await event.message.reply('/ban')
                        await event.message.delete()

                    elif db.checkmode(event.message.chat_id, 'autowarn'):
                        await event.message.reply('/warn')
                        await event.message.delete()

                    elif db.checkmode(event.message.chat_id, 'mutepolitics'):
                        await event.message.reply('/mute 12h Политота')
                        await event.message.delete()
                    else:
                        await event.message.delete()
                    
    if event.message.text.startswith('.'):
        if db.allowed(event.message.sender_id):
            if event.message.is_reply:
                reply_msg = await event.message.get_reply_message()
                msg = await client.send_message(event.message.chat_id, message=event.message.text, reply_to=reply_msg)
            else:
                msg = await client.send_message(event.message.chat_id, message=event.message.text, reply_to=event.message)
                
            reply = await event.client.get_messages(event.chat, ids=msg.id)
            res = await commands(reply)
            if not res:
                await reply.delete()
                await event.message.reply('**Команда не найдена...**')

client.run_until_disconnected()
