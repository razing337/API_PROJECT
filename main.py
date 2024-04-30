from aiogram import Bot, Dispatcher, types
from database import Database
from config import APITOKEN, ADMINID

bot = Bot(token=APITOKEN)
dispatcher = Dispatcher(bot)

database = Database("database.db")

censure = []
with open("censure.txt", "r", encoding="utf8") as file:
    for word in file:
        censure.append("".join(word.split()))


@dispatcher.messagehandler(commands='start')
async def start(message: types.Message):
    await message.answer("👋 Привет! Я плохой ботик, который будет всех банить :)")


@dispatcher.messagehandler(commands=['getid'])
async def getid(message: types.Message):
    await message.answer(message.fromuser.id)


@dispatcher.messagehandler(commands=['kick'])
async def kick(message: types.Message):
    if message.fromuser.id == ADMINID:
        if not message.replytomessage:
            await message.answer("Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.kickchatmember(message.chat.id, message.replytomessage.fromuser.id)
        await message.answer(f"Пользователь @{message.replytomessage.fromuser.username} исключён из беседы.")
        await message.delete()


@dispatcher.messagehandler(commands='ban')
async def kick(message: types.Message):
    if message.fromuser.id == ADMINID:
        if not message.replytomessage:
            await message.answer("Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.banchatmember(message.chat.id, message.replytomessage.fromuser.id)
        await message.answer(f"Пользователь @{message.replytomessage.fromuser.username} заблокирован в беседе.")
        await message.delete()


@dispatcher.messagehandler(commands=['unban'])
async def unban(message: types.Message):
    if message.fromuser.id == ADMINID:
        if not message.replytomessage:
            await message.answer("Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.unbanchatmember(message.chat.id, message.replytomessage.fromuser.id)
        await message.answer(f"Пользователь @{message.replytomessage.fromuser.username} разбанен в беседе.")
        await message.delete()


@dispatcher.messagehandler(commands='mute')
async def mute(message: types.Message):
    if message.fromuser.id == ADMINID:
        if not message.replytomessage:
            await message.answer("Команда должна быть отправлена ответом на сообщение")
            return
        if len(message.text.split()) < 2:
            await message.answer("Для того чтобы замутить пользователя нужно ввести время в секундах, пример: /mute 60")
            return
        mutetime = int(message.text.split()[1])
        database.addmute(userid=message.replytomessage.fromuser.id, mutetime=mutetime)
        await message.delete()
        await message.replytomessage.reply(f"Пользователь @{message.replytomessage.fromuser.username} замучен на {mutetime} секунд!")


@dispatcher.messagehandler(contenttypes='new_chat_members')
async def newuserinchat(message: types.Message):
    await message.delete()


@dispatcher.messagehandler(contenttypes=['leftchatmember'])
async def userleftfromchat(message: types.Message):
    await message.delete()


@dispatcher.messagehandler()
async def deletecensure(message: types.Message):
    messagelist = message.text.lower().split()
    for usermessage in messagelist:
        if usermessage in censure:
            await message.delete()
            await message.answer("Не нужно такое присылать")
            break

    if not database.examination(message.fromuser.id):
        database.add(message.fromuser.id)
    if not database.mute(message.fromuser.id):
        pass
    else:
        await bot.restrictchatmember(message.chat.id, message.fromuser.id, untildate=None)

if name == 'main':
    executor.startpolling(dispatcher)