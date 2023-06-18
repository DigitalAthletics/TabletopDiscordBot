from __future__ import print_function

import os.path
import random
import re
import Logger_custom

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def Read_Cell(spreadsheet_id, range_name):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    Logger_custom.AppendLog("token check (Read_Cell)")
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            Logger_custom.AppendLog("try refresh (Read_Cell)")

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            Logger_custom.AppendLog("try credentials (Read_Cell)")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            Logger_custom.AppendLog("try rewrite token 2 (Read_Cell)")
            token.write(creds.to_json())
    try:
        service = discovery.build('sheets', 'v4', credentials=creds)
        value = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        Cell_val = str(value.get('values'))
        return Cell_val[3:(len(Cell_val) - 3)]
    except HttpError as err:
        print(err)


# number of dices - dice size - bonus to roll - bonus sign
def CubeSim(num, val, bonus, sign):
    i = 1
    result = 0
    mod = 0

    bonus = abs(bonus)
    num = abs(num)
    val = abs(val)

    # result = int(bonus)
    if "-" in sign:
        # print("-")
        mod = -1 * bonus * num
    elif "+" in sign:
        # print("+")
        mod = bonus * num

    while i <= num:
        result += random.randint(1, val)
        i = i + 1

    end_val = result + mod

    msg = "Roll:" + str(end_val) + ", [" + str(result) + sign + str(bonus) + "]"  # ", [mod:" + sign + str(bonus) + " ," + "dices:" + str(num) + " ," + "dice size:" + str(val) + "]"
    return msg


def CubeSim_wrap(string):
    sign = " "
    if "-" in string:
        sign = "-"
    elif "+" in string:
        sign = "+"
    rx = re.compile(r'-?\d+(?:\.\d+)?')
    numbers = rx.findall(string)
    if len(numbers) == 3:
        return CubeSim(int(numbers[0]), int(numbers[1]), int(numbers[2]), sign)
    elif len(numbers) == 2:
        return CubeSim(int(numbers[0]), int(numbers[1]), 0, sign)


def Find_Val(player_name, weapon, game_mode, code):
    if player_name is not None:
        if game_mode is not None:
            creds = None
            Logger_custom.AppendLog("token check (Find_Val)")
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    Logger_custom.AppendLog("try refresh (Find_Val)")

                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
                else:
                    Logger_custom.AppendLog("try credentials (Find_Val)")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    Logger_custom.AppendLog("try rewrite token 2 (Find_Val)")
                    token.write(creds.to_json())
            try:
                service = discovery.build('sheets', 'v4', credentials=creds)
                if code == "skill":
                    request = service.spreadsheets().values().get(spreadsheetId=player_name, range="Навыки!A3:A40")
                else:
                    request = service.spreadsheets().values().get(spreadsheetId=player_name, range="Главная!B1:B40")
                response = request.execute()
                rows = response.get('values', [])
                i = 0
                code = code.lower()
                weapon = weapon.lower()
                for x in rows:
                    i = i + 1
                    for y in x:
                        y = y.lower()
                        if y == weapon and code != "skill":
                            if code == "acc":
                                if game_mode == "Pathfinder_old":
                                    strVal = "Главная!D" + str(i)
                                    return CubeSim_wrap(Read_Cell(player_name, strVal))
                                elif game_mode == "Pathfinder_simplified":
                                    strVal = "Главная!E" + str(i)
                                    return CubeSim_wrap(Read_Cell(player_name, strVal))
                            elif code == "dmg":
                                if game_mode == "Pathfinder_old":
                                    strVal = "Главная!I" + str(i)
                                    return CubeSim_wrap(Read_Cell(player_name, strVal))
                                elif game_mode == "Pathfinder_simplified":
                                    strVal = "Главная!K" + str(i)
                                    return CubeSim_wrap(Read_Cell(player_name, strVal))
                        elif code == "skill":
                            if y == weapon:
                                strVal = "Навыки!I" + str(i+2)
                                return CubeSim_wrap(Read_Cell(player_name, strVal))

            except HttpError as err:
                print(err)


def What_Do(player_name, command, game_mode):
    if player_name is not None:
        if game_mode is not None:
            if game_mode == "Pathfinder_old":
                command = command.lower()
                if "инициатива" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!F12"))
                elif "тест" in command:
                    return CubeSim_wrap(Read_Cell(player_name, 'Главная!N24'))
                elif "тест2" in command:
                    return CubeSim_wrap(Read_Cell(player_name, 'Главная!N25'))
                elif "акробатика" in command:
                    return CubeSim_wrap(Read_Cell(player_name, 'Навыки!K8'))
                elif "дрессировка" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K3"))
                elif "лечение" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K4"))
                elif "выживание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K5"))
                elif "внимание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K6"))
                elif "проницательность" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K7"))
                elif "акробатика" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K8"))
                elif "лазание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K9"))
                elif "изворотливость" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K10"))
                elif "полет" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K11"))
                elif "верховая езда" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K12"))
                elif "плавание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K13"))
                elif "оценка" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K14"))
                elif "ремесло ()" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K15"))
                elif "знание (высший свет)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K16"))
                elif "знание (география)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K17"))
                elif "знание (инженерное дело)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K18"))
                elif "знание (история)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K19"))
                elif "знание (краеведение)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K20"))
                elif "знание (магия)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K21"))
                elif "знание (планы)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K22"))
                elif "знание (подземелья)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K23"))
                elif "знание (природа)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K24"))
                elif "знание (религия)" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K25"))
                elif "профессия ()" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K26"))
                elif "колдовство" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K27"))
                elif "обман" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K28"))
                elif "дипломатия" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K29"))
                elif "запугивание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K30"))
                elif "языкознание" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K31"))
                elif "исполнение ()" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K32"))
                elif "механика" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K33"))
                elif "маскировка" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K34"))
                elif "ловкость рук" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K35"))
                elif "скрытность" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Навыки!K36"))
                elif "стойкость" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C19"))
                elif "реакция" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C20"))
                elif "воля" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C21"))
                elif "использование магических устройств" in command:
                    return Read_Cell(player_name, "Навыки!K37")
            elif game_mode == "Pathfinder_simplified":
                command = command.lower()
                if "инициатива" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!F12"))
                if "стойкость" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C19"))
                if "реакция" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C20"))
                if "воля" in command:
                    return CubeSim_wrap(Read_Cell(player_name, "Главная!C21"))
                else:
                    return "Unsupported in this version, use <Skill> instead."
            elif game_mode is None:
                return "Please, set game mode!"
