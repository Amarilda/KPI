import pandas as pd
from datetime import date
import random

verbs = pd.read_excel("verbs.xlsx")
df = pd.read_excel("VerbBender.xlsx")

def VerbBender():
    num = random.randrange(0, len(verbs))
    tenses = ['Infinitive','Present tense','Past tense','Past participle']
    print(verbs['English'][num])

    counter = 0
    atbilde = []
    atbilde.append(date.today().strftime("%d/%m/%Y"))
    atbilde.append(verbs['English'][num])
    for i in tenses:

        print(i)
        answer= input()
        atbilde.append(answer)

        if verbs[i][num] != answer:
            print(verbs[i][num])
            counter+= 1
    print("You got "+str((1 - counter/4)*100)+"% correct")
    atbilde.append((1 - counter/4)*100)
    df.loc[len(df)] = atbilde
    df.to_excel("VerbBender.xlsx", index = False)


VerbBender()