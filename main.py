import logging
from dotenv import load_dotenv
import os
from discord import Intents
from discord.ext import commands

logging.basicConfig(filemode="city-cs.log", level=logging.DEBUG, format="[%(asctime)s - %(levelname)s] %(message)s", datefmt="%d/%b/%Y %H:%M:%S")
logger = logging.getLogger("city-cs.main")
logger.setLevel(logging.INFO)

logger.info("Starting City CS Bot")

# Attempt to load a .env file, if none exists, use the default settings
try:
    load_dotenv()
except BaseException:
    logger.warning(".env file could not be loaded")

token = os.getenv("botToken")
prefix = os.getenv("botPrefix")

# Set startup cogs that will be loaded when the bot starts
startupCogs = ["reactionRoles"]

intents = Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
bot = commands.Bot(command_prefix=(prefix, prefix.lower()), intents=intents)
logger.info(f"Using bot prefix \"{prefix}\"")

# Attempt to load each cog
for cog in startupCogs:
    try:
        bot.load_extension(f"modules.{cog}")
        logger.info(f"{cog} loaded")
    except Exception as e:
        logger.error(f"Unable to load {cog}: {e}")

bot.run(token)