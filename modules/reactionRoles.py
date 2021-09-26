import logging
logger = logging.getLogger("city-cs.reactionRoles")
import discord
from discord import reaction
from discord.ext import commands
try:
    import ujson as json
except ModuleNotFoundError:
    import json
logger.info("Starting reactionRoles")

with open("data/roles.json") as file:
    reactionRoleData = json.load(file)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info(f"Reaction Roles initialised, using {self.bot=}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        logger.debug(f"Reaction added: {payload=}")
        if payload.member is not None:
            for message_id in reactionRoleData:
                if int(message_id) == payload.message_id:
                    message = payload.message_id
                    break
            logger.debug(f"Message found! {message=}")
            for reactionData in reactionRoleData[str(message)]:
                logger.debug(reactionData['reaction'] + "\uFE0F\N{combining enclosing keycap}")
                if reactionData['reaction'] + "\uFE0F\N{combining enclosing keycap}" == payload.emoji.name:
                    logger.info(f"Adding role {int(reactionData['role'])} from {payload.member}")
                    await payload.member.add_roles(payload.member.guild.get_role(int(reactionData['role'])))
                    await payload.member.send("Your roles have been updated per your options")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        logger.debug(f"Reaction removed: {payload=}")
        if payload.user_id is not None:
            for message_id in reactionRoleData:
                if int(message_id) == payload.message_id:
                    message = payload.message_id
                    break
            logger.debug(f"Message found! {message=}")
            for reactionData in reactionRoleData[str(message)]:
                logger.debug(reactionData['reaction'] + "\uFE0F\N{combining enclosing keycap}")
                if reactionData['reaction'] + "\uFE0F\N{combining enclosing keycap}" == payload.emoji.name:
                    logger.info(f"Removing role {int(reactionData['role'])} from {payload.user_id}")
                    payload.member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                    await payload.member.remove_roles(payload.member.guild.get_role(int(reactionData['role'])))
                    await payload.member.send("Your roles have been updated per your options")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))