#!/usr/bin/env python3
"""
Database updater tenderly.

(c) Copyright Bprotocol foundation 2023.
Licensed under MIT
"""

from fastlane_bot import Bot, Config

bot = Bot(ConfigObj=Config.new(config=Config.CONFIG_TENDERLY))
bot.update(udtype=bot.UDTYPE_FROM_CONTRACTS, drop_tables=False, only_carbon=False, top_n=10)
