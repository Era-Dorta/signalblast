#!/usr/bin/env python
#
# This code is heavily based on
# https://github.com/lwesterhof/semaphore/blob/19b949d336a2dafbddd26325db21fba2ed74d292/examples/broadcastbot.py
# See there for authorship
#
import argparse
import anyio
import os
from semaphore import Bot
from logging import INFO
from typing import Optional


from bot_answers import BotAnswers
from bot_commands import CommandRegex
from utils import get_logger, redirect_semaphore_logger


async def main(admin_pass: Optional[str]):
    """Start the bot."""

    log_file = '/var/log/signalblast.log'
    logger = get_logger(log_file, logging_level=INFO)
    redirect_semaphore_logger(log_file)

    os.makedirs('./data', exist_ok=True)

    # Connect the bot to number.
    async with Bot(os.environ["SIGNAL_PHONE_NUMBER"], logging_level=INFO) as bot:
        bot_answers = BotAnswers(logger, admin_pass)

        bot.register_handler(CommandRegex.subscribe.value, bot_answers.subscribe)
        bot.register_handler(CommandRegex.unsubscribe.value, bot_answers.unsubscribe)
        bot.register_handler(CommandRegex.broadcast.value, bot_answers.broadcast)
        bot.register_handler(CommandRegex.add_admin.value, bot_answers.add_admin)
        bot.register_handler(CommandRegex.remove_admin.value, bot_answers.remove_admin)
        bot.register_handler(CommandRegex.msg_to_admin.value, bot_answers.msg_to_admin)
        bot.register_handler(CommandRegex.msg_from_admin.value, bot_answers.msg_from_admin)
        bot.register_handler(".*", bot_answers.display_help)

        # Run the bot until you press Ctrl-C.
        await bot.start()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--admin_pass", type=str, required=False, help="the password to add or remove admins")

    args = args_parser.parse_args()
    anyio.run(main, args.admin_pass)
