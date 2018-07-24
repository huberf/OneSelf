# OneSelf

### Setup:

The initial setup is intended to be very minimal with virtually no steps until
you begin integrating your own data.
1. Run `git clone https://github.com/huberf/OneSelf`
2. Navigate there and you can begin the following steps (usually `cd OneSelf/`)

### MyFitnessPal
1. Run `pip install myfitnesspal`.
2. Set up your authentication information securely by running `myfitnesspal
   store-password my_username`. The package creator engineered it so your
   password is securely stored and code can therefore be pushed to GitHub easily
   without containing keys, etc.
3. In `config.json`, edit the `myfitnesspal` key to provide your username.
4. Run `python3 sync/getMyFitnessPal.py`.
5. Now with your data, run `python3 process/nutrition-tracker.py` to get an
   array of insights from your data.

### Mint Finance
1. First visit, mint.intuit.com and sign-in to your account.
2. Visit https://mint.intuit.com/transaction.event?filterType=cash and press
   "Export" at the bottom of the page.
3. Place the downloaded file in the `records/` directory with the name
   `mint_transactions.csv`.
4. Test the setup by running `python3 process/mint_finance.py`. It should print
   useful metrics and give an overview of its general capabilities.

### WakaTime

You have multiple options. One is to export your data and the other is to use
the API but the API requires a subscription to retreive historical data and is
currently unsupported by OneSelf.
Data export:
1. Visit [https://wakatime.com/settings/account](https://wakatime.com/settings/account)
2. Scroll down to the export section and follow the prompts.
3. Place the export file in `records/` and name it `wakatime-export.json`.

### Last.fm

Our sync method uses the last.fm API and will require some authentication on
your end.

### Coming soon(er or later)
* Garmin
* Nomie
* Last.fm
* Strava
* WakaTime
* RescueTime
* Trakt.tv
* Welltory
* Moves
* Gyroscope
* Goodreads

### Philosophy
Health science and productivity are bound to improve when millions of
individuals closely analyze their personal data and the collective insights of
the masses. We should fight for data availability and build solutions for
ourselves to track new metrics and enhance the insights of others. The key to
immortality may very well already exist in the collective insights we can gather
through data collection and analysis.

### Contributing
Please feel free to open an issue or PR if you've found a bug. If you're looking
to implement a feature, please open an issue before creating a PR so I can
review it and make sure it's something that should be added.
