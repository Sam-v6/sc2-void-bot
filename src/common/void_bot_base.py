from sc2.bot_ai import BotAI
from loguru import logger
from datetime import datetime
import os
import json

class VoidBotBase(BotAI):
    async def on_end(self, game_result):

        # Log when the game ended
        logger.info(f"{self.time_formatted} On end was called")

        # Create stats info
        os.makedirs(os.path.join(os.getenv('VOID_BOT_HOME'), 'logs'), exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        map_name = self.game_info.map_name.replace(" ", "_")
        filename = f"{self.__class__.__name__}_{map_name}_{timestamp}_stats.json"

        # Store data in a json
        stats_dict = {stat[0]: float(stat[1]) for stat in self.state.score.summary}
        with open(os.path.join(os.getenv('VOID_BOT_HOME'), 'logs', filename), "w") as f:
            json.dump(stats_dict, f, indent=4)

        # Get and specific bot logic
        await self.custom_on_end(game_result)

    # Each bot optionally overrides this
    async def custom_on_end(self, game_result):
        pass
