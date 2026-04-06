# Discord Prometheus Notifications

A Python script that counts Discord messages in a specified channel and exposes the count as a Prometheus metric (`discord_messages_total`).

## Prerequisites
- Discord Application & Bot Token
  - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
  - Create or select an existing application, then add a bot.
  - Copy the Bot Token (keep it secret!).

## Dependencies

```
discord.py>=2.4.0
prometheus_client>=0.21.1
``` 

## Installation

1. Clone this repo
```
git clone https://github.com/juandes/discord-channel-count-prometheus.git
cd discord-channel-count-prometheus
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Configure the bot
   1. Invite your bot to your server and turn on the "Message Content Intent" in the bot settings.

## Usage
```
python main.py \
    --bot-token "YOUR_DISCORD_BOT_TOKEN" \
    --channel-id 12345 \
    --metrics-port 8001
```

This starts a local HTTP server serving metrics at http://localhost:8001/metrics.

### Command Line Arguments
- --bot-token (required)
  - Your Discord bot token.
- --channel-id (required)
  - The ID of the Discord channel to monitor.
- --metrics-port (optional)
  - Port on which to expose Prometheus metrics. Defaults to 8000 if not specified.


## Prometheus Configuration
To scrape the bot’s metrics, add a new `scrape_configs` entry to your Prometheus configuration (`prometheus.yml`). For example, if you’re running the bot on your local machine at port 8001:

```yaml
scrape_configs:
  - job_name: 'discord_bot'
    static_configs:
      - targets: ['192.168.1.XX:8001']
```

## Accessing the Metrics
1. Check Metrics in Browser
Visit http://localhost:8001/metrics (or whichever port you chose). You should see plain text output like:
```
discord_messages_total 5
```
2. Prometheus Query
In Prometheus, go to the Graph tab and enter:
```
discord_messages_total
```
to see the counter's current value.