import pandas as pd
import requests, json

import datetime

from credentials import notion_new_token
from  deepdiff import DeepDiff

def notion():

    headers = {'Authorization': f"Bearer {notion_new_token}", 
            'Content-Type': 'application/json', 
            'Notion-Version': '2022-06-28'}

    db = requests.post(f'https://api.notion.com/v1/search',  headers=headers).json()

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(db, f, ensure_ascii=False)

    with open("db.json", "r") as json_file:
        db = json.load(json_file)

    with open("notion.json", "r") as json_file:
        notion = json.load(json_file)

    day = str(datetime.date.today())
    notion[day] = {}

    Lenght = len(db['results'])

    #sorted df of notion scrape
    df = pd.DataFrame(columns=  ['title', 'created date','tags'])

    for number in range(0,Lenght): 
        answer = []
        result = db['results'][number]
        i = {}
        #title

        if result['properties']['Name']['title'] == {}:
            Lenght -= 1
            pass
        else: 
            try:
                answer.append(eval(str(result['properties']['Name']['title'])[1:-1])['plain_text']) 
            except: answer.append("")
            answer.append(result['created_time'])

            #tags
            new_frame = eval(str(result['properties']['Tags']['multi_select'])[1:-1])
            lenghth = len(new_frame)
            tags = {}
            if len(result['properties']['Tags']['multi_select']) == 1:
                tags[0] = eval(str(result['properties']['Tags']['multi_select'])[1:-1])['name']
            else: 
                for num in range (0, lenghth):
                    tags[num] = new_frame[num]['name']
            i['tags'] = tags
            
            answer.append(tags)

            df.loc[len(df)] = answer
            df.sort_values(by = ['created date','title'], inplace = True)
            df.reset_index(drop = True, inplace = True)

    #insert into notion, the oldest entry first
    for number in range(0, Lenght):
        i = {}
        for column_name in ['title', 'created date', 'tags']:
            i[column_name] =   df.iloc[number][column_name]

        notion[day][str(number)] = i 

    #old vs new
    compare = DeepDiff(notion[list(notion.keys())[-2]], notion[list(notion.keys())[-1]])
    print(compare)
    compare_len = len(compare)
    print(f' { compare_len }  amendments made to Notion')

    if compare_len != 0:
        with open('notion.json', 'w', encoding='utf8') as f:
            json.dump(notion, f, ensure_ascii=False) 
    else:pass