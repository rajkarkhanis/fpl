import requests
import os
import polars as pl

season = "2024-25"

def fetch_global_data() -> pl.DataFrame:
    print("Getting global data")
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_gw(gw_num: int) -> pl.DataFrame:
    print(f"Getting data for gameweek {gw_num}")
    url = f"https://fantasy.premierleague.com/api/event/{gw_num}/live/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    df = pl.DataFrame(data["elements"])
    stats_df = pl.DataFrame(df["stats"].to_list())
    df = df.drop("stats").with_columns(stats_df)
    df = df.drop("explain")

    return df

def add_player_info(players: pl.DataFrame, teams: pl.DataFrame, positions: pl.DataFrame, gw: pl.DataFrame) -> pl.DataFrame:
    players = players.select(["id", "first_name", "second_name", "team", "element_type"])

    players = players.with_columns(
        (players["first_name"] + " " + players["second_name"]).alias("name")
    ).drop(["first_name", "second_name"])

    teams = teams.select(["id", "name"]).rename({"id": "team", "name": "team_name"})
    players = players.join(teams, on="team", how="left").drop("team")

    positions = positions.select(["id", "singular_name_short"]).rename({"id": "element_type", "singular_name_short": "position"})
    players = players.join(positions, on="element_type", how="left").drop("element_type")

    gw = gw.join(players, on="id", how="left")
    return gw

def save_to_csv(df: pl.DataFrame, gw: int) -> None:
    folder_path = f"data/{season}"
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{folder_path}/gw{gw}.csv"

    df.write_csv(filename)
    print(f"GW saved as: {filename}")


def main(latest_gw: int) -> None:
    global_data = fetch_global_data()
    players = pl.DataFrame(global_data["elements"])
    teams = pl.DataFrame(global_data["teams"])
    positions = pl.DataFrame(global_data["element_types"])

    for gw_num in range(1, latest_gw + 1):
        gw = fetch_gw(gw_num)
        print(f"Adding player info for gameweek {gw_num}")
        gw = add_player_info(players, teams, positions, gw)
        save_to_csv(gw, gw_num)

if __name__ == "__main__":
    latest_gw = 29
    main(latest_gw)
