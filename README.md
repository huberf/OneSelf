# OneSelf

### Setup:

The initial setup is intended to be very minimal with virtually no steps until
you begin integrating your own data.
1. Run `git clone https://github.com/huberf/OneSelf`
2. Navigate there and you can begin the following steps (usually `cd OneSelf/`)

### Proxy Collection
Currently this server supports sending data to the Nomie 2 app as well as
receiving data from Nomie 3 webhooks.
*Warning* This feature is under development and the safety and robustness of the
data collection is not guaranteed.
The server can be found in `collection-server/server.py` and started by
`python3 collection-server/server.py`

## Generic Processing

After setting up and syncing some services below, there are some general purpose
processing scripts currently or in production to support your own analysis. Running `python3
process/collators/hour_blocks.py` produces a sequence of csv files that contain
two columns `timestamp` and `value` which are aggregate values for various
metrics from connected services. These files can then be used to perform
regression between values between data services.

## Services

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

### 23&Me Genetic Data

In the settings section, request your full data export. Place the unzipped
`.txt` file in `records/` with the name `genome_data.txt`.

### Last.fm

Our sync method uses the last.fm API and will require some authentication on
your end. We use the `lastpy` package which requires additional setup and can
be viewed at
[github.com/huberf/lastfm-scrobbler](https://github.com/huberf/lastfm-scrobbler)
Once setup, merely run `python3 sync/getLastfm.py`.


### Trakt.tv

You need Trakt.tv VIP to do CSV exports. Once you have that, follow the below
steps to collect the data.
1. Visit https://trakt.tv/users/USER_NAME/history replacing USER_NAME with
   your username.
2. Press the CSV export button.
3. Place the export file in `records/` and name it `trakt.csv`
4. You can now execute `python3 process/trakt_tv.py` to analyze your viewing
   habits.


### Goodreads

The current implementation requires a manual export.
1. Visit
   [https://www.goodreads.com/review/import](https://www.goodreads.com/review/import)
   and press "Export Library".
2. Take the exported file and place in `records/` with the name
   `goodreads_library_export.csv`.
3. To see interesting statistics and insights simply run `python3
   process/goodreads.py` from the root project directory.


### Strava

This requires some development experience as it directly uses the Strava API.
You'll need to setup an API access account with Strava at
[https://developers.strava.com/](https://developers.strava.com/). Then in
`config.json` located in the root directory of this repo, edit the `strava`
section to add your username, access_token, and runner_id (this is a number
associated with your Strava account). You can find your `runner_id` by going to
your profile page on Strava and looking at the URL to find the number at the
very end. You are now ready to execute `python3 sync/getStrava.py`. Note:
Everytime this runs, it will collect every single activity in your account with
full GPS data so may take some time depending upon how many activities
you have.
Analysis scripts are coming soon, but feel free to design one yourself and
submit it as a PR.


### Garmin

Unfortunately, the Garmin API is fairly closed off and currently, this project
only supports acquiring summary details for your Garmin activities. To do this,
go to
[https://connect.garmin.com/modern/activities](https://connect.garmin.com/modern/activities)
and scroll to the bottom. Continue scrolling until all activities are loaded.
Then go back to the top, and click `Export CSV`. Put the exported CSV in the
`records/` directory of this project titled `garmin-activities.csv`.
You can now run the processing script `python3 process/garmin.py` to view data
and generate reports.


### RescueTime

Currently, the RescueTime API isn't supported (and without Premium only provides
limited data access). Rather, one will need to go to the RescueTime data export
page and request a full export of logged time at
[https://www.rescuetime.com/accounts/your-data](https://www.rescuetime.com/accounts/your-data).
Place the generated CSV file in the `records/` directory with the name
`rescuetime-data.csv`.
Full processing scripts and reports are coming soon.


### Swarm (Foursquare)

This sync method uses the Foursquare API, so the first step is to create an app
in Foursquare's developer system in order to get an API key. Go to
[https://foursquare.com/developers/register](https://foursquare.com/developers/register)
and create an app with permission "Access to Check-In or User Data". You will
now have a "Client ID" and "Client Secret". Modify `config.json` in the root of
this project to include these keys.

Now you will need to get user authentication. The full steps are at
[https://developer.foursquare.com/docs/api/configuration/authentication](https://developer.foursquare.com/docs/api/configuration/authentication)
but all of this can be done manually. You will first need to enter
`https://foursquare.com/oauth2/authenticate?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI`
in your browser, replacing capitalized components with the corresponding
information.

Next, grab the `?code=CODE` section from the URL you are redirected to. And now
finally visit, in your browser, `https://foursquare.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI&code=CODE`
once again replacing the capitalized parts with the correct information.

Finally, from the JSON response, grab the access code and put the access code in
`config.json` under `access_code` in the `foursquare` section.


### Gyroscope

There is presently no public API so all data exports will be done by visiting
[https://gyrosco.pe/export](gyroso.pe/export) and exporting desired metrics. To
export, visit the link and export a report, saving it to disk. Without changing
the name, place it in the `records/gyroscope/` folder. Some data such as HR is
limited to the last month or other such ranges, so if there are multiple ones,
place them in the same folder above except with different endings after the name
Gyroscope gives the file (e.g. `gyroscope-Noah-hr-export.csv` to
`gyroscope-Noah-hr-export(4).csv`). All processing scripts will load all files
relating to the specific metric and collate them, removing duplicate entries in
memory without modifying the actual record files.

Processing scripts are still to be constructed...

### Coming soon(er or later)
* Nomie
* Welltory
* Moves

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
