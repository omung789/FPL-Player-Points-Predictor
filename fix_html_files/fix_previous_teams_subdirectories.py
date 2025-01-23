import os
from datetime import date
import shutil

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

gameweek = 23

years = [f"{current_year - i}-{str(current_year - i + 1)[2:]}" for i in range(5)]

cur_dir = os.getcwd()
folder_dir = cur_dir + '/website/webpages/previous teams'

# move best teams to the correct year if already calculated (will be the case for 2 oldest years)
years_to_be_moved = years[1:len(years) - 2]
years_to_be_moved.reverse()
for i,year in enumerate(years_to_be_moved):
    year_dir = folder_dir + f"/{year}/index.html"

    with open(year_dir, 'r') as f:
        text = f.readlines()
        #print(text)
    
    correct_year = False
    
    for line in text:
        if year in line:
            correct_year = True
            break
    
    if correct_year:
        continue
    
    shutil.copy(year_dir, folder_dir + f"/{years[years.index(year) + 1]}/index.html")


def get_num_spaces(line):
    num_spaces = 0
    for i in range(len(line)):
        if line[i] == ' ':
            num_spaces += 1
        else:
            break
    return num_spaces

#use html_strings files to update the html files
for k,year in enumerate(years[:2]):
    year_dir = folder_dir + f"/{year}/index.html"

    with open(year_dir, 'r') as f:
        text = f.readlines()
        #print(text)

    correct_year = False
    
    #dont want to touch files for previous years if they have already been updated
    #but for current season we will want to update the file every gameweek
    if year != years[0]:
        for line in text:
            if year in line:
                correct_year = True
                break
    
    if correct_year:
        continue

    html_strings_dir = cur_dir + f"/data/{year}/html_strings_{year}.txt"

    with open(html_strings_dir, 'r') as f:
        html_strings = f.readlines()

    for i,line in enumerate(text):
        if years[k+1] in line:
            line = line.replace(years[k+1], year)
            text[i] = line
        if f'Best overall team from {year}' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line, (num_spaces) * ' ' + f'Best overall team from {year} season so far (After {gameweek - 1} gameweeks)')
        elif 'Total Points' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces) * ' ' + html_strings[-2])
            text[i] = line
        elif 'Total Cost' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces) * ' ' + html_strings[-1])
            text[i] = line
        elif 'player goalkeeper' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces - 2) * ' ' + html_strings[0])
            text[i] = line
            start_of_outfield = i + 1
        elif '<div class="bench">' in line:
            num_spaces = get_num_spaces(text[i])
            for j in range(4):
                text[i + j + 1] = (num_spaces + 2) * ' ' + html_strings[11 + j]
            break

    new_team = []

    num_spaces = get_num_spaces(text[start_of_outfield])

    num_defenders, num_midfielders, num_forwards = 0, 0, 0
    for i in range(1,11):
        if 'defender' in html_strings[i]:
            if num_defenders == 0:
                new_team.append((num_spaces - 2) * ' ' + '<div class="defenders">\n')
            num_defenders += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
        elif 'midfielder' in html_strings[i]:
            if num_midfielders == 0:
                new_team.append((num_spaces - 2) * ' ' + '</div>\n')
                new_team.append((num_spaces - 2) * ' ' + '<div class="midfielders">\n')
            num_midfielders += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
        elif 'forward' in html_strings[i]:
            if num_forwards == 0:
                new_team.append((num_spaces - 2) * ' ' + '</div>\n')
                new_team.append((num_spaces - 2) * ' ' + '<div class="forwards">\n')
            num_forwards += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
    new_team.append((num_spaces - 2) * ' ' + '</div>\n')

    for i in range(start_of_outfield, start_of_outfield + len(new_team)):
        text[i] = new_team[i - start_of_outfield]

    with open(year_dir, 'w') as f:
        for line in text:
            f.write(line)
    

