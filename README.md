# FPL Gameweek Data

Since Vaastav will stop pushing updates to his [fpl](https://github.com/vaastav/Fantasy-Premier-League) repository after 2024-25 season, I figured I'll write my own FPL API scraper. My repository is not meant to be a direct replacement to Vaastav's.

I've only added the scripts about the data I actually used, which was gameweek by gameweek data on players. Also, I won't be adding the generated .csv files to VCS. You're gonna have to run the script and get them yourself.

Thanks to [Oliver Looney](https://www.oliverlooney.com/blogs/FPL-APIs-Explained) for explaining the FPL API endpoints.

## Instructions

### Clone the repository
```bash
git clone https://github.com/rajkarkhanis/fpl
cd fpl
```

### Create a virtual environment (optional but recommended)
I use conda, if you do as well:
```bash
conda activate fpl
```

If not:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Now there's a problem with the FPL API. The more interesting data points like player value, expected points, per 90 minutes, etc. are available on the `/bootstrap-static` endpoint which gets overwritten with new data after every completed gameweek.

So if you forget to get data for a previous gameweek, good luck. Now to actually get the data just:
```bash
python main.py
```

This will figure out which gameweek is the latest, fetch gameweek data for all players, and join with some extra stats from the `/bootstrap-static` endpoint.

## Things I might do

Now I kind of lied, there is a way to get player data from a previous gameweek. You can get player value from player details `/element-summary/{id}` endpoint but that's about it. The other more interesting data points are gone.

The problem with this is that you will make 15 x 700 = 10,500 API requests, if there have been 15 gameweeks and there are 700 players total. I'm not doing that.

Best not forget!
