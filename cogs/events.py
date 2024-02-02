import disnake
from disnake.ext import commands
from main import CENSORED_WORDS, HELP_COMMANDS, cursor,client
import sqlite3

class event(commands.Cog):

    def __init__(self, client: commands.Bot):
            self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0, 0, 0, {member.guild.id})")
        else:
            pass

        role = disnake.utils.get(member.guild.roles, name="Recruit")
        channel = client.get_channel(1077945182848294912)
        emb = disnake.Embed(title="", description="Приветствуем тебя!")
        emb.set_author(icon_url=f"{member.avatar.url}", name=f"{member.name}")
        emb.set_image(
            url="https://cdn.discordapp.com/attachments/1155259038557290567/1158027607841976350/image.png?ex=651ac0c0&is=65196f40&hm=dc1645ea5738088938073ba65449cd14460793265722771136048fc5ef2ae22c&")
        await channel.send(embed=emb)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = client.get_channel(1077945182848294912)
        emb = disnake.Embed(title="")
        emb.set_author(name=f"{member.name}")
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message(self, message):
        for content in message.content.split():
            for help_commands in HELP_COMMANDS:
                if content.lower() == help_commands:
                    emb = disnake.Embed(title="Правила дискорд сервера")
                    await message.delete()
                    await message.channel.send(embed=emb)

        for content in message.content.split():
            for censored_word in CENSORED_WORDS:
                if content.lower() == censored_word:
                    await message.delete()
                    await message.channel.send(f" Ай-йя-йяй {message.author.mention}")
        await client.process_commands(message)


def setup(client: commands.Bot):
    client.add_cog(event(client))