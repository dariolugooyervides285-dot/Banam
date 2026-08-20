import discord
from discord.ext import commands
import requests
import os

# Configuración de los intents obligatorios de Discord
intents = discord.Intents.default()
intents.message_content = True  # Permite leer las imágenes y textos del chat

bot = commands.Bot(command_prefix="b!", intents=intents)

# Lee las llaves secretas que guardaste en el panel de Render
SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_API_KEY = os.getenv("SIGHTENGINE_API_KEY")

@bot.event
async def on_ready():
    print(f"Banam activado y protegiendo el servidor.")

@bot.event
async def on_message(message):
    # Evita que el bot se analice a sí mismo
    if message.author == bot.user:
        return

    # Verificar si el mensaje tiene imágenes adjuntas
    if message.attachments:
        for attachment in message.attachments:
            # Validar formatos de imagen comunes
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                url_imagen = attachment.url
                
                # Conexión con la IA de moderación
                params = {
                    'url': url_imagen,
                    'models': 'nudity-2.0,gore',
                    'api_user': SIGHTENGINE_USER,
                    'api_secret': SIGHTENGINE_API_KEY
                }
                
                try:
                    response = requests.get('https://sightengine.com', params=params).json()
                    
                    # Extraer puntuaciones de la IA
                    porno_score = response.get('nudity', {}).get('sexual_activity', 0) or response.get('nudity', {}).get('sexual_display', 0)
                    gore_score = response.get('gore', {}).get('prob', 0)
                    
                    # Umbral equilibrado recomendado (0.35)
                    if porno_score > 0.35 or gore_score > 0.35:
                        await message.delete() # Borra la imagen prohibida inmediatamente
                        
                        # Mensaje de advertencia de Banam
                        await message.channel.send(f"⚠️ {message.author.mention}, el sistema de IA **Banam** eliminó tu mensaje por contener material no permitido (NSFW/Gore).")
                        return 
                        
                except Exception as e:
                    print(f"Error en la IA: {e}")

    await bot.process_commands(message)

# Token automático conectado a Render
bot.run(os.getenv("DISCORD_TOKEN"))
