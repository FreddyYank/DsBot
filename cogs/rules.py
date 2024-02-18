import disnake
from disnake.ext import commands
import datetime

class Rules(commands.Cog):
        def __int__(self, client:commands.Bot):

            self.client = client

        @commands.slash_command()
        @commands.has_permissions(administrator=True)
        async def rules(self,ctx):
            emb = disnake.Embed(title="Правила Discord-сервера  Delta Squad ||",
                                description="САВА ЛОХ:",
                                colour=disnake.Colour.orange())
            emb.add_field(name=" 1.1 | Рекламы сторонних ресурсов.",
                          value="Наказание: Блокировка навсегда.",
                          inline=False)
            emb.add_field(
                name=" 1.2 | Распространение личной информации без согласия.",
                value=" Наказание: Блокировка чата на день -> блокировка навсегда.")
            emb.add_field(
                name=" 1.3 | Запрещено выдавать себя за администрацию сервера.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 час.",
                inline=False)
            emb.add_field(name=" 1.4 | Запрещено распространять читы / вирусы.",
                          value=" Наказание: Блокировка навсегда.",
                          inline=False)
            emb.add_field(
                name=
                " 1.5 | Запрещен открытый скептицизм, имеющий цель призвать подписчиков сообщества не играть на проекте или же имеющий цель убедить разработчиков проекта в нецелесообразности открытия существования проекта.",
                value=" Наказание: Блокировка чата на 1 день -> блокировка навсегда.",
                inline=False)
            emb.add_field(
                name=
                " 1.6 | Запрещено провоцировать пользователей на нарушения настоящих правил в любой форме.",
                value=" Наказание: Предупреждение -> блокировка чата на 3 часа.",
                inline=False)

            emb.add_field(
                name=" 1.7 | Запрещено ввести политические разговоры.",
                value=" Наказание: Блокировка чата на 3 дня -> блокировка навсегда.",
                inline=False)
            emb.add_field(
                name=
                "1.8 | Оскорблять и дискриминировать участников и сторонних лиц по любому признаку (национальному, половому, религиозному, расовому, возрастному, профессиональному или по любым другим признакам) без ведомой на то причины.",
                value=" Наказание: Блокировка чата на 1 час.",
                inline=False)
            emb.add_field(
                name=
                "1.9 | Флудить / спамить, а так же писать бессмысленный текст для поднятия ранга.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 час.",
                inline=False)
            emb.add_field(
                name="2.0 | Постоянно писать Caps Lock-om.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 час.",
                inline=False)
            emb.add_field(
                name="2.1 | Упоминание игроков / ролей без надобности.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 день.",
                inline=False)
            emb.add_field(name="",
                          value="ВО ВСЕХ ГОЛОСОВЫХ ЧАТАХ ЗАПРЕЩЕНО:",
                          inline=False)
            emb.add_field(name="2.2 | Оскорбления.",
                          value=" Наказание: Блокировка чата на 1 час.",
                          inline=False)
            emb.add_field(
                name="2.3 | Крики и создание сторонних шумов.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 час.",
                inline=False)
            emb.add_field(
                name="2.4 | Неадекватное поведение.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 день.",
                inline=False)
            emb.add_field(
                name="2.5 | Транслирование музыки без согласия всех участников канала.",
                value=" Наказание: Предупреждение -> блокировка чата на 1 час.",
                inline=False)
            emb.add_field(
                name=
                "2.6 | Запрещено забирать музыкального бота и применять его команды, если он используется другим.",
                value=" Наказание: Предупреждение -> Бан!",
                inline=False)
            emb.add_field(name="", value="", inline=False)

            emb.set_author(
                name=f"{ctx.author.name}",
                icon_url=
                "https://sun6-21.userapi.com/s/v1/ig2/uwFB8IpumwRbiomR7TP9R8Tos6q1mnXR0Ki7p7wu2hwZUdlU9Dd_El6L_y2lG83HYXKY2q9e4sJUabuvM9TAqgPR.jpg?size=2545x2545&quality=95&crop=0,14,2545,2545&ava=1"
            )

            emb.set_image(
                "https://media.discordapp.net/attachments/984771008491814932/1108768829099737168/wonder.gif"
            )
            emb.set_footer(
                text="Последние изменения: 09-06-2023 [20:12:36.526787PM]",
                icon_url=
                "https://cdn.discordapp.com/attachments/1082773835050393741/1137104553699987627/8488ac92078829.png"
            )

            emba = disnake.Embed(title="Короче!", colour=disnake.Colour.blue())
            emba.add_field(name="Читы -> Бан", value="", inline=False)
            emba.add_field(name="Кемперство -> Бан", value="", inline=False)
            emba.add_field(name="Оскорбление -> Бан", value="")
            emba.add_field(name="Оскорбление администрации -> Расстрел, потом БАН!",
                           value="",
                           inline=False)
            emba.add_field(name="Всем все понятно??",
                           value="Всем удачи!:)",
                           inline=False)

            # channel = client.get_channel(1065375494448615544)
            # await channel.send(embed=emb)

            await ctx.send(embed=emba)

def setup(client: commands.Bot):
    client.add_cog(Rules(client))
