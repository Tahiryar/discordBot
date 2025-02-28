import discord
import openai
import os
from dotenv import load_dotenv  # Load dotenv module

# Load environment variables
load_dotenv()

# Get API keys securely
openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Bot logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f"Message from {message.author}: {message.content}")

        if message.content.lower().startswith('chatgpt'):
            user_message = message.content[len('chatgpt '):]  # Extract message after "chatgpt"
            response = await self.get_chatgpt_response(user_message)
            await message.channel.send(response)

    async def get_chatgpt_response(self, user_message):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_message,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Run the bot
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)  # Use token from .env file
