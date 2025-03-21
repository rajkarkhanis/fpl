import requests
import os
import polars as pl

season = "2024-25"

def fetch_gw(gw_num: int) -> pl.DataFrame:
    url = f"https://fantasy.premierleague.com/api/event/{gw_num}/live/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    df = pl.DataFrame(data["elements"])
    stats_df = pl.DataFrame(df["stats"].to_list())
    df = df.drop("stats").with_columns(stats_df)
    df = df.drop("explain")

    return df

def save_to_csv(df: pl.DataFrame, gw: int) -> None:
    folder_path = f"data/{season}"
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{folder_path}/gw{gw}.csv"

    df.write_csv(filename)
    print(f"GW saved as: {filename}")


def main(latest_gw: int) -> None:
    for gw in range(1, latest_gw + 1):
        df = fetch_gw(gw)
        save_to_csv(df, gw)

if __name__ == "__main__":
    latest_gw = 3
    main(latest_gw)
