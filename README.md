# OneSelf

## Setup:

### MyFitnessPal
1. Run `pip install myfitnesspal`.
2. Set up your authentication information securely by running `myfitnesspal
   store-password my_username`. The package creator engineered it so your
   password is securely stored and code can therefore be pushed to GitHub easily
   without containing keys, etc.
3. In `config.json`, edit the `myfitnesspal` key to provide your username.
3. Run `python3 sync/getMyFitnessPal.py`.
