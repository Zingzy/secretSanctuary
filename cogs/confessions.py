import datetime
import random
import uuid

import discord
from discord import app_commands, ui
from discord.ext import commands

from utils import (
    confession_gifs,
    load_confessions,
    save_confession,
    waiting_gifs,
    random_pfp,
)


class ConfessModal(ui.Modal, title="Spill the tea ☕"):
    confession = ui.TextInput(
        label="👉 Literally anything you want!",
        style=discord.TextStyle.paragraph,
        max_length=4000,
        placeholder="💬 I would like confess that I ...",
        min_length=20,
    )

    async def on_submit(self, interaction: discord.Interaction):
        data = load_confessions()

        id = str(uuid.uuid4())[:8]
        identifier = random.randint(1000, 10000)

        data[id] = {
            "confession": self.confession.value,
            "date": datetime.date.today().strftime("%B %d, %Y"),
            "time_gmt": datetime.datetime.utcnow().strftime("%H:%M:%S"),
            "author": f"AnonymousUser#{identifier}",
        }

        save_confession(data)

        embed = discord.Embed(
            description="# Your secret is safe with us! 😉",
            color=discord.Color.og_blurple(),
        )

        embed.add_field(name="Confession ID", value=f"`{id}`", inline=False)
        embed.add_field(
            name="Confession Date",
            value=datetime.date.today().strftime("%B %d, %Y"),
            inline=False,
        )
        embed.add_field(
            name="You can view your confession here",
            value="https://confessions.idk.com",
            inline=False,
        )

        embed.set_image(url=random.choice(confession_gifs))
        embed.set_footer(
            text=f"Confessed by AnonymousUser#{identifier}",
            icon_url=interaction.user.avatar,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class AnonymousConfessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.tree.command(
        name="explore-confessions",
        description="Explore Random Anonymous Secrets",
    )
    @app_commands.describe(private="Would send you messages privately if enabled")
    async def discover(interaction, private: bool = False):
        data = load_confessions()
        ch = random.choice(list(data.keys()))
        pfp = random_pfp()

        embed = discord.Embed(
            title=f"Confession by {data[ch]['author']}",
            color=discord.Color.random(),
            description=data[ch]["confession"] + "\n",
        )

        embed.set_footer(
            text=f"Information requested by {interaction.user}",
            icon_url=interaction.user.avatar,
        )

        embed.set_thumbnail(url=pfp)

        embed.add_field(name="📅 Confession Date", value=data[ch]["date"])
        embed.add_field(name="🔢 Confession Id", value=f"`{ch}`")

        await interaction.response.send_message(embed=embed, ephemeral=private)

    @app_commands.command(
        name="confess", description="Submit a confession anonymously 🤫"
    )
    @app_commands.checks.cooldown(1, 3600.0)
    async def confessions(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ConfessModal())

    @confessions.error
    async def on_your_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            end_time = datetime.datetime.now() + datetime.timedelta(
                seconds=error.retry_after
            )
            end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
            end_time_ts = f"<t:{int(end_time.timestamp())}>"

            hours, remainder = divmod(error.retry_after, 3600)
            minutes, seconds = divmod(remainder, 60)
            seconds = round(seconds)
            time_left = f"{hours+' hour, ' if not hours<1 else ''}{int(minutes)} minute{'s' if minutes != 1 else ''} and {seconds} second{'s' if seconds != 1 else ''}"

            embed = discord.Embed(
                title="⏳ Cooldown",
                description=f"You have to wait until **{end_time_ts}** ({time_left}) before submitting another confession.",
                color=discord.Color.red(),
            )
            embed.set_image(url=random.choice(waiting_gifs))

            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AnonymousConfessions(bot))
    print("Anonymous Confessions Sumbitter is loaded")
