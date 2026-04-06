FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

VOLUME /data

ENV BOT_TOKEN=""
ENV CHANNEL_ID=""
ENV METRICS_PORT="8000"
ENV STATE_FILE="/data/counter.txt"

CMD ["sh", "-c", "python main.py --bot-token \"$BOT_TOKEN\" --channel-id \"$CHANNEL_ID\" --metrics-port \"$METRICS_PORT\" --state-file \"$STATE_FILE\""]
