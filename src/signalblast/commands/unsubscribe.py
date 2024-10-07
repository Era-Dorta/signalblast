from signalbot import Command
from signalbot import Context as ChatContext

from signalblast.broadcastbot import BroadcasBot
from signalblast.commands_strings import CommandRegex
from signalblast.utils import triggered


class Unsubscribe(Command):
    def __init__(self, bot: BroadcasBot) -> None:
        super().__init__()
        self.broadcastbot = bot

    @triggered(CommandRegex.unsubscribe)
    async def handle(self, ctx: ChatContext) -> None:
        try:
            subscriber_uuid = ctx.message.source_uuid

            if subscriber_uuid not in self.broadcastbot.subscribers:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "Not subscribed!")
                self.broadcastbot.logger.info(f"{subscriber_uuid} tried to unsubscribe but they are not subscribed")
                return

            await self.broadcastbot.subscribers.remove(subscriber_uuid)
            await self.broadcastbot.reply_with_warn_on_failure(ctx, "Successfully unsubscribed!")
            self.broadcastbot.logger.info(f"{subscriber_uuid} unsubscribed")
        except Exception as e:
            self.broadcastbot.logger.error(e, exc_info=True)
            try:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "Could not unsubscribe!")
            except Exception as e:
                self.broadcastbot.logger.error(e, exc_info=True)