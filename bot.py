# bot.py
from email.errors import MessageError
import os
from datetime import date

# library for entertainment :)))
import random

# library for crawler
import requests
import re

# library for discordAPI
import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_CHANNEL = os.getenv('DISCORD_DEFAULT_CHANNEL')
PREFIX = os.getenv('DISCORD_PREFIX')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

# Display the date today


def get_today():
    today = date.today()
    return today.strftime("%d/%m/%Y")

# Display icon


def get_icon():
    icons = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    return random.choice(icons) + ' '

# Get the price of petrol


def get_petrol_price():
    page = requests.get('https://webtygia.com/api/xang-dau')
    data = re.findall('<td class="text-right">(.*?)</td>', str(page.content))
    result = list(map(lambda x: x.replace('\\n', ''), data))[:-1]
    zone_1 = result[::2]
    zone_2 = result[1::2]
    zone_1.pop(4)
    zone_2.pop(4)
    #remove the last element
    product_list = ['E5 RON 92-II', 'DO 0,001S-V', 'DO 0,05S-II',
                    'Xăng RON 95-III', 'Xăng RON 95-IV', 'Xăng RON 95-V']
    print(zone_1,zone_2)
    return product_list, zone_1[:-1], zone_2[:-1]

# Play rock paper scissors


def rock_paper_scissors(player_choice):
    choice = ['kéo', 'búa', 'bao']
    computer_choice = random.choice(choice)
    player_choice = player_choice.lower()[:3]
    if player_choice == computer_choice:
        return "😾 Tao lỡ chọn " + player_choice + " rồi, hòa nha!"
    if player_choice == 'kéo':
        if computer_choice == 'búa':
            return "😸 Mài thua rồi, tao ra cái " + computer_choice + " đấy!"
        else:
            return "😾 Mài thắng rồi, tao lỡ chọn " + computer_choice + " đấy!"
    if player_choice == 'búa':
        if computer_choice == 'bao':
            return "😸 Mài thua rồi, tao ra cái " + computer_choice + " đấy!"
        else:
            return "😾 Mài thắng rồi, tao lỡ chọn " + computer_choice + " đấy!"
    if player_choice == 'bao':
        if computer_choice == 'kéo':
            return "😸 Mài thua rồi, tao ra cái " + computer_choice + " đấy!"
        else:
            return "😾 Mài thắng rồi, tao lỡ chọn " + computer_choice + " đấy!"


# Check wheather the bot is connected or not
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot is ready to use with prefix: {PREFIX}')

# say something interact with user


@bot.event
async def on_message(message):
    global on_count_number, on_count_user
    # the bot is just ignore itself
    if message.author == bot.user:
        return

    # setup and clear can be use everywhere in server
    if message.channel.name != DEFAULT_CHANNEL:
        if message.content.lower().startswith('*') or message.content.lower().startswith('meow'):
            # do nothing
            pass
        else:
            return

    # i just want to say hello you
    if message.content.lower().startswith('hello') or message.content.lower().startswith('hi'):

        msg = get_icon() + 'Hello, {0.author.mention}!'.format(message)
        await message.channel.send(msg)

    # think that i'm Tran Duc Bo
    if message.content.lower().startswith('mèo méo'):
        msg = get_icon() + 'con mèo ngu ngốc ngọt ngào đáng yêu cute phô mai que xin chào cả nhà'
        await message.channel.send(msg)

    # what does the cat say ?????
    if message.content.lower().startswith('meow') or message.content.startswith('Meow'):
        msg = get_icon() + 'gàoooooooo~'
        await message.channel.send(msg)

    # rock paper scissors
    if message.content.lower().startswith('kéo') or message.content.lower().startswith('búa') or message.content.lower().startswith('bao'):
        msg = rock_paper_scissors(message.content)
        await message.channel.send(msg)

    # this is the main message :'> but has not in dev yet
    if message.content.lower().startswith('giá xăng'):
        description = "Cập nhật lần cuối đến " + str(get_today())
        embed = discord.Embed(title="Giá xăng dầu hôm nay",
                              color=discord.Color.dark_blue(), description=description)
        product_row, price_zone1, price_zone2 = get_petrol_price()
        embed.set_author(name="Petrolimex - Tập đoàn Xăng dầu Việt Nam", url='https://www.petrolimex.com.vn/',
                         icon_url='https://files.petrolimex.com.vn/thumbnailpngs/6783dc1271ff449e95b74a9520964169/0/0/0/6e1b4cb20a6f454b8f9b9aaa0d717012/0/041118/164fb04325634d398479b716f16c2f44.png')
        embed.set_image(
            url='https://files.petrolimex.com.vn/files/6783dc1271ff449e95b74a9520964169/image=png/a934e37198c1407ab5035477efd7a920/petrolimex.png')
        embed.set_thumbnail(
            url='https://files.petrolimex.com.vn/thumbnailpngs/6783dc1271ff449e95b74a9520964169/0/0/0/6e1b4cb20a6f454b8f9b9aaa0d717012/0/041118/164fb04325634d398479b716f16c2f44.png')
        embed.add_field(name="Sản phẩm", value='\n'.join(
            product_row), inline="true")
        embed.add_field(name="Vùng 1", value=' vnd\n'.join(
            price_zone1), inline="true")
        embed.add_field(name="Vùng 2", value=' vnd\n'.join(
            price_zone2), inline="true")
        embed.add_field(name="\u200B", value='\u200B')
        embed.set_footer(text="Data là thật đó, tao éo đùa đâu. Hehe 😏",
                         icon_url='https://files.petrolimex.com.vn/thumbnailpngs/6783dc1271ff449e95b74a9520964169/0/0/0/6e1b4cb20a6f454b8f9b9aaa0d717012/0/041118/164fb04325634d398479b716f16c2f44.png')
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.command(name='meow', help='Hmm, I just wanna say hello')
async def say_hello(ctx):
    response = get_icon() + "nyan~ nyan~"
    await ctx.send(response)


@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    message = get_icon() + 'Tao cho mày nè: ' + ', '.join(dice)
    await ctx.send(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        msg = 'Mày hỏng có quyền kêu tao làm như vậy. ' + get_icon()
        await ctx.send(msg)


@bot.command(name='clear', help='Purge message with a number')
async def clear(ctx, amount=100):
    if amount > 500:
        amount = 500
    await ctx.channel.purge(limit=amount)


@bot.command(name='setup', help='Create a workspace for bot to interact')
async def create_channel(ctx, channel_name=DEFAULT_CHANNEL):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        existing_channel = discord.utils.get(guild.channels, name=channel_name)

        message = '😼 Qua ' + '<#' + \
            str(existing_channel.id) + '> chơi với tao!'
        await ctx.send(message)
    else:
        message = '😾 Tao tạo rồi, qua <#' + \
            str(existing_channel.id) + '> kiếm tao nè!'
        await ctx.send(message)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
