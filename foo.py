from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

years = [f"{current_year - i}-{str(current_year - i + 1)[2:]}" for i in range(5)]

print(years)