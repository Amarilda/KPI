import datetime
import json

def ThinkingTheFeelings():
    with open("MSC/main.json", "r") as json_file:
        main = json.load(json_file)

    if max(main.keys()) != str((datetime.datetime.now()).date()):
        
        with open("MSC/priorities.json", "r") as json_file:
            priorities = json.load(json_file)

        daily = {}
        day = str(datetime.date.today())
        yesterday = str(datetime.date.today() - datetime.timedelta(1))
        cat_is_binary = ['keto', 'journaling',  'meditation',  'magnesium', 'Karense', 'Nils', 'Stein på stein', 'Python cleanup']
        valid_inputs = ['1' , '0']

        main[day] = daily
        main[day]['base'] = {}
        main[day]['emotional_state'] = {}
        main[day]['what_was_I_thinking_yesterday'] = {}

        for metric in priorities['base']:
            print(metric)
            i = input() or 0
            main[day]['base'][metric] = i

        for emotion in priorities['emotional_state']:
            print(emotion)
            i = input() or 0
            main[day]['emotional_state'][emotion] = i

        try:
            yesterday_task = main[yesterday]['base']['top task for tomorrow (VERB)']
            print('did you '+yesterday_task +' today?')
            answer = input()
            main[day]['what_was_I_thinking_yesterday'][yesterday_task] = answer
        except:pass

# check if binary choices work
        if main[day]['base']['Are you chasing girl boss goals today?'].lower().strip() == 'n':
            pass
        else:
            sub_dict = priorities['KPIS'][max(priorities['KPIS'].keys())]
            for category in  sub_dict:
                main[day][category] = {}

                for question in sub_dict[category]:
                    print(question)
                    if question in cat_is_binary:
                        i = -1
                        while i not in valid_inputs:
                            i = input() or '0'
                    else:
                        i = input() or '0'

                    
                    main[day][category][question] = i

        with open('MSC/main.json', 'w') as outfile:
            json.dump(main, outfile)

    else:        pass