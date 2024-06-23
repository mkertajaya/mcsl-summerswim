
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob
import re


def convert_mcsl_data(htmlbasepath,filename_html,filename_output='output.csv'):
    #remove wildcard from htmlbasepath
    htmlbasepath_nowildcard = htmlbasepath.replace('/*.html', '')

    #define path
    htmlpath = os.path.join(htmlbasepath_nowildcard, f'{filename_html}')
    outputpath =  os.path.join(htmlbasepath_nowildcard, f'{filename_output}')

    #open file
    with open(htmlpath, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

    #get year and week based on html input file
    htmlfile_list = htmlbasepath.split('/')
    year = htmlfile_list[2] #this depends on path you gave
    week = htmlfile_list[3] #this depends on path you gave

    #process the rest of the file
    # Find all <h4> tags (event names)
    event_tags = soup.find_all('h4')

    # Initialize an empty list to store event data
    events = []

    # Loop through each event tag
    for event_tag in event_tags:
        event_name = event_tag.text.strip()

        # Find the corresponding table for each event
        table = event_tag.find_next('table')
        rows = table.find_all('tr')

        # Initialize an empty list for this event's data
        event_data = []

    # Loop through rows (skip the header row)
        for row in rows[1:]:
            cells = row.find_all('td')
            if cells:
                position, name, seed_time, final_time, points = [cell.text.strip() for cell in cells]
                event_data.append({
                    'position': position,
                    'name': name,
                    'seed_time': seed_time,
                    'final_time': final_time,
                    'points': points
                })

        # Append the event data to the list
        events.append({'event_name': event_name, 'data': event_data})

    # Create new list for dataframe
    data_list=[]
    for event in events:
        event_name = event['event_name']
        # print(f"Event Name: {event['event_name']}"
        for data in event['data']:
            # print(f"year: {year}, week: {week}, event: {event_name}, rank: {data['position']}, swimmer: {data['name']}, seed: {data['seed_time']}, final: {data['final_time']}, point: {data['points']}")
            data_list.append({
                        'year': year,
                        'week': week,
                        'event': event_name,
                        'rank': data['position'],
                        'swimmer': data['name'],
                        'seed': data['seed_time'],
                        'final': data['final_time'],
                        'point': data['points']
                    })

    #create dataframe
    df = pd.DataFrame(data_list) 

    #special handling for swimmer with () on its name
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Dan)', '- Dan'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Ben)', '- Ben'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Jojo)', '- Jojo'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Jorie)', '- Jorie'))

   #get event number
    df['event_no'] = df['event'].apply(lambda x:x.split('-')[0].replace('Event ', ''))
    #remove relay events (27,28,49,50) , i am using space at the end cause data has it
    df = df[~df['event_no'].isin(['27 ','28 ' ,'49 ','50 '])]

    #splitting swimmer colunn into 3
    df[['swimmer_name', 'swimmer_age', 'swimmer_team']] = df['swimmer'].str.split(pat='(', expand=True, n=2)
    #remove ')' from age and team
    df['swimmer_age'] = df['swimmer_age'].apply(lambda x:x.replace(')',''))
    df['swimmer_team'] = df['swimmer_team'].apply(lambda x:x.replace(')',''))

    # #add seconds for seed and final
    #function to do it
    def x_to_seconds(x):
        x = x.replace('X', '') #replacing exibition time
        x_list = x.split(':')
        if x in ('NT', 'NS', 'DQ', 'DNF'): # ignore NT, NS, DQ, and DNF
            return(x)
        elif len(x_list) == 1: #only seconds no minutes
            return(float(x_list[0]))
        else:
            return(float(x_list[0])*60 + float(x_list[1]))
    # x_to_seconds(x)


    df['seed_seconds'] = df['seed'].apply(lambda x:x_to_seconds(x))
    df['final_seconds'] = df['final'].apply(lambda x:x_to_seconds(x))

 
    #export to csv with | delimited
    df.to_csv(outputpath,sep='|', index=False, columns=['year','week','event','rank','swimmer','seed','final','swimmer_name','swimmer_age','swimmer_team','seed_seconds','final_seconds','event_no']) # Use pipe to seperate data

    #return test
    return(f'{htmlpath} is processed')


#file/folder
# html_loc = "/Users/mk/Documents/pyProject/mcsl-summwerswim/data/2019/week1/*.html"

htmlbasepath = "./data/2024/week2/*.html"
# filename_output = '2019.csv'
# filename_html = 'WvEW.html'

#read file in the folder:
for path in glob.glob(htmlbasepath):
    filename_html = path.split('/')[-1]
    print(filename_html)
    filename_output = filename_html.replace('.html', '.csv')
    result = convert_mcsl_data(htmlbasepath,filename_html,filename_output)
    print(result)

