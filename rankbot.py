from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
import os
import discord

load_dotenv()

watcher = LolWatcher(os.getenv('API_KEY'))
client = discord.Client()

region = 'na1'

def get_summoner_rank(name):
    try:
        summoner = watcher.summoner.by_name(region,name)
    except ApiError:
        return "No summoner found"

    ranked_stats = watcher.league.by_summoner(region,summoner['id'])

    solo_tiers = ['MASTER', 'GRANDMASTER', 'CHALLENGER']

    dict_num = 0 if ranked_stats[0].get('queueType') == 'RANKED_SOLO_5x5' else 1

    summ_name = ranked_stats[dict_num].get('summonerName')
    rank = ranked_stats[dict_num].get('tier').title() +  ' ' + ranked_stats[dict_num].get('rank')
    lp = ranked_stats[dict_num].get('leaguePoints')
    wins = ranked_stats[dict_num].get('wins')
    losses = ranked_stats[dict_num].get('losses')

    stats_string = """{name}\nRank: {rank} {lp} LP\nW: {wins} L: {losses}
    """
    return stats_string.format(name=summ_name, rank=rank, lp=lp, wins=wins, losses=losses)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('!rank'):
        msg_words = msg.split()
        rank = get_summoner_rank(msg_words[1])
        await message.channel.send(rank)

client.run(os.getenv('DISCORD_TOKEN'))





