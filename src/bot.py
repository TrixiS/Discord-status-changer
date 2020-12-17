import asyncio
import itertools
import discord

from discord.ext import commands

class StatusBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.statuses_task = None
        self.statuses = itertools.cycle(kwargs.pop("statuses"))
        super().__init__(*args, **kwargs)

    async def _statuses_task(self):
        for status, time in self.statuses:
            if time <= 0:
                continue

            await self.change_presence(activity=discord.CustomActivity(
                name=status,
                # emoji="💵"
            ))

            print(f"Set status: {status}")

            await asyncio.sleep(time)

    async def on_ready(self):
        await self.wait_until_ready()

        print(f"Bot {str(self.user)} started.")

        if self.statuses_task is not None:
            try:
                self._statuses_task.cancel()
            except Exception:
                pass

        await self.change_presence(activity=discord.CustomActivity(
            name="Test test test"
        ))

        self.statuses_task = self.loop.create_task(self._statuses_task())

    async def process_commands(self, message):
        return
