import discord
import requests
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD")  # Regenerate and replace here
GOOGLE_CHAT_WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAQAf2rug9g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=9UOvqFjwDsRVFKx6EXOdr0TqxNJC7VY0HR_rkNOaJKw'  # Replace here
CHANNEL_ID = 1086109782206861403  # Your Discord channel ID

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True  # Needed to resolve mentions like <@&role>

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.id == client.user.id:
        return

    # Extract message content
    content = message.content.strip()

    # Resolve mentions
    content = await resolve_mentions(message, content)

    # Extract embed content if normal content is empty
    if not content and message.embeds:
        embed_texts = []
        for embed in message.embeds:
            if embed.title:
                embed_texts.append(f"**{embed.title}**")
            if embed.description:
                embed_texts.append(embed.description)
            for field in embed.fields:
                embed_texts.append(f"**{field.name}**\n{field.value}")
        content = "\n".join(embed_texts).strip()

    if content:
        print(f'📩 Forwarding: {content}')
        response = send_to_google_chat(content)
        if response.status_code != 200:
            print(f'❌ Error sending to Google Chat: {response.status_code}, {response.text}')
    else:
        print('⚠️ Message had no content or embed text, not forwarded.')

async def resolve_mentions(message, content):
    # Replace @everyone and @here
    content = content.replace("@everyone", "**@everyone**")
    content = content.replace("@here", "**@here**")

    # Replace role mentions
    for role in message.role_mentions:
        content = content.replace(f"<@&{role.id}>", f"**@{role.name}**")

    # Replace user mentions
    for user in message.mentions:
        content = content.replace(f"<@{user.id}>", f"**@{user.display_name}**")

    return content

def send_to_google_chat(message):
    payload = {"text": message}
    return requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload)

client.run(DISCORD_TOKEN)


import discord

DISCORD_TOKEN = 'MTM2OTU2MzEzMzQ3OTQ4OTUzNg.GAgGGo.p1_BhrkP7Dujo645CXWTf2CRsXmcOUbCBwezdQ'  # Regenerate and replace here
GOOGLE_CHAT_WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAQAf2rug9g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=9UOvqFjwDsRVFKx6EXOdr0TqxNJC7VY0HR_rkNOaJKw'  # Replace here
CHANNEL_ID = 1086109782206861403  # Your Discord channel ID

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.id == client.user.id:
        return

    # Try getting normal message content first
    content = message.content.strip()

    # If content is empty, try extracting from embeds
    if not content and message.embeds:
        embed_texts = []
        for embed in message.embeds:
            if embed.title:
                embed_texts.append(f"**{embed.title}**")
            if embed.description:
                embed_texts.append(embed.description)
            for field in embed.fields:
                embed_texts.append(f"**{field.name}**\n{field.value}")
        content = "\n".join(embed_texts).strip()

    if content:
        print(f'📩 Forwarding: {content}')
        response = send_to_google_chat(content)
        if response.status_code != 200:
            print(f'❌ Error sending to Google Chat: {response.status_code}, {response.text}')
    else:
        print('⚠️ Message had no content or embed text, not forwarded.')

def send_to_google_chat(message):
    payload = {"text": message}
    return requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload)

client.run(DISCORD_TOKEN)

