import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Tus códigos de IA ya configurados
SIGHTENGINE_USER = '714986818'
SIGHTENGINE_SECRET = 'kn8GkwqmGrfWaYR9MRTCqDVKXKKtbP88'

async def evaluar_contenido(url_imagen):
    params = {
        'url': url_imagen,
        'models': 'nudity-2.0,gore,csam',
        'api_user': SIGHTENGINE_USER,
        'api_secret': SIGHTENGINE_SECRET
    }
    try:
        response = requests.get('https://sightengine.com', params=params)
        data = response.json()
        
        if data.get('status') == 'success':
            if data['nudity']['sexual_activity'] > 0.7 or data['nudity']['sexual_display'] > 0.7:
                return "Porno/Contenido Explícito"
            if data['gore']['prob'] > 0.6:
                return "Gore/Violencia Extrema"
            if data.get('csam', {}).get('prob', 0) > 0.5:
                return "Material Ilegal (CSAM)"
    except Exception as e:
        print(f"Error en IA: {e}")
    return None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        re
