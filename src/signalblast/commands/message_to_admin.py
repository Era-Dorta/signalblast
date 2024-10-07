import asyncio
import functools
from re import Pattern
from typing import Optional

from signalbot import Command
from signalbot import Context as ChatContext

from signalblast.broadcastbot import BroadcasBot
from signalblast.commands_strings import AdminCommandStrings, CommandRegex, PublicCommandStrings
from signalblast.utils import triggered


class MessageToAdmin(Command):
    def __init__(self, bot: BroadcasBot) -> None:
        super().__init__()
        self.broadcastbot = bot

    @triggered(CommandRegex.msg_to_admin)
    async def handle(self, ctx: ChatContext) -> None:
        try:
            subscriber_uuid = ctx.message.source_uuid
            message = self.broadcastbot.message_handler.remove_command_from_message(
                ctx.message.text, PublicCommandStrings.msg_to_admin
            )

            if self.broadcastbot.admin.admin_id is None:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "I'm sorry but there are no admins to contact!")
                self.broadcastbot.logger.info(f"Tried to contact an admin but there is none! {subscriber_uuid}")
                return

            if subscriber_uuid in self.broadcastbot.banned_users:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "You are not allowed to contact the admin!")
                self.broadcastbot.logger.info(f"Banned user {subscriber_uuid} tried to contact admin")
                return

            msg_to_admin = self.broadcastbot.message_handler.compose_message_to_admin(
                "Sent you message:\n", subscriber_uuid
            )
            msg_to_admin += message
            attachments = self.broadcastbot.message_handler.empty_list_to_none(ctx.message.base64_attachments)
            await self.broadcastbot.send(self.broadcastbot.admin.admin_id, msg_to_admin, base64_attachments=attachments)
            self.broadcastbot.logger.info(
                f"Sent message from {subscriber_uuid} to admin {self.broadcastbot.admin.admin_id}"
            )
        except Exception as e:
            self.broadcastbot.logger.error(e, exc_info=True)
            try:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "Failed to send the message to the admin!")
            except Exception as e:
                self.broadcastbot.logger.error(e, exc_info=True)
