import discord
import requests
from flask import Flask
from threading import Thread

DISCORD_TOKEN = 'MTM2OTU2MzEzMzQ3OTQ4OTUzNg.GAgGGo.p1_BhrkP7Dujo645CXWTf2CRsXmcOUbCBwezdQ'  # Regenerate and replace here
GOOGLE_CHAT_WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAQAf2rug9g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=9UOvqFjwDsRVFKx6EXOdr0TqxNJC7VY0HR_rkNOaJKw'  # Replace here
CHANNEL_ID = 1086109782206861403  # Your Discord channel ID

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Alive</h1><p>This bot is hosted. You can access it directly via the Replit link.</p>'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.id == client.user.id:
        return

    content = message.content.strip()
    if content:
        print(f'📩 Forwarding: {content}')
        response = send_to_google_chat(content)
        if response.status_code != 200:
            print(f'❌ Error: {response.status_code}')

def send_to_google_chat(message):
    payload = {"text": message}
    return requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload)

keep_alive()  # Start the Flask server
client.run(DISCORD_TOKEN)  # Run the Discord bot
