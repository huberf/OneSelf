import myfitnesspal
from utils import loadConfig

config = loadConfig.getConfig()

user_name = config['keys']['myfitnesspal']['username']
client = myfitnesspal.Client(user_name)

lastSync = (2013, 3, 2)
while current <= today:
  day = client.get_date(current.year, current.month, current.day)
  breakfast = day.meals[0]
  lunch = day.meals[1]
  dinner = day.meals[2]
