import asyncio
import functools
from re import Pattern
from typing import Optional

from signalbot import Command
from signalbot import Context as ChatContext

from signalblast.broadcastbot import BroadcasBot
from signalblast.commands_strings import AdminCommandStrings, CommandRegex, PublicCommandStrings
from signalblast.utils import triggered


class DisplayHelp(Command):
    def __init__(self, bot: BroadcasBot) -> None:
        super().__init__()
        self.broadcastbot = bot

    def _get_help_message(self, input_message: str, subscriber_uuid: str) -> str:
        if input_message.startswith(PublicCommandStrings.help):
            is_wrong_command = False
        else:
            is_wrong_command = True

        if subscriber_uuid != self.broadcastbot.admin.admin_id:
            if is_wrong_command:
                return self.broadcastbot.wrong_command_message
            return self.broadcastbot.help_message
        if is_wrong_command:
            return self.broadcastbot.admin_wrong_command_message
        return self.broadcastbot.admin_help_message

    @triggered(CommandRegex.help)
    async def handle(self, ctx: ChatContext) -> None:
        try:
            subscriber_uuid = ctx.message.source_uuid
            message = ctx.message.text

            help_message = self._get_help_message(message, subscriber_uuid)

            await self.broadcastbot.reply_with_warn_on_failure(ctx, help_message)
            self.broadcastbot.logger.info(f"Sent help message to {subscriber_uuid}")
        except Exception as e:
            # if isinstance(e, StopPropagation):
            #     raise
            self.broadcastbot.logger.error(e, exc_info=True)
