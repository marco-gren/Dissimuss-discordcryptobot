
import discord
from discord.ext import commands,tasks
import requests
import json
import random
from tinydb import TinyDB,Query
import asyncpraw
from decouple import config
my_secret = config("TOKEN")
#replace x with your account
reddit = asyncpraw.Reddit(
    client_id="x",
    client_secret="x",
    password="x",
    user_agent="x",
    username="x",
)

User = Query()    

bot = discord.Client()

bot = commands.Bot(command_prefix='!')

cryptoping =TinyDB("db.json")

    
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
@bot.command()
async def meme(ctx):
    subreddit = await reddit.subreddit("memes")

    all_subs =[]

    hot = subreddit.hot(limit = 50)
    async for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url= url)
    await ctx.send(embed = em ) 


@bot.command(help=""" Add cyrptocurrency to list """)
async def new(ctx,x):
        cryptoping.insert({'currency':f'{x}'})
        await ctx.channel.send("new currency added")  
@bot.command(help=""" Delete cryptocurrency from list """)    
async def delete(ctx,arg):
  cryptopingdelete(arg)
  await ctx.channel.send(f"{arg} got deleted")
    
@bot.command(help="""Show all coins on list """)
async def liste(ctx):
    print(cryptoping.all())
    liste = cryptoping.all()
    for currency in liste:
        name = currency["currency"]
        print(name)
        await ctx.channel.send(name)
@bot.command(
    help= """
    "!crypto wantedcurrency" replace wantedcurrency with a currency of choice. 😪 & 🚀 show the trend in last 24h . 
    Important: If the currency has a space in their name replace it with a -.
   

    
    """)
async def crypto(ctx,arg):
    outcome = cryptorequest(arg)
    outcomedolar = cryptorequestdolar(arg)
    print(outcome)
    print(arg)
    await ctx.channel.send(f"{outcome[1]}€{outcome[0]}")
    await ctx.channel.send(f"{outcomedolar[1]}${outcomedolar[0]}")
    
@bot.command(help="""Starts the currencyupdater. Every hour """)
async def go(ctx):
    cryptodingdong.start(ctx)
@bot.command(help="""Stops the currencyupdater""")
async def stop():
    cryptodingdong.stop()
@tasks.loop(seconds=3600)
async def cryptodingdong(ctx):
        liste = cryptoping.all()
        for currency in liste:
            name = currency["currency"]
            outcome = cryptorequest(name)
            outcomedolar = cryptorequestdolar(name)
            money = outcome[1]
            money2 = outcomedolar[1]
            await ctx.channel.send(f"{name}:\n{money} € and {money2} $")
                                

def cryptorequest(x):
    request = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price?ids={x}&vs_currencies=eur').text
    requesttrend = requests.get(
        f'https://api.coingecko.com/api/v3/coins/{x}/market_chart?vs_currency=eur&days=1&interval=daily').text
    requesttrend = json.loads(requesttrend)

    oldValue = requesttrend["prices"][0]
    oldValue2 = oldValue[1]

    newValue = requesttrend["prices"][1]
    newValue2 = newValue[1]

    requesttrend = float(newValue2) / (float(oldValue2) / 100) - 100
    
    request = json.loads(request)
    requestprice = (float(request[x]["eur"]))

    if requesttrend > 0:
        requestemote = (":rocket:")
    else:
        requestemote = (":sleepy:")
    return requestemote,requestprice

def cryptorequestdolar(x):
    request = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price?ids={x}&vs_currencies=usd').text
    requesttrend = requests.get(
        f'https://api.coingecko.com/api/v3/coins/{x}/market_chart?vs_currency=usd&days=1&interval=daily').text
    requesttrend = json.loads(requesttrend)

    oldValue = requesttrend["prices"][0]
    oldValue2 = oldValue[1]

    newValue = requesttrend["prices"][1]
    newValue2 = newValue[1]

    requesttrend = float(newValue2) / (float(oldValue2) / 100) - 100
    
    request = json.loads(request)
    requestprice = (float(request[x]["usd"]))

    if requesttrend > 0:
        requestemote = (":rocket:")
    else:
        requestemote = (":sleepy:")
    return requestemote,requestprice   
        


def cryptopingdelete(x):
    results = cryptoping.remove(User.currency == x )
    print(results)
    
               
bot.run(my_secret)

