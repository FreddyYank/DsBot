import disnake
from disnake.ext import commands
import sqlite3
import random
from main import cursor
from main import client
from main import situation_work




import disnake
from disnake.ext import commands
import sqlite3
import datetime

from main import cursor
from main import client
class Ecom(commands.Cog):
    def __int__(self, client:commands.Bot):
        self.client = client
        #__________________ECOM_ADM---------------------------

    with sqlite3.connect("server.db") as connection:
        @commands.slash_command()
        async def prof(self, ctx):
            embe = disnake.Embed(
                title=f":coin: Баланс {ctx.author.name}",
                description=""
            )
            embe.add_field(name=f":leaves:Кошелек:",
                           value=f"""`{cursor.execute("SELECT cash from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                           inline=False)
            embe.add_field(name=":homes:Дом:",
                           value=f"""`{cursor.execute("SELECT home from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                           inline=False)
            embe.add_field(name=":office:Бизнес:",
                           value=f"""`{cursor.execute("SELECT business from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`""",
                           inline=False)

            await ctx.send(embed=embe)

        @commands.slash_command()
        @commands.has_permissions(administrator=True)
        async def add_role(self, ctx, role: disnake.Role, cost: int):
            channel1 = client.get_channel(1156681611904036970)
            if role is None:
                await channel1.send(f"<@{ctx.author.id}> Укажите роль которую желаете внести в параметре.")
            elif cost is None:
                await channel1.send(f"<@{ctx.author.id}> укажите стоимость данной роли в параметре.")
            else:
                cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))

                await channel1.send(f"<@{ctx.author.id}> Успешно!")

        @commands.slash_command()
        @commands.has_permissions(administrator=True)
        async def rem_role(self, ctx, role: disnake.Role):
            channel1 = client.get_channel(1156681611904036970)
            if role is None:
                await channel1.send(f"<@{ctx.author.id}> Укажите роль которую желаете удалить в параметре.")
            else:
                cursor.execute("DELETE FROM shop WHERE  role_id = {}".format(role.id))

                await channel1.send(f"<@{ctx.author.id}> Успешно!")

        @commands.slash_command()
        async def shop(self, ctx):
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
            embed.add_field(name="", value=f"{string0:━>20}", inline=False)

            embed.add_field(name="", value="━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)

            embed.add_field(name=":office: Бизнесы", value="", inline=False)
            embed.add_field(name=":oncoming_automobile: `Автосалон`- `1.200.000` ~~¹⁷⁰⁰⁰⁰⁰~~",
                            value="Доход - от `14.000` до `20.000`", inline=False)
            embed.add_field(name=":fuelpump: `Заправка`-`1.200.000`", value="Доход - от `10.000` до `14.000`",
                            inline=False)
            embed.add_field(name=":stuffed_flatbread: `Шаурмечная`-`200.000`",
                            value="Доход - от `2.000` до `5.000`", inline=False)
            await ctx.send(embed=embed)

        @commands.slash_command()
        async def buy(self, ctx, biz: str = None, home: str = None):
            embe = disnake.Embed(description=f"**{ctx.author.name}** У вас недостаточно денег!")
            if biz == None and home == None:
                await ctx.send("Вы не указали название покупаемого дома или бизнеса!")
            elif cursor.execute("SELECT business FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] != 'Отсутствует':
                emb = disnake.Embed(title="", description="У вас уже есть бизнес!")
                await ctx.send(embed=emb)
            elif biz.lower() == "атосалон" or biz.lower() == "авто":
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
            elif biz.lower() == "шаурмечная" or biz.lower() == "шаурма":
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
            elif biz.lower() == "заправка" or biz.lower() == "азс":
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
                emb = disnake.Embed(description=f"Бизнес под названием \"{biz}\" не найден")
                await ctx.send(embed=emb)

        @commands.slash_command()
        async def sold(self, ctx, biz: str = None, home: str = None):
            if biz is None is home is None:
                await ctx.send("Вы не выбрали что именно вы хотите продать (дом/бизнес)")
            elif cursor.execute("SELECT users FROM business WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] == "Отсутствует":
                await ctx.send("У вас нету бизнеса(Иди работай раб!)")

        @commands.slash_command()
        async def buy_role(self, ctx, role: disnake.Role):
            if role is None:
                await ctx.send(f"**{ctx.author}**, укажите роль которую вы желаете приобрести.")
            else:
                if role in ctx.author.roles:
                    await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль.")
                elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
                        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
                    await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки данной роли")
                else:
                    await ctx.author.add_roles(role)
                    cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(
                        cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
                        ctx.author.id))

                    await ctx.send(f"Вы успешно приобрели роль <@{role.id}>")

        @commands.slash_command()
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def work(self, ctx):
            amount = random.randint(100, 500)
            situation = random.choice(situation_work)
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), ctx.author.id))

            emb = disnake.Embed(title="", description=f"{situation} **+{amount}**:leaves:")

            await ctx.send(embed=emb)

        @commands.slash_command()
        async def avatar(self, ctx, member: disnake.Member):

            emb = disnake.Embed(title=f"{member.name}", colour=disnake.Colour.random())
            emb.set_image(url=f"{member.avatar.url}")
            await ctx.send(embed=emb)

        @commands.event
        async def on_slash_command_error(self, ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                emb = disnake.Embed(title=f"",
                                    description=f"Ты слишком *устал*. Вы сможете работать через **{error.retry_after.__round__()}с**.")
                await ctx.send(embed=emb)
            else:
                pass

        @commands.slash_command()
        async def givemoney(self, ctx, member: disnake.Member, amount: int):
            if amount < 10:
                await ctx.send("Минимальная сумма перевода 10 :leaves:")
            elif cursor.execute("SELECT cash FROM users WHERE id = {}  ".format(ctx.author.id)).fetchone()[
                0] < amount:
                await ctx.send('Недостаточно средств. Ваш баланс: {}'.format(
                    cursor.execute("SELECT cash from users WHERE id = {}".format(ctx.author.id)).fetchone()[0]))
            else:
                cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
                cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))

                emb = disnake.Embed(title="Переведено!", description=f"Сумма: **{amount}**",
                                    colour=disnake.Colour(0x00FF7F))
                emb.add_field(name="Получатель:", value=f"{member.name}")
                await ctx.send(embed=emb)

        @commands.slash_command()
        async def monetka(self, ctx, orel: str, coin: int):
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

        @commands.slash_command()
        async def rob(self, ctx, member: disnake.Member):
            mon1 = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
            mon2 = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            # print(mon2, mon1)
            money = random.randint(mon2, mon1)

            if member is None:
                await ctx.send("Вы не указали пользователя которого хотите **ограбить!**")
            elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0] < 50:
                await ctx.send("Для ограбления данного пользователя у него должно быть хотя бы 50 :leaves: ")
            else:
                await ctx.send(f"Вы успешно ограбили **{member.name}** | +{money}")
            print(mon1, mon2)

        @commands.slash_command()
        async def leaderboard(self, ctx):
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

        @commands.slash_command()
        async def biz(self, ctx):
            if cursor.execute("SELECT business FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                0] == 'Отсутствует':
                emb = disnake.Embed(description="У вас нету бизнеса.")
                await ctx.send(embed=emb)
            else:
                emb = disnake.Embed(title="Меню бизнеса",
                                    description=f"Бизнес: {cursor.execute(f'SELECT business FROM users WHERE id = {ctx.author.id}').fetchone()[0]}")
                await ctx.send(embed=emb)

def setup(client: commands.Bot):
    client.add_cog(Ecom(client))