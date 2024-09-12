import discord, boto3
from datetime import datetime
from discord.ext import tasks
from rss_parser import RSSParser
from requests import get

#Configure RSS parser & fetch the feed
rss_url = "https://feeds.feedburner.com/TheHackersNews"
response = get(rss_url)
rss = RSSParser.parse(response.text)

#Store existing news into a list
rss_articles = []

def load_current_news():
    global rss_articles
    print(f"[*] Loading existing news at {datetime.now()}")
    for item in rss.channel.items:
        title = item.title
        title = title.replace("content=", "")
        rss_articles.append(title)

#Configure Discordpy
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#Main loop to fetch the news & post it to a channel if new
@tasks.loop(seconds=5400)
async def refresh_news():
    global rss_articles
    
    #Check to see if there are over 100 articles in our rss_articles list and clean it up a bit if true
    if len(rss_articles) > 100:
         del rss_articles[:30]
         print(f"[*] Deleting some old entries from the RSS topic list")
    else:
         pass
    
    print(f"[*] Refreshing the RSS feed at {datetime.now()}")
    response = get(rss_url)
    rss = RSSParser.parse(response.text)
    channel = client.get_channel(1218111916191518740)
    for item in rss.channel.items:
        title = item.title
        title = title.replace("content=", "")
        link = item.link
        link = link.replace("content=", "")

        if title in rss_articles:
            pass

        else:
            print(f"[*] Posting news @ {datetime.now()} -> {link}")
            rss_articles.append(title)
            await channel.send(f"{title}\n{link}")

#On ready state start the loop
@client.event
async def on_ready():
	print(f"[*] Logged in as {client.user} at {datetime.now()}")
	print(f"[*] Starting the loop at {datetime.now()}")
	refresh_news.start()

#Fetch Discord token from AWS SSM Parameter Store
ssm_client = boto3.client('ssm', region_name='eu-north-1')
bot_token = ssm_client.get_parameter(Name="discordtoken")
bot_token = bot_token['Parameter']['Value']

#Load current news & run the bot
load_current_news()
client.run(bot_token)
