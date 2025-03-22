import requests
import polars as pl

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
