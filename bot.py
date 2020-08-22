import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import os

bot = commands.Bot(command_prefix=">", description="Este bot tiene como objetivo realizar algunas funcionalidades utiles para que juguemos de una forma mas comoda!!! envia el comando -help para ver los comandos", help_command=None)

searchResults=[]
TOKEN= os.getenv("TOKEN")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description="Amantes de los videojuegos, las polas, la Mary Jane, la comida y todo lo que maree.", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
    embed.add_field(name="Fecha de creación del server", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Dueño del server", value=f"{ctx.guild.owner}")
    embed.add_field(name="Region del server", value=f"{ctx.guild.region}")
    embed.add_field(name="ID del servidor", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"https://i.pinimg.com/564x/fb/da/0f/fbda0f3ab85bf7cd8cf66b0807be2e8e.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Lista de comandos:", color=discord.Color.dark_red())
    embed.add_field(name="Ver información del server:", value="-info")
    embed.add_field(name="Buscar videos en yt:", value="-yt como pasar x mazmorra")
    embed.add_field(name="Obtener videos de la busqueda anterior:", value="-nextyt 1 (puedes poner desde 1 hasta 30 aprox)")
    embed.set_thumbnail(url="https://i.pinimg.com/564x/30/7d/e0/307de0cea329e28896cce0294253eca2.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def yt(ctx, *, search): #get args and search videos on youtube
    global searchResults
    queryString= parse.urlencode({'search_query': search}) #take the args from the user and parse that to a url
    htmlContent= request.urlopen('http://www.youtube.com/results?'+ queryString)
    searchResults=re.findall( r"watch\?v=(\S{11})", htmlContent.read().decode())#get videos id
    
    await ctx.send(f"Se han encontrado {len(searchResults)} resultados.\n\nPrimer Resultado:\nhttp://www.youtube.com/watch?v={searchResults[0]}") #get and send the first video

@bot.command()
async def nextyt(ctx, option:int):
    leng = len(searchResults)
    if leng != 0:
        await ctx.send(f"http://www.youtube.com/watch?v={searchResults[option]}")
    else:
        await ctx.send("No has buscado videos!! para ver los comandos utiliza: -help")

@bot.event 
async def on_ready():
    print("Bot is Online")

# @bot.event
# async def on_member_join(ctx, member):
#     channel = bot.get_channel("745007812957962283")
#     await ctx.send(f"Bienvenido {member} usa el comando -info")

bot.run(TOKEN)