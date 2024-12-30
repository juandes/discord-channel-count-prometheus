import argparse
import discord
from discord.ext import commands
from prometheus_client import start_http_server, Counter


parser = argparse.ArgumentParser()
parser.add_argument("--bot-token", required=True, help="Discord bot token.")
parser.add_argument("--channel-id", type=int, required=True,
                    help="ID of the channel to count messages in.")
parser.add_argument("--metrics-port", type=int, default=8000,
                    help="Port to expose Prometheus metrics (default: 8000).")
args = parser.parse_args()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_COUNT = Counter("discord_messages_total",
                        "Count of Discord messages")


@bot.event
async def on_message(message):
    if message.channel.id != args.channel_id:
        return

    MESSAGE_COUNT.inc()

    await bot.process_commands(message)

if __name__ == "__main__":
    # Start an HTTP server for Prometheus scraping
    start_http_server(args.metrics_port)
    bot.run(args.bot_token)
