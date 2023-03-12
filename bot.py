import discord
import sys
import json
import main
import Logger_custom

client = discord.Client()
# default value
game_mode = 'Pathfinder_simplified'
# init flag
ready = 0


@client.event
async def on_ready():
    print("Table reader bot is ready")


@client.event
async def on_message(message):
    global game_mode
    if message.author == client.user:
        return
    # --------------------------------------
    # test command
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    # --------------------------------------
    # command to add player to list of players
    if message.content.startswith('$Add new player:'):
        Str = message.content.replace('$Add new player:', '')
        Str = Str.replace('$Add new player:', '')
        Data = Str.split(",")
        Data[0] = Data[0].replace(' ', '')
        Data[1] = Data[1].replace(' ', '')
        d = json.load(open("Players.json"))
        if Data[0] in d.keys():
            message.channel.send('Name taken')
        else:
            d[Data[0]] = Data[1]
            with open('Players.json', 'w') as f:
                json.dump(d, f, indent=2)
                # print(Data)
                Logger_custom.AppendLog("Player added " + Data[0])
            await message.channel.send('Player added,' + ' player name:' + Data[0])
    # --------------------------------------
    # command to stop bot
    if message.content.startswith('$EXIT123a098'):
        await message.channel.send('Exit done')
        Logger_custom.AppendLog("Exit call")
        sys.exit()
    # --------------------------------------
    # different version of table.
    if message.content.startswith('$Pathfinder_old'):
        game_mode = 'Pathfinder_old'
        await message.channel.send('game mode set to "Pathfinder_old"')
    # --------------------------------------
    # different version of table. Only simplified is in use now    
    if message.content.startswith('$Pathfinder_simplified'):
        game_mode = '$Pathfinder_simplified'
        await message.channel.send('game mode set to "$Pathfinder_simplified"')
    # --------------------------------------
    # roll dice 10 times 
    if message.content.startswith('$CUBE_TEST'):
        i = 0
        while i < 10:
            await message.channel.send("iteration" + " " + str(i) + " " + ":")
            await message.channel.send(main.CubeSim(1, 20, 0, "-"))
            i = i + 1
    # ---------------------------------------------
    # different types of character-related commands
    # ---------------------------------------------    
    if message.content.startswith('$do'):
        message.content.replace('$do', '')
        Str = message.content
        Str = Str.replace('$do', '')
        Data = Str.split(",")
        d = json.load(open("Players.json"))
        Val = Data[0].replace(' ', '')
        # print(Val)
        if Val in d:
            await message.channel.send(main.What_Do(d[Val], Data[1], game_mode))
    # --------------------------------------
    if message.content.startswith('$weaponacc'):
        message.content.replace('$weaponacc', '')
        Str = message.content
        Str = Str.replace('$weaponacc', '')
        Data = Str.split(",")
        d = json.load(open("Players.json"))
        Val = Data[0].replace(' ', '')
        # print(Val)
        if Val in d:
            await message.channel.send(main.Find_Val(d[Val], Data[1], game_mode, "acc"))
    # --------------------------------------
    if message.content.startswith('$weapondmg'):
        message.content.replace('$weapondmg', '')
        Str = message.content
        Str = Str.replace('$weapondmg', '')
        Data = Str.split(",")
        d = json.load(open("Players.json"))
        Val = Data[0].replace(' ', '')
        # print(Val)
        if Val in d:
            await message.channel.send(main.Find_Val(d[Val], Data[1], game_mode, "dmg"))
    # --------------------------------------
    if message.content.startswith('$skill'):
        message.content.replace('$skill', '')
        Str = message.content
        Str = Str.replace('$skill', '')
        Data = Str.split(",")
        d = json.load(open("Players.json"))
        Val = Data[0].replace(' ', '')
        # print(Val)
        if Val in d:
            Data[1] = Data[1].lower()
            if Data[1] == "инициатива" or Data[1] == "стойкость" or Data[1] == "реакция" or Data[1] == "воля":
                await message.channel.send(main.What_Do(d[Val], Data[1], game_mode))
            else:
                await message.channel.send(main.Find_Val(d[Val], Data[1], game_mode, "skill"))

if ready==0:
    client.run("TOKEN")
    ready = 1

