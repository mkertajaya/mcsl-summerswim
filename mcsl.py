
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob


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
    table = soup.find("table")
    cols = table.findAll("td")

    content = []
    result = []
    record = []

    for td in cols:
        try:
            string = ''.join(td.find(string=True))
            content.append(string)
        except: pass

    event = content[0]

    #loop the rest
    for line in content:
        if line[0:5] == 'Event':
            event = line
        else:
            #start of new record, when it sees rank
            if (line[1:2] == '.' and len(line)==2) or (line[2:3] == '.' and len(line) == 3) or (line[2:3] == 'T' and len(line) == 4): #T is for tie
                if result:
                    record.append(result)
                    result = []
                result.append(year)
                result.append(week)
                result.append(event)
                result.append(line)
            else:
                result.append(line)

    #take out relay record,
    individual_record = []
    for l in record:
        if 'Relay' not in l[2]: #third element on the list is where the event is located
            #print(l)
            individual_record.append(l)
    
    #create dataframe
    df = pd.DataFrame(individual_record, columns =['year', 'week', 'event', 'rank', 'swimmer', 'seed', 'final']) 

    #special handling for swimmer with () on its name
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Dan)', '- Dan'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Ben)', '- Ben'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Jojo)', '- Jojo'))
    df['swimmer'] = df['swimmer'].apply(lambda x:x.replace('(Jorie)', '- Jorie'))


    #splitting swimmer colunn into 3
    df[['swimmer_name', 'swimmer_age', 'swimmer_team']] = df['swimmer'].str.split(pat='(', expand=True)
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

    #get event number
    df['event_no'] = df['event'].apply(lambda x:x.split('-')[0].replace('Event ', ''))

    #export to csv with | delimited
    df.to_csv(outputpath,sep='|', index=False) # Use pipe to seperate data

    #return test
    return(f'{htmlpath} is processed')


#file/folder
# html_loc = "/Users/mk/Documents/pyProject/mcsl-summwerswim/data/2019/week1/*.html"

htmlbasepath = "./data/2023/week1/*.html"
# filename_output = '2019.csv'
# filename_html = 'WvEW.html'

#read file in the folder:
for path in glob.glob(htmlbasepath):
    filename_html = path.split('/')[-1]
    print(filename_html)
    filename_output = filename_html.replace('.html', '.csv')
    result = convert_mcsl_data(htmlbasepath,filename_html,filename_output)
    print(result)

