import os
from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

years = [f"{current_year - i}-{str(current_year - i + 1)[2:]}" for i in range(5)]

cur_dir = os.getcwd()
folder_dir = cur_dir + '/website/webpages/previous teams'

for i,year in enumerate(years[:-1]):
    if years[-1] not in os.listdir(folder_dir):
        break
    os.rename(folder_dir + f"/{years[i+1]}", folder_dir + f"/{year}")
    

file_location = 'website/webpages/previous teams/index.html'

with open(file_location, 'r') as f:
    text = f.readlines()
    #print(text)
if years[0] not in text[66]:    
    with open(file_location, 'w') as f:
        for line in text:
            for i, year in enumerate(years):
                if year in line:
                    line = line.replace(year, years[years.index(year) - 1])
                    break
            f.write(line)