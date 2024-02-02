import disnake
from disnake.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.color = disnake.Color.random()
    @commands.slash_command(description="Пингануть бота.")
    async def пинг(self, inter: disnake.ApplicationCommandInteraction):
        """Получить текущую задержку бота."""
        await inter.response.send_message(f"Пинг: {round(self.client.latency * 1000)}мс")

    @commands.slash_command(description="Аватарка участника.")
    async def аватар(self,ctx, member: disnake.Member):
        url = member.avatar.url
        emb = disnake.Embed(title=f"{member.name}", colour= self.color)
        emb.set_image(url=f"{url}")
        await ctx.send(embed=emb)

def setup(client: commands.Bot):
    client.add_cog(PingCommand(client))