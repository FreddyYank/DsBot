import disnake
from disnake.ext import commands
import sqlite3
class Admin(commands.Cog):


    with sqlite3.connect("server.db") as connection:

            #__________________ECOM_ADM---------------------------

        def __int__(self, client: commands.Bot):
            self.client = client

        # ____________________________________ADM_COMMANDS---------------------------------
        @commands.slash_command(pass_context=True)
        @commands.has_permissions(administrator=True)
        async def clear(self, inter: disnake.ApplicationCommandInteraction, amount: int = 15):
            await inter.response.defer()
            deleted_messages = await inter.channel.purge(limit=amount + 1)
            await inter.send(f"{len(deleted_messages)} сообщений удалено.")


def setup(client: commands.Bot):
    client.add_cog(Admin(client))