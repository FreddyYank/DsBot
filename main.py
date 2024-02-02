import asyncio
import requests
import random
from config import settings
import sqlite3
import disnake
import folium
import datetime
from disnake.ext import commands

# --------------------------------------------MAIN-------------------------------------

client = commands.Bot(command_prefix=settings["PREFIX"],
                      help_command=None, sync_commands_debug=True,
                      intents=disnake.Intents.all())

client.remove_command("help")

hello_world = ["прив", "салам", "ку", "привет", "здравствуйте"]

HELP_COMMANDS = ["правила", "rules", "правила", "help"]

CENSORED_WORDS = [
    ""
]

situation_work = ["Вы помыли пол в учебном заведении, тем самым заработали",
                  "Вы продали найденный телефон, тем самым заработали",
                  "Вы отремонтировали машину, тем самым заработали",
                  "Вы проконсультировали клиента, тем самым заработали",
                  "Вы успешно поставили окно, тем самым заработали",
                  "Вы оказали услугу массажа, тем самым заработали",
                  "Вы разработали программу, тем самым заработали",
                  "Вы написали статью, тем самым заработали.",
                  "Вы подняли сайт в поисковых результатах, тем самым заработали.",
                  "Вы убрали снег во дворе, тем самым заработали.",
                  "Вы собрали и доставили заказ вовремя, тем самым заработали.",
                  "Вы провели монтаж электрической проводки, тем самым заработали.",
                  "Вы создали дизайн-проект для клиента, тем самым заработали.",
                  "Вы разработали и запустили сайт, тем самым заработали."]

biznas = [
    ("Автосалон", 1200000),
    ("Заправка", 1200000),
    ("Шаурмечная", 200000)

]
# ------------------------------------LOGI--------------------------------

color = disnake.Colour.random()

with sqlite3.connect("server.db") as connection:
    cursor = connection.cursor()
    @client.event
    async def on_ready():
        cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
            role_id INT,
            id INT,
            cost BIGINT

        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            id INT,
            cash BIGINT,
            rep INT,
            lvl INT,
            warn INT,
            server_id INT,
            business TEXT,
            home TEXT,
            bank BIGINT

        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS biz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price BIGINT

        )""")

        for guild in client.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                    cursor.execute(
                        f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, {guild.id},'Отсутствует','Бомж',0)")

                else:
                    pass
        connection.commit()
        await client.change_presence(activity=disnake.Game(name="*Brawl Stars*"))
        print(f".discord bot connect: {client.user}")

        b = 0
        for i in biznas:
            b += 1
            cursor.execute("SELECT id FROM biz")
            if cursor.fetchone() is None:
                cursor.executemany("INSERT INTO biz(name, price) VALUES(?,?)", biznas)
            else:
                pass


    # --------------------------------------------EVENTS-----------------------------------------



    @client.slash_command(description="Ваш профиль.")
    async def профиль(ctx):
        embe = disnake.Embed(
            title=f":coin: Баланс {ctx.author.name}",
            description="",
            colour=disnake.Colour.random()
        )
        #embe.set_thumbnail(url=f"{ctx.author.avatar_url}")

        embe.add_field(name=f":leaves:Кошелек:",
                       value=f"""`{cursor.execute("SELECT cash from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                       inline=False)
        embe.add_field(name=":homes:Дом:",
                       value=f"""`{cursor.execute("SELECT home from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                       inline=False)
        embe.add_field(name=":office:Бизнес:",
                       value=f"""`{cursor.execute("SELECT business from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                       inline=False)

        message = await ctx.send(embed=embe)


    @client.slash_command(description="Добавить роль в магазин.")
    @commands.has_permissions(administrator=True)
    async def add_role(ctx, role: disnake.Role, cost: int):
        channel1 = client.get_channel(1156681611904036970)
        if role is None:
            await channel1.send(f"<@{ctx.author.id}> Укажите роль которую желаете внести в параметре.")
        elif cost is None:
            await channel1.send(f"<@{ctx.author.id}> укажите стоимость данной роли в параметре.")
        else:
            cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))

            await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command(description="Удалить роль из магазина.")
    @commands.has_permissions(administrator=True)
    async def rem_role(ctx, role: disnake.Role):
        channel1 = client.get_channel(1156681611904036970)
        if role is None:
            await channel1.send(f"<@{ctx.author.id}> Укажите роль которую желаете удалить в параметре.")
        else:
            cursor.execute("DELETE FROM shop WHERE  role_id = {}".format(role.id))

            await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command(description="Магазин сервера.")
    async def магазин(ctx):
        embed = disnake.Embed(title='Магазин Сервера', colour=disnake.Color(0x87CEEB))
        num = 0
        embed.add_field(name=":cyclone: Роли", value="")
        for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
            if ctx.guild.get_role(row[0]) != None:
                num += 1
                embed.add_field(

                    name=f":white_small_square:{num}. Стоимость: `{row[1]}` :leaves:",
                    value=f"└ Роль: {ctx.guild.get_role(row[0]).mention}",
                    inline=False
                )
            else:
                pass
        embed.add_field(name="", value="━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)

        embed.add_field(name=":homes: Дома", value="")
        string = "Элитный класс"
        embed.add_field(name=f"{string.center(25, '━')}", value="", inline=False)

        string0 = "Средний класс"
        embed.add_field(name="", value=f"{string0.center(25, '━')}", inline=False)

        embed.add_field(name="", value="━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)

        embed.add_field(name=":office: Бизнесы", value="", inline=False)
        embed.add_field(name=":oncoming_automobile: `Автосалон`- `1.200.000` ~~¹⁷⁰⁰⁰⁰⁰~~",
                        value="Доход - от `14.000` до `20.000`", inline=False)
        embed.add_field(name=":fuelpump: `Заправка`-`1.200.000`", value="Доход - от `10.000` до `14.000`",
                        inline=False)
        embed.add_field(name=":stuffed_flatbread: `Шаурмечная`-`200.000`",
                        value="Доход - от `2.000` до `5.000`", inline=False)
        await ctx.send(embed=embed)


    @client.slash_command(description="Купить дом или бизнес.")
    async def купить(ctx, бизнес: str = None, дом: str = None):
        embe = disnake.Embed(description=f"**{ctx.author.name}** У вас недостаточно денег!")
        if дом == None and дом == None:
            await ctx.send("Вы не указали название покупаемого дома или бизнеса!")
        elif cursor.execute("SELECT business FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
            0] != 'Отсутствует':
            emb = disnake.Embed(title="", description="У вас уже есть бизнес!")
            await ctx.send(embed=emb)
        elif бизнес.lower() == "атосалон" or бизнес.lower() == "авто":
            price = 1200000
            if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] >= price:
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(price, ctx.author.id))
                cursor.execute(
                    "UPDATE users SET business = '{}' WHERE id = {}".format('Автосалон', ctx.author.id))

                emb = disnake.Embed(description="Поздравляю вы приобрели **Автосалон!**")
                await ctx.send(embed=emb)
            else:
                await ctx.send(embed=embe)
        elif бизнес.lower() == "шаурмечная" or бизнес.lower() == "шаурма":
            price = 200000
            if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] >= price:
                # cursor.execute("INSERT INTO biz(price) VALUES({}) WHERE id =".format(int(price),ctx.author.id))
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(price, ctx.author.id))
                cursor.execute(
                    "UPDATE users SET business = '{}' WHERE id = {}".format('Шаурмечная', ctx.author.id))

                emb = disnake.Embed(description="Поздравляю вы приобрели **Шаурмечную**")
                await ctx.send(embed=emb)
            else:
                await ctx.send(embed=embe)
        elif бизнес.lower() == "заправка" or бизнес.lower() == "азс":
            price = 1200000
            if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] >= price:
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(price, ctx.author.id))
                cursor.execute(
                    "UPDATE users SET business = '{}' WHERE id = {}".format('Заправка', ctx.author.id))

                emb = disnake.Embed(description="Поздравляю вы приобрели **АЗС**")
                await ctx.send(embed=emb)
            else:
                await ctx.send(embed=embe)
        else:
            emb = disnake.Embed(description=f"Бизнес под названием \"{бизнес}\" не найден")
            await ctx.send(embed=emb)


    @client.slash_command(description="Продать дом или бизнес.")
    async def продать(ctx, *,бизнес: str = None, дом: str = None):
        if бизнес is None is дом is None:
            await ctx.send("Вы не выбрали что именно вы хотите продать (дом/бизнес)")
        elif cursor.execute("SELECT users FROM business WHERE id = {}".format(ctx.author.id)).fetchone()[
            0] == "Отсутствует":
            await ctx.send("У вас нету бизнеса(Иди работай раб!)")



    @client.slash_command(description="Купить роль из магазина сервера.")
    async def купить_роль(ctx, роль: disnake.Role):
        if роль is None:
            await ctx.send(f"**{ctx.author}**, укажите роль которую вы желаете приобрести.")
        else:
            if роль in ctx.author.roles:
                await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль.")
            elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(роль.id)).fetchone()[0] > \
                    cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
                await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки данной роли")
            else:
                await ctx.author.add_roles(роль)
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(
                    cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(роль.id)).fetchone()[0],
                    ctx.author.id))

                await ctx.send(f"Вы успешно приобрели роль <@{роль.id}>")


    @client.slash_command(name="работать",description="Работать.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def работать(ctx):
        amount = random.randint(100, 500)
        situation = random.choice(situation_work)
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), ctx.author.id))

        emb = disnake.Embed(title="", description=f"{situation} **+{amount}**:leaves:", colour=disnake.Colour(0xFFE4B5))

        await ctx.send(embed=emb)



    @client.event
    async def on_slash_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            emb = disnake.Embed(title=f"",
                                description=f"Ты слишком *устал*. Вы сможете работать через **{error.retry_after.__round__()}с**.",
                                colour=disnake.Colour(0xDEB887)
                                )

            await ctx.send(embed=emb)
        else:
            pass


    @client.slash_command(description="Передать листочки.")
    async def givemoney(ctx, member: disnake.Member, amount: int):
        if amount < 10:
            await ctx.send("Минимальная сумма перевода 10 :leaves:")
        elif cursor.execute("SELECT cash FROM users WHERE id = {}  ".format(ctx.author.id)).fetchone()[
            0] < amount:
            await ctx.send('Недостаточно средств. Ваш баланс: {}'.format(
                cursor.execute("SELECT cash from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]))
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))

            user = client.get_user(member.id)

            embed = disnake.Embed(description= f"Пополнение счета на сумму: **{amount}** :leaves: от **{ctx.author.name}**",colour=disnake.Colour(0x00FF7F))
            emb = disnake.Embed(title="Переведено!", description=f"Сумма: **{amount}**",
                                 colour=disnake.Colour(0x00FF7F))

            emb.add_field(name="Получатель:", value=f"{member.name}")
            await ctx.send(embed=emb)
            await user.send(embed=embed)


    @client.slash_command(description="Орел и Решка")
    async def монетка(ctx, orel: str, coin: int):
        gg = random.randint(0, 100)
        monet = ""
        print(gg)
        if gg <= 40:
            monet = "орел"
        else:
            monet = "решка"
        print(monet)
        emb = disnake.Embed(title="Орел и Решка", description=f"Ставка:{coin} :leaves:")
        emb.add_field(name=f"Ваше предположение: {orel}", value=f"Итог: {str(monet)}", inline=False)
        emb.add_field(name=":green_circle: Итог игры :green_circle:",
                      value=f":green_square: Победа(+{coin}) :green_square:")
        if orel is None:
            await ctx.send(f"{ctx.author.name} вы не выбрали сторону монеты.")
        elif coin < 10:
            await ctx.send("Минимальная сумма ставки **100** :leaves:")
        elif coin is None:
            await ctx.send(f"{ctx.author.name} вы не указали сумму ставки.")
        elif coin > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send("У вас нет стольки денег.")
        else:
            if orel.lower() == "орёл" or orel.lower() == "орел" and monet == "орел":
                await ctx.send(embed=emb)
                cursor.execute(
                    "UPDATE users SET cash = cash + {} WHERE id = {}".format(int(coin), ctx.author.id))

            elif orel.lower() == "решка" and monet == "решка":
                await ctx.send(embed=emb)
                cursor.execute(
                    "UPDATE users SET cash = cash + {} WHERE id = {}".format(int(coin), ctx.author.id))

            else:
                emb = disnake.Embed(title="Орел и Решка", description=f"Ставка:{coin} :leaves:")
                emb.add_field(name=f"Ваше предположение: {orel}", value=f"Итог: {str(monet)}", inline=False)
                emb.add_field(name=":red_circle: Итог игры :red_circle:",
                              value=f":red_square: Поражение(- {coin}):red_square:")
                await ctx.send(embed=emb)
                cursor.execute(
                    "UPDATE users SET cash = cash - {} WHERE id = {}".format(int(coin), ctx.author.id))


    @client.slash_command(description="Ограбить друга.")
    async def ненадодядя(ctx, member: disnake.Member):
        mon1 = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
        mon2 = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        print(mon2 + mon1)
        money = random.randint(mon2, mon1)
        #print(money)
        if member is None:
            await ctx.send("Вы не указали пользователя которого хотите **ограбить!**")
        elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0] < 50:
            await ctx.send("Для ограбления данного пользователя у него должно быть хотя бы 50 :leaves: ")
        else:
            await ctx.send(f"Вы успешно ограбили **{member.name}** | +{money}")
        print(mon1, mon2)


    @client.slash_command(description="Лучшие по кол-ву листочков.")
    async def лидеры(ctx):
        embed = disnake.Embed(title='Топ 10 пользователей по :leaves: сервера')
        counter = 0

        for row in cursor.execute(
                "SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(
                    ctx.guild.id)):
            counter += 1
            embed.add_field(
                name=f'# {counter} | `{row[0]}`',
                value=f'Баланс: {row[1]}:leaves:',
                inline=False
            )

        mess = await ctx.send(embed=embed)
        ross = client.get_emoji('🔱')
        await mess.add_reaction(ross)


    @client.slash_command(description="Информация по бизнесу.")
    async def бизнес(ctx):
        if cursor.execute("SELECT business FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
            0] == 'Отсутствует':
            emb = disnake.Embed(description="У вас нету бизнеса.")
            await ctx.send(embed=emb)
        else:
            emb = disnake.Embed(title="Меню бизнеса",
                                description=f"Бизнес: {cursor.execute(f'SELECT business FROM users WHERE id = {ctx.author.id}').fetchone()[0]}")
            await ctx.send(embed=emb)

    @client.slash_command()
    async def банк(ctx):
        await ctx.send(f"""`{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""")


    # @commands.slash_command()
    # @commands.has_permissions(administrator=True)
    # async def take(ctx, member: disnake.Member, amount):
    #     channel = client.get_channel(1156681611904036970)
    #     if member is None:
    #         await channel.send(
    #             f"<@{ctx.author.id}> вы не указали пользователя у которого хотите забрать *листочки* ")
    #     elif amount is None:
    #         await channel.send(f"<@{ctx.author.id}> вы не указали кол-во забираемых листочков! ")
    #     elif amount == "all":
    #         cash = cursor.execute(f"SELECT cash FROM users WHERE id = {member.id}").fetchone()[0]
    #         cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(cash, member.id))
    #         await channel.send("Успешно!")
    #     elif int(amount) < 1:
    #         await ctx.send(f"**{ctx.author.name}** укажите сумму больше **0** ")
    #     else:
    #         cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
    #
    # @commands.slash_command()
    # @commands.has_permissions(administrator=True)
    # async def award(ctx, member: disnake.Member, amount):
    #     channel1 = client.get_channel(1156681611904036970)
    #     if member is None:
    #         await channel1.send(
    #             f"<@{ctx.author.id}> вы не указали пользователя которому хотите выдать *листочки* :leaves:")
    #     elif amount is None:
    #         await ctx.send(f"<@{ctx.author.id}> вы не указали кол-во выдаваемых листочков! :leaves:")
    #     elif int(amount) < 1:
    #         await channel1.send(f"<@{ctx.author.id}> укажите сумму больше **0** ")
    #     else:
    #         cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), member.id))
    #         cursor.connection.commit()
    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def award(ctx, member: disnake.Member, amount):
        channel1 = client.get_channel(1156681611904036970)
        if member is None:
            await channel1.send(
                f"<@{ctx.author.id}> вы не указали пользователя которому хотите выдать *листочки* :leaves:")
        elif amount is None:
            await ctx.send(f"<@{ctx.author.id}> вы не указали кол-во выдаваемых листочков! :leaves:")
        elif int(amount) < 1:
            await channel1.send(f"<@{ctx.author.id}> укажите сумму больше **0** ")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
            await channel1.send(f"<@{ctx.author.id}> Успешно! ")


    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def take(ctx, member: disnake.Member, amount):
        channel = client.get_channel(1156681611904036970)
        if member is None:
            await channel.send(
                f"<@{ctx.author.id}> вы не указали пользователя у которого хотите забрать *листочки* ")
        elif amount is None:
            await channel.send(f"<@{ctx.author.id}> вы не указали кол-во забираемых листочков! ")
        elif amount == "all":
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
            await channel.send("Успешно!")

        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author.name}** укажите сумму больше **0** ")
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
            await ctx.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил."):
        channel1 = client.get_channel(1156681611904036970)
        channel = client.get_channel(1133146191073390663)
        now_date = datetime.datetime.now()
        emb = disnake.Embed(title="", colour=disnake.Colour(0xFF7F50))
        emb.add_field(name="", value=f"Участник: **{member.name}**(<@{member.id}>) был *кикнут*!", )
        emb.add_field(name="Модератор", value=f"**.{ctx.author.name}**(<@{ctx.author.id}>)", inline=False)
        emb.add_field(name="Причина:", value=f"`{reason}`", inline=True)
        emb.set_footer(icon_url=f"{member.avatar.url}", text=f"id участника: {member.id} • {now_date}")
        await member.kick(reason=reason)
        await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command(name="ban", aliases=["Бан", "банн"])
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил."):
        channel1 = client.get_channel(1156681611904036970)
        channel = client.get_channel(1133146191073390663)
        now_date = datetime.datetime.now()
        emb = disnake.Embed(title="", colour=disnake.Colour(0xFF7F50))
        emb.add_field(name="", value=f"Участник: **{member.name}**(<@{member.id}>) был *забанен*!", )
        emb.add_field(name="Модератор", value=f"**.{ctx.author.name}**(<@{ctx.author.id}>)")
        emb.add_field(name="Причина:", value=f"`{reason}`", inline=True)
        emb.set_footer(icon_url=f"{member.avatar.url}", text=f"id участника: {member.id} • {now_date}")
        await channel.send(embed=emb)
        await member.ban(reason=reason)
        await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def mute(ctx, member: disnake.Member, *, reason="Нарушение правил.", link):
        channel1 = client.get_channel(1156681611904036970)
        role = disnake.utils.get(member.guild.roles, id=1133146740338458686)
        channel = client.get_channel(1133147090210541690)
        now_date = datetime.datetime.now()

        emb = disnake.Embed(title="", colour=disnake.Colour(0xE9967A))
        emb.add_field(name="", value=f"Участник: **{member.name}**(<@{member.id}>) был *замьючен*!", inline=False)
        emb.add_field(name="Модератор", value=f"**.{ctx.author.name}**(<@{ctx.author.id}>)", )
        emb.add_field(value=f"[Перейти]({link})", name="Сообщение")
        emb.add_field(name="Длительность:", value="time", inline=False)
        emb.add_field(name="Причина:", value=f"`{reason}`", inline=False)
        emb.set_footer(icon_url=f"{member.avatar.url}", text=f"id участника: {member.id} • {now_date}")
        inte = len(reason)
        if inte < 15:
            await channel1.send(f"<@{ctx.author.id}> Кол-во символов в `reason` должно быть `не менее 15`.")
        elif "https://discord.com/channels/" not in link:
            await channel1.send(f"<@{ctx.author.id}> Укажите ссылку на сообщение в параметре `link`.")

        else:
            await member.add_roles(role)
            await channel.send(embed=emb)
            await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def warn(ctx, member: disnake.Member, *, reason="Нарушение правил."):
        channel1 = client.get_channel(1156681611904036970)
        channel = client.get_channel(1156316627671994388)
        inte = len(reason)
        cursor.execute("UPDATE users SET warn = warn + 1 WHERE id = {}".format(member.id))
        connection.commit()
        now_date = datetime.datetime.now()
        emb = disnake.Embed(title="", colour=disnake.Colour(0xFF7F50))
        emb.add_field(name="",
                      value=f"""Участник: **{member.name}**(<@{member.id}>) получил предупреждение! (**{cursor.execute("SELECT warn from users WHERE id = {}".format(member.id)).fetchone()[0]}**/3)""")
        emb.add_field(name="Модератор", value=f"**.{ctx.author.name}**(<@{ctx.author.id}>)", inline=False)
        emb.add_field(name="Причина:", value=f"`{reason}`", inline=True)
        emb.set_footer(icon_url=f"{member.avatar.url}", text=f"id участника: {member.id} • {now_date}")
        await channel.send(embed=emb)
        await channel1.send(f"<@{ctx.author.id}> Успешно!")
        if cursor.execute("SELECT warn FROM users WHERE id = {}".format(member.id)).fetchone()[0] >= 3:
            reason = "3 варна."
            channel1 = client.get_channel(1156681611904036970)
            channel = client.get_channel(1133146191073390663)
            now_date = datetime.datetime.now()
            emb = disnake.Embed(title="", colour=disnake.Colour(0xFF7F50))
            emb.add_field(name="", value=f"Участник: **{member.name}**(<@{member.id}>) был *забанен*!", )
            emb.add_field(name="Модератор", value=f"**.{ctx.author.name}**(<@{ctx.author.id}>)")
            emb.add_field(name="Причина:", value=f"`{reason}`", inline=True)
            emb.set_footer(icon_url=f"{member.avatar.url}", text=f"id участника: {member.id} • {now_date}")
            await channel.send(embed=emb)
            await member.ban(reason="3 варна.")
            await channel1.send(f"<@{ctx.author.id}> Успешно!")


    @client.slash_command()
    @commands.has_permissions(administrator=True)
    async def unwarn(ctx, member: disnake.Member):
        channel1 = client.get_channel(1156681611904036970)
        channel = client.get_channel(1133146191073390663)
        if cursor.execute("SELECT warn FROM users WHERE id = {}".format(member.id)).fetchone()[0] < 1:
            await ctx.send("У данного пользователя не имеется варнов!")
        else:
            cursor.execute("UPDATE users SET warn = warn - 1 WHERE id = {}".format(member.id))
            connection.commit()
            await channel1.send(f"<@{ctx.author.id}> Успешно!")

    @client.slash_command(description="Пробить по ip.")
    async def ip(ctx, ip="127.0.0.1"):
        try:
            response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
            # print(response)

            data = {
                '[IP]': response.get('query'),
                '[Инт.провайдер]': response.get('isp'),
                '[Организация]': response.get('org'),
                '[Страна]': response.get('country'),
                '[Регион]': response.get('regionName'),
                '[Город]': response.get('city'),
                '[Индекс]': response.get('zip'),
                '[Широта]': response.get('lat'),
                '[Долгота]': response.get('lon'),
            }

            emb = disnake.Embed(title="Успешно!",colour=disnake.Colour.blurple())
            for k, v in data.items():
                emb.add_field(name="", value=f"**{k}**: {v}",inline=False)

            area = folium.Map(location=[response.get('lat'),response.get('lon')])
            a = area.save(f"ip_adress\{ctx.author.name}_{response.get('query')}_{response.get('country')}.html")

            await ctx.send("Расположение на карте:",file = disnake.File(f"ip_adress\{ctx.author.name}_{response.get('query')}_{response.get('country')}.html"))
            await ctx.send(embed=emb)

        except requests.exceptions.ConnectionError:
            await ctx.send("Ошибка.")


        # ---------------------Connect----------------

    client.load_extension("cogs.admin")
    client.load_extension("cogs.ping")
    client.load_extension("cogs.events")
    client.load_extension("cogs.rules")
    client.run(settings["TOKEN"])



