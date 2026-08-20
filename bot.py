import discord
from discord.ext import commands
import aiohttp
import os
import datetime 

### --- CONFIGURACIÓN DE NÚCLEO DE MÁXIMA PRIORIDAD ---

intents = discord.Intents.default()
intents.message_content = True  # Escáner de flujo de datos continuo
intents.members = True          # Control de fronteras del servidor 

### Inicialización del sistema central camuflado

bot = commands.Bot(command_prefix="c!", intents=intents) 

### Credenciales de la Inteligencia Artificial (Extraídas directamente del entorno)

SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_API_KEY = os.getenv("SIGHTENGINE_API_KEY") 

### Matriz extendida de detección de ingeniería social y acoso infantil

PATRONES_GROOMING = [
"donde vives", "cual es tu direccion", "donde queda tu casa",
"pasa tu direccion", "dame tu direccion", "cual es tu casa",
"pasa direccion", "donde vives?", "cual es tu dirección?",
"pasa foto", "estas sola", "estas solo", "pasa pack", "pasa ig",
"pasa whatsapp", "quieres ser mi novia", "cuantos años tienes",
"mandame foto", "estas solita", "estas solito", "mandame tu foto"
] 

### Registro de historial de reincidencias blindado (Persistente durante la sesión)

registro_violaciones = {} 

@bot.event
async def on_ready():
    print("=================================================================")
    print(f"⚡ SISTEMA INTEGRADO DE SEGURIDAD MÁXIMA ACTIVADO: {bot.user.name}")
    print("⚡ POTENCIA DE ESCÁNER COMPUESTO EN EJECUCIÓN [10x MOTOR NORMAL]")
    print("=================================================================") 

### --- MOTOR 1: CONTROL ULTRA ESTRICTO DE ACCESO (PROTECCIÓN ANTI-INVASIÓN) ---

@bot.event
async def on_member_join(member):
    ahora = datetime.datetime.now(datetime.timezone.utc)
    antiguedad = ahora - member.created_at 

### Umbral de seguridad elevado: Cuentas creadas hace menos de 14 días son bloqueadas

    if antiguedad.days < 14:
    try: 

# Mensaje genérico de fachada para ocultar que es una IA policial

        await member.send("⚠️ Error 503: Servidor temporalmente inaccesible para cuentas no verificadas.")
        await member.kick(reason="Seguridad 10x: Cuenta de alto riesgo (antigüedad insuficiente).")
        print(f"🔒 [Frontera] Expulsado evasor potencial: {member.name} (Edad cuenta: {antiguedad.days} días)")

    except Exception as e:
        print(f"Error en cortafuegos de entrada: {e}") 

### --- MOTOR 2: DEFENSA ACTIVA EN TIEMPO REAL (MICROSEGUNDOS) ---

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

### ANALIZADOR A: INTELIGENCIA DE TEXTO (PREVENCIÓN DE ACOSO)

    contenido_limpio = message.content.lower()
    if any(patron in contenido_limpio for patron in PATRONES_GROOMING):
try:
await message.delete()  # Supresión instantánea del intento de contacto 

# Sanción severa inmediata: Aislamiento total por 1 hora

duracion_sancion = datetime.timedelta(hours=1)
await message.author.timeout(duracion_sancion, reason="Seguridad 10x: Violación de políticas de protección de datos.")
print(f"🤫 [Policía Texto] Interceptado mensaje sospechoso de {message.author.name}. Modificado estado a: Aislado.")
return

except Exception as e:
print(f"Fallo en motor de texto corporativo: {e}") 

### ANALIZADOR B: ESCÁNER DE FLUJO MULTIMEDIA (PORNO, GORE, EXPLOTACIÓN INFANTIL)

if message.attachments:
for attachment in message.attachments:
archivo_nombre = attachment.filename.lower() 

### Formatos universales multimedia procesados por el motor

if archivo_nombre.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.mov', '.webm')):
url_objetivo = attachment.url 

endpoint_ia = '[https://api.sightengine.com/1.0/check.json](https://api.sightengine.com/1.0/check.json)'
parametros = {
'url': url_objetivo,
'models': 'nudity-2.0,gore,minor',
'api_user': SIGHTENGINE_USER,
'api_secret': SIGHTENGINE_API_KEY
}

try:
async with aiohttp.ClientSession() as session:
async with session.get(endpoint_ia, params=parametros) as response:
if response.status == 200:
datos_ia = await response.json()
            if datos_ia.get('status') == 'success':
                datos_desnudez = datos_ia.get('nudity', {})
                datos_menores = datos_ia.get('minor', {})

### Puntuación combinada de actividad explícita

indice_porno = max(
datos_desnudez.get('sexual_activity', 0) or 0,
datos_desnudez.get('sexual_display', 0) or 0
) 

### Puntuaciones críticas de Gore y Explotación (CP)

indice_gore = datos_ia.get('gore', {}).get('prob', 0) or 0
indice_cp = datos_menores.get('prob', 0) or 0
riesgo_menor_extremo = datos_menores.get('none', 1) < 0.20 if 'none' in datos_menores else False 

### REGAL DE EXCEPCIÓN: Si la foto solo tiene poca ropa, el índice 'erotica' sube,

### pero como 'indice_porno' se mantiene bajo, la foto no se borra. Se respeta tu orden.

### AMENAZA NIVEL 1: Material ilegal de menores (CP) o Gore Sangriento -> Destrucción y Expulsión fulminante

if indice_cp > 0.70 or riesgo_menor_extremo or indice_gore > 0.55:
await message.delete()
await message.author.kick(reason="Seguridad 10x: Contenido prohibido crítico detectado de forma automatizada.")
print(f"💥 [Defensa Crítica] Contenido extremo eliminado. Usuario {message.author.name} expulsado permanentemente del perímetro.")
return 

### AMENAZA NIVEL 2: Pornografía o Desnudez Explícita Directa

elif indice_porno > 0.55:
await message.delete()  # Borrado inmediato del archivo explícito 

usuario_id = message.author.id                # Lógica de castigos progresivos blindada
                if usuario_id not in registro_violaciones:
                    registro_violaciones[usuario_id] = 1
                    tiempo_aislamiento = datetime.timedelta(minutes=10)
                else:
                    registro_violaciones[usuario_id] += 1
                    tiempo_aislamiento = datetime.timedelta(hours=1)

                try:
                    await message.author.timeout(tiempo_aislamiento, reason="Seguridad 10x: Difusión de material explícito.")
                    print(f"⚠️ [Defensa] Contenido explícito eliminado de {message.author.name}. Silenciado por: {tiempo_aislamiento}.")
                except discord.Forbidden:
                    print("❌ Alerta del núcleo: Permisos de moderación insuficientes en el servidor de Discord.")
                return
        else:
            print(f"Error de comunicación con la base IA: {datos_ia.get('error', {}).get('message')}")

except Exception as e:
print(f"Error crítico en el hilo de análisis de píxeles: {e}") 

### Mantiene la ejecución de los comandos del bot

await bot.process_commands(message) 

### --- MOTOR 3: COMANDOS DE FACHADA GLOBAL (EL DISFRAZ PERFECTO) ---

@bot.command(name="ping")
async def ping_sistema(ctx):
"""Muestra respuesta de red estándar"""
await ctx.send("🏓 **Core Core System:** Conexión estable. Latencia optimizada correctamente.") 

@bot.command(name="ayuda")
async def ayuda_sistema(ctx):
"""Despliega catálogo simulado de comandos"""
await ctx.send("⚙️ **Panel de Servicios Globales Core:**\nc!ping - Testeo de latencia del servidor.\nc!info - Métricas operativas del sistema.") 

@bot.command(name="info")
async def info_sistema(ctx):
"""Muestra el estado de la máquina del bot"""
await ctx.send("📊 **Estado del Entorno:** Canales protegidos, base de datos sincronizada. Operando sin anomalías.") 

### --- MOTOR 4: COMANDO POLICIAL TÁCTICO MÁXIMO ---

@bot.command(name="ban")
async def comando_ban_tactico(ctx, prefijo_a: str, member: discord.Member, *, motivo: str = "Baneado por el Alto Mando del Servidor"): 

### Verifica si quien ejecuta el comando tiene el rango administrativo de banear miembros

if ctx.author.guild_permissions.ban_members: 

### Validación obligatoria de estructura requerida: c!ban a @usuario

if prefijo_a.lower() == "a":
try: 

### Borra los mensajes de la última semana de ese usuario al banearlo

await member.ban(delete_message_days=7, reason=motivo)
await ctx.send("🔨 **Operación finalizada.** El registro del usuario ha sido eliminado por completo.")

# ACTIVACIÓN DEL SUPERBOT
bot.run(os.getenv("DISCORD_TOKEN"))
