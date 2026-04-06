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
parser.add_argument("--state-file", default="counter.txt",
                    help="File to persist the message count across restarts (default: counter.txt).")
args = parser.parse_args()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_COUNT = Counter("discord_messages_total",
                        "Count of Discord messages")


def load_count():
    try:
        with open(args.state_file) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_count(value):
    with open(args.state_file, "w") as f:
        f.write(str(value))


@bot.event
async def on_ready():
    saved = load_count()
    if saved:
        MESSAGE_COUNT.inc(saved)


@bot.event
async def on_message(message):
    if message.channel.id != args.channel_id:
        return

    MESSAGE_COUNT.inc()
    save_count(int(MESSAGE_COUNT._value.get()))

    await bot.process_commands(message)

if __name__ == "__main__":
    # Start an HTTP server for Prometheus scraping
    start_http_server(args.metrics_port)
    bot.run(args.bot_token)
