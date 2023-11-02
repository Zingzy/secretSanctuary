import discord
from discord import ui, app_commands
from discord.ext import commands
from utils import mongo, suggestion_gifs, feedback_gifs, random_pfp, insert_suggestion, insert_feedback
import random

class SuggestionModal(ui.Modal, title="contact mods without them knowing who you are"):
    suggestion = ui.TextInput(
        label="👉 Literally anything you want!",
        style=discord.TextStyle.paragraph,
        max_length=4000,
        placeholder="💬 I would like to suggest that ...",
        min_length=20,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel = interaction.guild.get_channel(server["suggestion_channel"])
        embed = discord.Embed(
            description=self.suggestion.value,
            color=discord.Color.og_blurple(),
        )

        author = f"AnonymousUser#{random.randint(1000, 10000)}"

        embed.set_author(name=author)
        embed.set_thumbnail(url="https://media2.giphy.com/media/EEbiK7EP3ohrNXQIc1/giphy.gif?cid=ecf05e47952vhkf0meyq1yogmi7cagsmnk04ji3t3xzd3ss8&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        embed.set_footer(text="Anonymous Suggestion")
        await channel.send(embed=embed)
        insert_suggestion(server_id=interaction.guild.id, suggestion=self.suggestion.value)

        embed2 = discord.Embed(
            description="Your anonymous suggestion has been successfully made !",
            color=discord.Color.og_blurple(),
        )
        embed2.set_image(url=random.choice(suggestion_gifs))
        embed2.set_footer(text="Anonymous Suggestion")
        await interaction.response.send_message(embed=embed2, ephemeral=True)


class FeedbackModal(ui.Modal, title="contact mods without them knowing who you are"):
    feedback = ui.TextInput(
        label="👉 Literally anything you want!",
        style=discord.TextStyle.paragraph,
        max_length=4000,
        placeholder="💬 I would like to suggest that ...",
        min_length=20,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel = interaction.guild.get_channel(server["feedback_channel"])
        embed = discord.Embed(
            description=self.feedback.value,
            color=discord.Color.og_blurple(),
        )

        author_name = f"anonymousUser#{random.randint(1000, 10000)}"

        embed.set_author(name=author_name)
        embed.set_footer(text="Anonymous Feedback")
        embed.set_thumbnail(url="https://media0.giphy.com/media/9xmjP6FkdINCA6Ucp4/giphy.gif?cid=ecf05e47z0fiascm1vdb3dfk91iq68hvbousm205bgkq7dkv&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        await channel.send(embed=embed)
        insert_feedback(server_id=interaction.guild.id, feedback=self.feedback.value)

        embed2 = discord.Embed(
            description="Your anonymous feedback has been successfully made !",
            color=discord.Color.og_blurple(),
        )
        embed2.set_image(url=random.choice(feedback_gifs))
        embed2.set_footer(text="Anonymous Feedback")
        await interaction.response.send_message(embed=embed2, ephemeral=True)


class AnonymousSuggestion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="suggest",
        description="Suggest anything you want",
    )
    # @app_commands.checks.cooldown(1, 3600.0)
    async def suggest(self, interaction: discord.Interaction):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        if not server:
            await interaction.response.send_message(embed=discord.Embed(title="No suggestion channel set", description="Ask the server mods to set up the feedback channel", color=discord.Color.red() ))
            return
        if server["suggestion_channel"] is None:
            await interaction.response.send_message(embed=discord.Embed(title="No suggestion channel set", description="Ask the server mods to set up the feedback channel", color=discord.Color.red() ))
            return
        await interaction.response.send_modal(SuggestionModal())

    @app_commands.command(
        name="feedback",
        description="Suggest anything you want",
    )
    # @app_commands.checks.cooldown(1, 3600.0)
    async def feedback(self, interaction: discord.Interaction):
        # await interaction.response.defer()
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        if not server:
            await interaction.response.send_message(embed=discord.Embed(title="No feedback channel set", description="Ask the server mods to set up the feedback channel", color=discord.Color.red() ), ephemeral=True)
            return
        if server["feedback_channel"] is None:
            await interaction.response.send_message(embed=discord.Embed(title="No feedback channel set", description="Ask the server mods to set up the feedback channel", color=discord.Color.red() ), ephemeral=True)
            return
        await interaction.response.send_modal(FeedbackModal())

    @app_commands.command()
    @app_commands.default_permissions(administrator=True)
    async def suggestion_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        await interaction.response.defer()
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel_id = None
        if channel is not None:
            channel_id = channel.id
        schema = {
            "_id": interaction.guild.id,
            "suggestion_channel": channel_id,
            "feedback_channel": None,
            "feedbacks": [],
            "suggestions": [],
        }

        if not server:
            db.insert_one(schema)
            if channel is None:
                await interaction.followup.send(
                    "set suggestion channel to None"
                )
                return
            await interaction.followup.send(
                f"set suggestion channel to {channel.mention}"
            )
            return

        if channel is None:
            db.update_one(
                {"_id": interaction.guild.id}, {"$set": {"suggestion_channel": None}}
            )
            await (interaction.followup.send("set suggestion channel to None"))
            return
        db.update_one(
            {"_id": interaction.guild.id}, {"$set": {"suggestion_channel": channel.id}}
        )

        await interaction.followup.send(embed=discord.Embed(title="Suggestion channel set ✨", description="You can now use the /suggest command", color=discord.Color.green() ), ephemeral=True)

    @suggestion_channel.error
    async def suggestion_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.followup.send(embed=discord.Embed(title="Missing permissions", description="You need to be an administrator to use this command", color=discord.Color.red() ), ephemeral=True)
            return

    @app_commands.command()
    @app_commands.default_permissions(administrator=True)
    async def feedback_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        await interaction.response.defer()
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel_id = None
        if channel is not None:
            channel_id = channel.id
        schema = {
            "_id": interaction.guild.id,
            "suggestion_channel": None,
            "feedback_channel": channel_id,
            "feedbacks": [],
            "suggestions": [],
        }

        if not server:
            db.insert_one(schema)
            if channel is None:
                await interaction.followup.send("set feedback channel to None")
                return
            await interaction.followup.send(
                f"set feedback channel to {channel.mention}"
            )
            return

        if channel is None:
            db.update_one(
                {"_id": interaction.guild.id}, {"$set": {"feedback_channel": None}}
            )
            await interaction.followup.send("set feedback channel to None")
            return
        db.update_one(
            {"_id": interaction.guild.id}, {"$set": {"feedback_channel": channel.id}}
        )

        await interaction.followup.send(embed=discord.Embed(title="Feedback channel set ✨", description="You can now use the /feedback command", color=discord.Color.green() ), ephemeral=True)

    @feedback_channel.error
    async def feedback_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(title="Missing permissions", description="You need to be an administrator to use this command", color=discord.Color.red() ), ephemeral=True)
            return


async def setup(bot):
    await bot.add_cog(AnonymousSuggestion(bot))
    print("Loaded Anonymous Suggestion Cog")
