# Base imports
import os

# Additional imports
import pandas as pd


class Plotter:

    def __init__(self, log_dir):
        # Class vars
        self._log_dir = log_dir
        self._plot_dir = os.path.join(os.path.dirname(self._log_dir).replace("logs", "plots"))

        # Init
        self._initialize()

    def plot(self) -> None:
        # Create all plots
        _plot_economy()
        _plot_army_size()
        _plot_technology()
        _plot_apm()

        # Create log columns
        _log_columns()

    def _initialize(self) -> None:
        # Make plot dir
        os.makedirs(self._plot_dir, exist_ok=True)

    def _plot_economy(self) -> None:
        fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

        ax.plot(self._data["game_time"], self._data["game_time"], label="sin(x)", color="blue")
        ax.plot(self._data["game_time"], y2, label="cos(x)", color="red")

        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.set_title("Sine and Cosine Functions", fontsize=14)
        ax.legend(loc="upper right", fontsize=10)
        ax.set_xticks(np.arange(0, 11, 2))   # ticks every 2 units on x-axis
        ax.set_yticks(np.arange(-1, 1.1, 0.5))  # ticks every 0.5 on y-axis
        ax.tick_params(axis="both", which="major", labelsize=10)
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.tight_layout()
        plt.savefig(os.path.join(self._plot_dir, "economy.png"))
        pass

    def _plot_army_size(self) -> None:
        pass

    def _plot_technology(self) -> None:
        pass

    def _plot_apm(self) -> None:
        pass

    def _log_columns(self) -> None:
        # Save columns to text file
        with open('columns.txt', 'w') as f:
            for col in df.columns:
                f.write(f"{col}\n")

if __name__ == "__main__":

    # Path
    path = os.path.join(os.getenv("VOID_BOT_HOME"), "logs", "master_results.csv")

    # Load a parquet file
    df = pd.read_parquet("/home/sam/repos/sc2-repos/sc2-void-bot/logs/BCRushBot_Torches_AIE_20250817_095542.parquet")

    # See the first few rows
    print(df.head())

    print(df["collected_minerals"])

    # Save columns to text file
    with open('columns.txt', 'w') as f:
        for col in df.columns:
            f.write(f"{col}\n")

    # Peek at specific columns