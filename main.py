import telebot
import asyncio
import aiohttp
import os


bot = telebot.TeleBot(os.environ.get('TOKEN'))


async def check_ava(player_id):
    async with aiohttp.ClientSession() as session:
        urls = []
        task_list = []

        urls.append(f'http://mwiz.mobi/static/img/av/p{player_id}.gif')
        urls.append(f'http://mwiz.mobi/static/img/av/p{player_id}.jpg')

        for ava_id in range(2, 200):
            urls.append(f'http://mwiz.mobi/static/img/av/p{player_id}-{ava_id}.gif')
            urls.append(f'http://mwiz.mobi/static/img/av/p{player_id}-{ava_id}.jpg')

        for url in urls:
            task_list.append(asyncio.create_task(session.get(url)))

        responses = await asyncio.gather(*task_list)

    return responses


async def check_present(player_id):
    async with aiohttp.ClientSession() as session:
        urls = []
        task_list = []

        urls.append(f'http://mwiz.mobi/static/img/present/{player_id}.gif')
        urls.append(f'http://mwiz.mobi/static/img/present/{player_id}.png')

        for pres_id in range(2, 200):
            urls.append(f'http://mwiz.mobi/static/img/present/{player_id}{pres_id}.gif')
            urls.append(f'http://mwiz.mobi/static/img/present/{player_id}{pres_id}.png')

        for url in urls:
            task_list.append(asyncio.create_task(session.get(url)))

        responses = await asyncio.gather(*task_list)

    return responses


async def check_smile(player_id):
    async with aiohttp.ClientSession() as session:
        urls = []
        task_list = []

        urls.append(f'http://mwiz.mobi/static/img/smiles/p{player_id}.gif')

        for pres_id in range(1, 100):
            urls.append(f'http://mwiz.mobi/static/img/smiles/p{player_id}-{pres_id}.gif')

        for url in urls:
            task_list.append(asyncio.create_task(session.get(url)))

        responses = await asyncio.gather(*task_list)

    return responses


async def check_image(player_id):
    async with aiohttp.ClientSession() as session:
        urls = []
        task_list = []

        urls.append(f'http://d.mwiz.mobi/static/img/item/p{player_id}.gif')

        for pres_id in range(1, 15):
            urls.append(f'http://mwiz.mobi/static/img/item/p{player_id}-{pres_id}.gif')

        for url in urls:
            task_list.append(asyncio.create_task(session.get(url)))

        responses = await asyncio.gather(*task_list)

    return responses


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Введи id игрока для получения его личных картинок".format(message.from_user))


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Введи число, являющееся id игрока Волшебников для получения личных аватарок, подарков, смайлов, образов")

    else:
        try:
            player_id = int(message.text)

            msg = "Аватарки:\n"

            responses = asyncio.run(check_ava(player_id))

            i = 0
            while i < len(responses):
                r = responses[i]
                if r.ok:
                    if str(r.url).endswith("gif"):
                        i += 1
                    msg += str(r.url) + "\n"
                i += 1
                if len(msg) > 4000:
                    bot.send_message(message.chat.id, msg)
                    msg = ""

            if msg != "": 
                bot.send_message(message.chat.id, msg)


            msg = "\nПодарки:\n"

            responses = asyncio.run(check_present(player_id))

            i = 0
            while i < len(responses):
                r = responses[i]
                if r.ok:
                    msg += str(r.url) + "\n"
                i += 1
                if len(msg) > 4000:
                    bot.send_message(message.chat.id, msg)
                    msg = ""

            if msg != "": 
                bot.send_message(message.chat.id, msg)

            msg = "\nСмайлы:\n"

            responses = asyncio.run(check_smile(player_id))

            i = 0
            while i < len(responses):
                r = responses[i]
                if r.ok:
                    msg += str(r.url) + "\n"
                i += 1
                if len(msg) > 4000:
                    bot.send_message(message.chat.id, msg)
                    msg = ""

            if msg != "": 
                bot.send_message(message.chat.id, msg)

            msg = "\nОбразы:\n"

            responses = asyncio.run(check_image(player_id))

            i = 0
            while i < len(responses):
                r = responses[i]
                if r.ok:
                    msg += str(r.url) + "\n"
                i += 1
                if len(msg) > 4000:
                    bot.send_message(message.chat.id, msg)
                    msg = ""

            if msg != "": 
                bot.send_message(message.chat.id, msg)

        except:
            bot.send_message(message.chat.id, "Произошла непредвиденная ошибка. Обратитесь к создателю бота.")


bot.polling(none_stop=True, interval=0)
