from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
import os
import discord
from riotwatcher._apis.league_of_legends.urls import SummonerApiUrls

load_dotenv()

watcher = LolWatcher(os.getenv('API_KEY'))
client = discord.Client()

region = 'na1'

def get_summoner_rank_info(name):
    try:
        summoner = watcher.summoner.by_name(region,name)
    except ApiError:
        return "No summoner found"

    ranked_stats = watcher.league.by_summoner(region,summoner['id'])

    dict_num = 0 if ranked_stats[0].get('queueType') == 'RANKED_SOLO_5x5' else 1

    summ_name = ranked_stats[dict_num].get('summonerName')
    rank_tier = ranked_stats[dict_num].get('tier').title()
    rank_division = ranked_stats[dict_num].get('rank')
    lp = ranked_stats[dict_num].get('leaguePoints')
    wins = ranked_stats[dict_num].get('wins')
    losses = ranked_stats[dict_num].get('losses')

    return {'summonerName': summ_name, 'tier':rank_tier, 'division':rank_division, 'lp':lp, 'wins':wins, 'losses':losses }

def get_summoner_rank(name):
    # try:
    #     summoner = watcher.summoner.by_name(region,name)
    # except ApiError:
    #     return "No summoner found"

    # ranked_stats = watcher.league.by_summoner(region,summoner['id'])

    # solo_tiers = ['MASTER', 'GRANDMASTER', 'CHALLENGER']

    # dict_num = 0 if ranked_stats[0].get('queueType') == 'RANKED_SOLO_5x5' else 1

    # summ_name = ranked_stats[dict_num].get('summonerName')
    # rank = ranked_stats[dict_num].get('tier').title() +  ' ' + ranked_stats[dict_num].get('rank')
    # lp = ranked_stats[dict_num].get('leaguePoints')
    # wins = ranked_stats[dict_num].get('wins')
    # losses = ranked_stats[dict_num].get('losses')
    summoner = get_summoner_rank_info(name)

    stats_string = """{name}\nRank: {rank} {lp} LP\nW: {wins} L: {losses}
    """
    return stats_string.format(name=summoner.summ_name, rank=summoner.rank, lp=summoner.lp, wins=summoner.wins, losses=summoner.losses)

def get_difference_in_ranks(name1, name2):
    summoner1 = get_summoner_rank_info(name1)
    summoner2 = get_summoner_rank_info(name2)

    ranks_dict = {'Iron' : 1, 'Bronze' : 2, 'Silver' : 3, 'Gold' : 4, 'Platinum' : 5, 'Diamond' : 6
    , 'Master' : 7, 'Grandmaster' : 7, 'Challenger' : 7}
    divisions_dict = {'I' : 1, 'II' : 2, 'III' : 3, 'IV' : 4}

    message_string = ""

    summ1_name = summoner1.get('summonerName')
    summ1_lp = summoner1.get('lp')
    summ1_tier = ranks_dict.get(summoner1.get('tier'))
    summ1_div = divisions_dict.get(summoner1.get('division'))

    summ2_name = summoner2.get('summonerName')
    summ2_lp = summoner2.get('lp')
    summ2_tier = ranks_dict.get(summoner2.get('tier'))
    summ2_div = divisions_dict.get(summoner2.get('division'))

    if summ1_tier == summ2_tier and summ1_div == summ2_div:
        message_string = "{summonerName1} is {difference} LP higher than {summonerName2}, {summonerName2} kinda sucks"
        if summ1_lp > summ2_lp:
            return message_string.format(summonerName1 = summ1_name, summonerName2 = summ2_name,
            difference = summ1_lp - summ2_lp)
        elif summ1_lp < summ2_lp:
            return message_string.format(summonerName1 = summ2_name, summonerName2 = summ1_name,
            difference = abs(summ2_lp - summ1_lp))
        else:
            return "You're both as good (or as bad) as each other"

    elif summ1_tier == summ2_tier:
        message_string = "{summonerName1} is {difference} division(s) higher than {summonerName2}, {summonerName2} needs to climb"
        if summ1_div < summ2_div:
            return message_string.format(summonerName1 = summ1_name, summonerName2 = summ2_name, difference = summ1_div - summ2_div)
        else:
            return message_string.format(summonerName1 = summ2_name, summonerName2 = summ1_name, difference = abs(summ2_div - summ1_div))
    
    else:
        message_string = "{summonerName1} is {difference} tier(s) higher than {summonerName2}, {summonerName2} needs to climb"
        if summ1_tier > summ2_tier:
            return message_string.format(summonerName1 = summ1_name, summonerName2 = summ2_name, difference = summ1_tier - summ2_tier)
        else:
            return message_string.format(summonerName1 = summ2_name, summonerName2 = summ1_name, difference = abs(summ2_tier - summ1_tier))



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('!rank'):
        msg_words = msg.split()
        rank = get_summoner_rank(msg_words[1])
        await message.channel.send(rank)
    elif msg.startswith('!diff'):
        msg_words = msg.split()
        difference = get_difference_in_ranks(msg_words[1],msg_words[2])
        await message.channel.send(difference)


client.run(os.getenv('DISCORD_TOKEN'))





