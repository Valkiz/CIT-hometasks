import csv
import numpy as np
import math
from collections import defaultdict

import requests

OUR_USER = 13

def getTopFive(sim:list):
    top5 = []  # Индексы похожих юзеров
    simGrades = list(sim)
    simGrades.sort(reverse=True)
    taken = 0
    for a in simGrades:
        whichUser = sim.index(a)
        while whichUser in top5:
            whichUser = sim.index(a, whichUser + 1)
        top5.append(whichUser)
        taken += 1
        if taken == 5: break
    return top5

with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    raw_data = [raw_data[1:] for raw_data in reader][1:]
    data = np.asarray(raw_data, float) #Прочли в матрицу
    '''
    for a in data:
        print(','.join(a))
    '''
sim = [0]*40
average = [0] * 40
#Рассматриваем нашего пользователя (14)
u = 0
for user in data:
    count = 0
    for myVal in user:
        if int(myVal) != -1:
            count+=1
            average[u]+=int(myVal)
    average[u]/=count
    if u == OUR_USER:
        u+=1
        continue #Скипнули расчет схожести для нашего пользователя
    A = 0
    B, C = 0,0
    film = 0
    for myVal in data[OUR_USER]:
        if int(myVal) != -1 and int(user[film]) != -1:  # Нашли оцененный обоими пользователями фильм
            A+=int(myVal)*int(user[film])
            B+=int(myVal)**2
            C+= int(user[film]) ** 2
        film += 1
    sim[u]=(A/math.sqrt(B))/math.sqrt(C)

    u += 1


sim = [round(a,4) for a in sim]
average = [round(a, 4) for a in average]

# Берем топ5
top5 = getTopFive(sim)

# top5 = [32,14,37,33,36]
#print("influenced by " + str([a + 1 for a in top5]))
#print([sim[a] for a in top5])

film = 0
firstTask = {}
for val in data[OUR_USER]:
    if int(val) == -1: #Нашли в строке неоцененный фильм
        data[OUR_USER][film] = 0 #Не забыли сбросить перед дальнейшими вычислениями
        simBoth = 0
        for simUser in top5:
            if int(data[simUser][film]) != -1:
                simBoth += abs(sim[simUser])
                data[OUR_USER][film]+= sim[simUser] * (data[simUser][film] - average[simUser])
        data[OUR_USER][film] /= simBoth
        data[OUR_USER][film] += average[OUR_USER]

        firstTask["movie " + str(film+1)] = round(data[OUR_USER][film],2)
        print('"movie ' + str(film+1)+'": ' +str(round(data[OUR_USER][film],2)))
    film+=1

print(firstTask)
reg_a = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
jsargs = {
    "user":14,
    "1": firstTask
}
head = {'content-type': 'application/json'}
print()
#r = requests.post(reg_a, json=jsargs,headers=head)
#print(r.json())