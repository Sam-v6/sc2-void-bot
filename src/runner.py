# SC2 Imports
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer

# Base imports
import os
from datetime import datetime

# Local imports
from bots.warpgate_push import WarpGateBot
from bots.proxy_rax import ProxyRaxBot
from bots.zerg_rush import ZergRushBot

if __name__ == "__main__":

    # Declare our bots in a tuple with bot and strat
    bots = [
            (Bot(Race.Protoss, WarpGateBot()), "warpgate_push"),
            (Bot(Race.Terran, ProxyRaxBot()), "proxy_rax"),
            (Bot(Race.Zerg, ZergRushBot()), "zergling_rush"),
            ]

    # Collect all the maps for SC2 AI Arena in 2025 Season 2
    ladder_maps = []
    map_path = os.path.join(os.getenv("SC2PATH"), "Maps", "2025S2Maps")
    for f in os.listdir(map_path):
        if f.endswith(".SC2Map"):
            ladder_maps.append(f)

    # Run games
    for bot in bots:
        for ladder_map in ladder_maps:
            print('----------------------------------------------------------------------------------------')
            map_name = ladder_map.split(".")[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result = run_game(
                maps.get(map_name),
                [bot[0], Computer(Race.Protoss, Difficulty.Medium)],
                realtime=False,
                save_replay_as=os.path.join(os.getenv("VOID_BOT_HOME"), "replays", f'{bot[1]}_{map_name}_{timestamp}.SC2Replay'),
            )
        
