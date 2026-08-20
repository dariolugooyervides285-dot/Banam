import discord
from discord.ext import commands
import aiohttp
import os
import datetime 

### Configuración de los intents obligatorios de Discord

intents = discord.Intents.default()
intents.message_content = True  # Permite leer el contenido, imágenes y videos del chat
intents.members = True          # Permite verificar a los miembros cuando se unen 

bot = commands.Bot(command_prefix="b!", intents=intents) 

### Lee las llaves secretas desde el panel de entorno de Render

SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_API_KEY = os.getenv("SIGHTENGINE_API_KEY")
TU_DISCORD_ID = int(os.getenv("MI_DISCORD_ID", "0"))  # Guarda tu ID de Discord en Render como MI_DISCORD_ID 

### Lista de palabras sospechosas que activarán el mute y reenvío privado

PALABRAS_SOSPECHOSAS = [
"donde vives", "cual es tu direccion", "donde queda tu casa",
"pasa tu direccion", "dame tu direccion", "cual es tu casa",
"pasa direccion", "donde vives?", "cual es tu dirección?"
] 

### Diccionario interno temporal para registrar las advertencias de los usuarios

### Nota: Si el bot se reinicia en Render, este contador vuelve a cero.

advertencias_usuarios = {} 

@bot.event
async def on_ready():
print(f"✅ Banam en línea y protegiendo el servidor como {bot.user}") 

### 1. INVESTIGACIÓN DE CUENTA AL UNIRSE

@bot.event
async def on_member_join(member):
ahora = datetime.datetime.now(datetime.timezone.utc)
antiguedad = ahora - member.created_at 

### Si la cuenta tiene menos de 14 días de haber sido creada, se expulsa por seguridad

if antiguedad.days < 14:
try:
await member.send("❌ Fuiste expulsado del servidor. Tu cuenta es demasiado reciente para verificar tu mayoría de edad.")
await member.kick(reason="Cuenta sospechosa / Posible menor de edad.")
print(f"👢 Cuenta sospechosa expulsada: {member.name}")
except Exception as e:
print(f"No se pudo expulsar al usuario al entrar: {e}") 

### 2. MODERACIÓN EN MILISEGUNDOS

@bot.event
async def on_message(message):
if message.author == bot.user:
return 

### A) DETECCIÓN DE PALABRAS SOSPECHOSAS (DIRECCIÓN DE CASA)

contenido_minusculas = message.content.lower()
if any(palabra in contenido_minusculas for palabra in PALABRAS_SOSPECHOSAS):
try:
await message.delete()
tiempo_mute = datetime.timedelta(hours=1)
await message.author.timeout(tiempo_mute, reason="Preguntar información personal / Dirección")
await message.channel.send(f"🤫 {message.author.mention} ha sido silenciado por 1 hora por solicitar o compartir información personal sospechosa.") 

if TU_DISCORD_ID != 0:
    dueno = await bot.fetch_user(TU_DISCORD_ID)
    await dueno.send(f"🚨 **Alerta de Banam:** El usuario **{message.author}** escribió un mensaje sospechoso en {message.channel.mention}:\n> {message.content}")
return

except Exception as e:
print(f"Error al procesar filtro de texto/mute: {e}")

### B) MODERACIÓN DE ARCHIVOS MULTIMEDIA (FOTOS, GIFS Y VIDEOS)

if message.attachments:
for attachment in message.attachments:
nombre_archivo = attachment.filename.lower()
if nombre_archivo.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.mov', '.webm')):
url_multimedia = attachment.url 

    api_url = 'https://api.sightengine.com/1.0/check.json'
    params = {
        'url': url_multimedia,
        'models': 'nudity-2.0,gore,minor',
        'api_user': SIGHTENGINE_USER,
        'api_secret': SIGHTENGINE_API_KEY
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('status') == 'success':
                        nudity_data = data.get('nudity', {})
                        minor_data = data.get('minor', {})

### 1. Monitoreo estricto de desnudez explícita total (Pechos, genitales, sexo)

desnudez_exagerada = max(
nudity_data.get('sexual_activity', 0) or 0,
nudity_data.get('sexual_display', 0) or 0
) 

### 2. Monitoreo de "poca ropa" (Trajes de baño, lencería, erótico, torso desnudo)

### Esto NO lo borramos, se queda guardado abajo con un umbral alto

poca_ropa = nudity_data.get('erotica', 0) or 0 

gore_score = data.get('gore', {}).get('prob', 0) or 0
cp_score = minor_data.get('prob', 0) or 0
es_unsafe_minor = minor_data.get('none', 1) < 0.20 if 'none' in minor_data else False 

### EVALUACIÓN DE REGLAS:

### Si es material de menores (CP) o Gore Extremo -> Expulsión inmediata directa

if cp_score > 0.70 or es_unsafe_minor or gore_score > 0.60:
await message.delete()
await message.author.kick(reason="Material extremo prohibido (Gore/Menores) detectado por IA.")
await message.channel.send(f"💥 **Banam IA:** El mensaje de {message.author.name} fue eliminado y el usuario fue expulsado por subir contenido extremadamente prohibido.")
return 

### Si es desnudez explícita total (Exageradamente poca ropa / partes íntimas visibles)

elif desnudez_exagerada > 0.60:
await message.delete()  # Borra la foto explícita al instante 

user_id = message.author.id
### Registrar o aumentar las faltas del usuario

if user_id not in advertencias_usuarios:
advertencias_usuarios[user_id] = 1
tiempo_castigo = datetime.timedelta(minutes=10)
msg_advertencia = f"⚠️ {message.author.mention}, **Banam IA** eliminó tu imagen por contener desnudez explícita. Has sido silenciado por **10 minutos** como advertencia."
else:
advertencias_usuarios[user_id] += 1
tiempo_castigo = datetime.timedelta(hours=1)
msg_advertencia = f"🚨 {message.author.mention}, reincidiste en subir contenido explícito. **Banam IA** te ha silenciado por **1 hora**." 

try:
await message.author.timeout(tiempo_castigo, reason="Subir contenido explícito / Desnudez")
await message.channel.send(msg_advertencia)
except discord.Forbidden:
print("❌ Error: El bot no tiene permisos de 'Moderar Miembros' para aplicar el timeout.")
return 

### NOTA DE LOGS: Si la foto solo tiene poca ropa (bikini/sensual), los scores de 'erotica' suben

                        # pero 'desnudez_exagerada' se mantiene bajo, por lo que el código no entra a ningún 'if' y la foto SE QUEDA en el chat perfectamente.
                        
                    else:
                        print(f"❌ Error en la API: {data.get('error', {}).get('message')}")
    except Exception as e:
        print(f"Error crítico en el análisis multimedia de la IA: {e}")

await bot.process_commands(message) 

### 3. COMANDO DE BANEO MANUAL ("b!ban a @usuario")

@bot.command(name="ban")
async def manual_ban(ctx, prefijo_a: str, member: discord.Member, *, razon: str = "Baneado por decisión administrativa"):
if ctx.author.guild_permissions.ban_members:
if prefijo_a.lower() == "a":
try:
await member.ban(reason=razon)
await ctx.send(f"🔨 El usuario **{member.name}** ha sido baneado permanentemente del servidor por la orden de {ctx.author.mention}.")
except Exception as e:
await ctx.send(f"❌ No pude banear al usuario. Verifica la jerarquía de roles.")
else:
await ctx.send("💡 Modo de uso correcto: b!ban a @nombre_de_usuario")
else:
await ctx.send("❌ No tienes permisos para usar este comando.")
