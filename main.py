import os
import polars as pl
import api
from typing import Optional

season = "2025-26"

def get_latest_gw(events: pl.DataFrame) -> Optional[int]:
    completed_gw = events.filter(events["finished"] == True)
    if completed_gw.is_empty():
        print("No gameweeks are completed!")
        return None

    return completed_gw.select("id").max().item()

def add_player_info(players: pl.DataFrame, teams: pl.DataFrame, positions: pl.DataFrame, gw: pl.DataFrame) -> pl.DataFrame:
    players = players.select(["id", "first_name", "second_name", "team", "element_type", "now_cost", "ep_this", "ep_next", "selected_by_percent", "expected_goals_per_90", "expected_goal_involvements_per_90", "expected_goals_conceded_per_90", "goals_conceded_per_90", "starts_per_90", "clean_sheets_per_90"])

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


def main() -> None:
    global_data = api.fetch_global_data()
    players = pl.DataFrame(global_data["elements"])
    teams = pl.DataFrame(global_data["teams"])
    positions = pl.DataFrame(global_data["element_types"])

    latest_gw = get_latest_gw(pl.DataFrame(global_data["events"]))
    if latest_gw is None:
        return

    gw = api.fetch_gw(latest_gw)
    print(f"Adding player info for gameweek {latest_gw}")
    gw = add_player_info(players, teams, positions, gw)
    save_to_csv(gw, latest_gw)

if __name__ == "__main__":
    main()
