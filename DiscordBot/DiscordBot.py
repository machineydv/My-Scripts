#!/usr/bin/python3

import asyncio

from nextcord import Client
from nextcord import Intents
from random import randrange
from datetime import datetime
from humanize import intcomma
from os import getenv as os_getenv
from re import search as re_search
from re import IGNORECASE

from lib.Globals import discord_server, repo_names
from lib.Globals import global_headers, repositories, my_repositories
from lib.Functions import fetch_corona_infection
from lib.Functions import fetch_pulls, fetch_stars_subs
from lib.Functions import corona_news_launch

intents = Intents.default()
intents.members = True
intents.messages = True

stonedbot_token = os_getenv('STONEDBOT_ACCESS_TOKEN')
if not stonedbot_token:
    print("Token not found")
    exit()

class BotHelper:
    def __init__(self):
        self.corona_string = self.corona()
        self.personal_string = self.personal()
        self.other_string = self.other()

    def corona(self):
        send_string = ""
        infection, death = fetch_corona_infection()
        send_string += f"**SARS-CoV-2 Status** ({datetime.now().strftime('%B %d %Y %H:%M:%S')})\n"
        send_string += f"Infection: {intcomma(infection)}\nDeath: {intcomma(death)}\n"
        return send_string

    def personal(self):
        send_string = ""
        for _ in repositories:
            active, closed = fetch_pulls(f"https://github.com/{_}/pulls")
            reponame = _.split('/')[-1]
            reponame = repo_names[f"{_.split('/')[-1]}"]
            send_string += f"**{reponame}**: \nActive: {intcomma(active)} :white_check_mark:, Total: {intcomma(active + closed)} :skull_crossbones:\n"
        return send_string

    def other(self):
        send_string = ""
        for _ in my_repositories:
            stars, subs = fetch_stars_subs(f"https://api.github.com/repos/{_}/")
            send_string += f"**{_.split('/')[-1]}**: \nStars: {stars} :star:, Watching: {subs} :sunglasses:\n"
        return send_string

helper = BotHelper()

class BotClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        corona_news_launch()
        self.loop.create_task(self.publish_corona(helper.corona_string))
        self.loop.create_task(self.publish_personal(helper.personal_string))
        self.loop.create_task(self.publish_other(helper.other_string))

    async def on_member_join(self, member):
        pass

    async def on_message(self, message):
        pass

    async def on_ready(self):
        print(f'Logged in as: {self.user.name}({self.user.id})')

    async def publish_corona(self, message):
        await self.wait_until_ready()
        channel = self.get_channel(790767464229109811)
        while True:
            await channel.send(message)
            await asyncio.sleep(randrange(86400))

    async def publish_personal(self, message):
        await self.wait_until_ready()
        channel = self.get_channel(803301891772907552)
        while True:
            await channel.send(message)
            await asyncio.sleep(randrange(86400))

    async def publish_other(self, message):
        await self.wait_until_ready()
        channel = self.get_channel(803301891772907552)
        while True:
            await channel.send(message)
            await asyncio.sleep(randrange(86400))

client = BotClient(intents=intents)
client.run(stonedbot_token)

