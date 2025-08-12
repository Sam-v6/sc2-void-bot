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
from multiprocessing import Pool

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

def run_single_game(bot_class_name, bot_race, strat_name, opponent_race, difficulty, map_name, dev):

    # Set up the bot instance
    bot_instance = Bot(bot_race, bot_class_name())

    # Optional: DEV mode to skip logging
    if dev:
        os.environ["DEV"] = "1"

    # Output file paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    replay_name = f"{strat_name}_{map_name}_{timestamp}.SC2Replay"
    replay_path = os.path.join(os.getenv("VOID_BOT_HOME"), "replays", replay_name)

    try:
        print(f'Running {strat_name} on {map_name} vs {opponent_race}-{difficulty}...')
        result = run_game(
            maps.get(map_name),
            [bot_instance, Computer(opponent_race, difficulty)],
            realtime=False,
            save_replay_as=replay_path,
        )
        return (strat_name, opponent_race, difficulty, map_name, result.name)
    except Exception as e:
        print(f"Error running {strategy_name} on {map_name}: {e}")
        return (strat_name, opponent_race, difficulty, map_name, "ERROR")

if __name__ == "__main__":

    # Get the args
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Run in dev mode (no logging)")
    args = parser.parse_args()
    cpus = os.cpu_count()//2

    # Ensure paths exist
    os.makedirs(os.path.join(os.getenv("VOID_BOT_HOME"), "logs"), exist_ok=True)
    os.makedirs(os.path.join(os.getenv("VOID_BOT_HOME"), "replays"), exist_ok=True)

    # List of bots (bot class, race, name)
    bots = [
        (WarpGateBot, Race.Protoss, "warpgate_push"),
        (ProxyRaxBot, Race.Terran, "proxy_rax"),
        (MassReaperBot, Race.Terran, "reaper_rush"),
        (BCRushBot, Race.Terran, "bc_rush"),
        (ZergRushBot, Race.Zerg, "zergling_rush"),
    ]

    # Races
    races = [Race.Terran, Race.Protoss, Race.Zerg]

    # Difficulty
    difficulties = [
        Difficulty.VeryEasy,
        Difficulty.Easy,
        Difficulty.Medium,
        Difficulty.MediumHard,
        Difficulty.Hard,
        Difficulty.Harder,
        Difficulty.VeryHard
        ]

    # Get map list
    ladder_maps = []
    map_path = os.path.join(os.getenv("SC2PATH"), "Maps", "2025S2Maps")
    for f in os.listdir(map_path):
        if f.endswith(".SC2Map"):
            ladder_maps.append(f.split(".")[0])

    # Prepare job list (each is a tuple of inputs to `run_single_game`)
    jobs = []
    for bot_class, bot_race, strat_name in bots:
        for opponent_race in races:
            for difficulty in difficulties:
                for map_name in ladder_maps:
                    jobs.append((bot_class, bot_race, strat_name, opponent_race, difficulty, map_name, args.dev))

    # Run in parallel
    with Pool(processes=cpus) as pool:
        results = pool.starmap(run_single_game, jobs)

    # Save results
    df = pd.DataFrame(results, columns=['bot_strategy', 'opponent_race', 'difficulty', 'map', 'result'])
    df.to_csv(os.path.join(os.getenv("VOID_BOT_HOME"), "logs", "master_results.csv"), index=False)

