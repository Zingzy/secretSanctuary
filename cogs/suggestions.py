import discord
from discord import ui, app_commands
from discord.ext import commands
from utils import mongo


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
        embed.set_author(name="Anonymous User")
        embed.set_footer(text="Anonymous Suggestion")
        await channel.send(embed=embed)
        await interaction.response.send_message("sent suggestion", ephemeral=True)


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
        embed.set_author(name="Anonymous User")
        embed.set_footer(text="Anonymous Feedback")
        await channel.send(embed=embed)
        await interaction.response.send_message("sent feedback", ephemeral=True)


class AnonymousSuggestion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="suggest",
        description="Suggest anything you want",
    )
    async def suggest(self, interaction: discord.Interaction):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        if not server:
            await interaction.response.send_message("no suggestion channel set")
            return
        if server["suggestion_channel"] is None:
            await interaction.response.send_message("no suggestion channel set")
            return
        await interaction.response.send_modal(SuggestionModal())

    @app_commands.command(
        name="feedback",
        description="Suggest anything you want",
    )
    async def feedback(self, interaction: discord.Interaction):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        if not server:
            await interaction.response.send_message("no feedback channel set")
            return
        if server["feedback_channel"] is None:
            await interaction.response.send_message("no feedback channel set")
            return
        await interaction.response.send_modal(FeedbackModal())

    @app_commands.command()
    @app_commands.default_permissions(administrator=True)
    async def suggestion_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel_id = None
        if channel is not None:
            channel_id = channel.id
        schema = {
            "_id": interaction.guild.id,
            "suggestion_channel": channel_id,
            "feedback_channel": None
        }

        if not server:
            db.insert_one(schema)
            if channel is None:
                await interaction.response.send_message("set suggestion channel to None")
                return
            await interaction.response.send_message(f"set suggestion channel to {channel.mention}")
            return

        if channel is None:
            db.update_one({"_id": interaction.guild.id}, {"$set": {"suggestion_channel": None}})
            await interaction.response.send_message("set suggestion channel to None")
            return
        db.update_one({"_id": interaction.guild.id}, {"$set": {"suggestion_channel": channel.id}})
        await interaction.response.send_message(f"set suggestion channel to {channel.mention}")

    @suggestion_channel.error
    async def suggestion_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("you don't have permission to do that")
            return

    @app_commands.command()
    @app_commands.default_permissions(administrator=True)
    async def feedback_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        db = mongo("servers")
        server = db.find_one({"_id": interaction.guild.id})
        channel_id = None
        if channel is not None:
            channel_id = channel.id
        schema = {
            "_id": interaction.guild.id,
            "suggestion_channel": None,
            "feedback_channel": channel_id
        }

        if not server:
            db.insert_one(schema)
            if channel is None:
                await interaction.response.send_message("set feedback channel to None")
                return
            await interaction.response.send_message(f"set feedback channel to {channel.mention}")
            return

        if channel is None:
            db.update_one({"_id": interaction.guild.id}, {"$set": {"feedback_channel": None}})
            await interaction.response.send_message("set feedback channel to None")
            return
        db.update_one({"_id": interaction.guild.id}, {"$set": {"feedback_channel": channel.id}})
        await interaction.response.send_message(f"set feedback channel to {channel.mention}")

    @feedback_channel.error
    async def feedback_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("you don't have permission to do that")
            return


async def setup(bot):
    await bot.add_cog(AnonymousSuggestion(bot))
    print("Loaded Anonymous Suggestion Cog")
