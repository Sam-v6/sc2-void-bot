# SC2 Imports
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer

# Base imports
import os
from datetime import datetime
import argparse

# Additional imports
import pandas as pd
import numpy as np

# Local imports
from bots.warpgate_push import WarpGateBot
from bots.proxy_rax import ProxyRaxBot
from bots.mass_reaper import MassReaperBot
from bots.one_base_battlecruiser import BCRushBot
from bots.zerg_rush import ZergRushBot
import pandas as pd

if __name__ == "__main__":

    # Get passed in args
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Run in dev mode (no logging)")
    args = parser.parse_args()

    # Set a process-level environment variable
    if args.dev:
        os.environ["DEV"] = "1"

    # Declare our bots in a tuple with bot and strat
    bots = [
            (Bot(Race.Protoss, WarpGateBot()), "warpgate_push"),
            (Bot(Race.Terran, ProxyRaxBot()), "proxy_rax"),
            (Bot(Race.Terran, MassReaperBot()), "reaper_rush"),
            (Bot(Race.Terran, BCRushBot()), "bc_rush"),
            (Bot(Race.Zerg, ZergRushBot()), "zergling_rush"),
            ]

    # Collect all the maps for SC2 AI Arena in 2025 Season 2
    ladder_maps = []
    map_path = os.path.join(os.getenv("SC2PATH"), "Maps", "2025S2Maps")
    for f in os.listdir(map_path):
        if f.endswith(".SC2Map"):
            ladder_maps.append(f)


    # Setup master csv for results
    log_dir = os.path.join(os.getenv("VOID_BOT_HOME"), "logs")
    os.makedirs(log_dir, exist_ok=True)
    master_csv_path = os.path.join(log_dir, "master_results.csv")

    # Create DataFrame that will hold our results
    rows = [m.split(".")[0] for m in ladder_maps]
    columns = [b[1] for b in bots]
    data = np.zeros(len(rows) * len(columns)).reshape(len(rows), len(columns))
    df = pd.DataFrame(data, index=rows, columns=columns)

    # Run games
    total_games = 0
    for bot in bots:
        for ladder_map in ladder_maps:
            print('----------------------------------------------------------------------------------------')
            
            # Get info
            map_name = ladder_map.split(".")[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Run the game
            result = run_game(
                maps.get(map_name),
                [bot[0], Computer(Race.Protoss, Difficulty.Medium)],
                realtime=False,
                save_replay_as=os.path.join(os.getenv("VOID_BOT_HOME"), "replays", f'{bot[1]}_{map_name}_{timestamp}.SC2Replay'),
            )

            # Store result
            if result.name == "Victory":
                df.at[map_name, bot[1]] += 1
            total_games += 1

    # Save master results
    #df = df / total_games
    df.to_csv(master_csv_path)
                
            

