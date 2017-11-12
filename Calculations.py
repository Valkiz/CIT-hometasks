import csv
import numpy as np
import math
from collections import defaultdict

import requests

OUR_USER = 13


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
simGrades = list(sim)
simGrades.sort(reverse=True)


def indices(searchIn:list, searchWhat:list) :
    for i in searchWhat :
        res = searchIn.index(i)
        searchIn.remove(i)
        yield res

sim = [round(a,4) for a in sim]
simGrades = [round(a, 4) for a in simGrades]

film = 0
for val in data[OUR_USER]:
    if int(val) == -1: #Нашли в строке неоцененный фильм
        simBoth = 0
        #print(sim)
        #Берем топ5, оценивших тот же самый фильм
        top5 = []  # Индексы похожих юзеров
        taken=0
        for a in simGrades:
            whichUser = sim.index(a)
            while whichUser in top5:
                whichUser = sim.index(a,whichUser+1)
            if data[whichUser][film] != -1:
                top5.append(whichUser)
                taken+=1
            if taken == 5: break
        print([sim[a] for a in top5])
        print ("influenced by "+str([a+1 for a in top5]))
        for simUser in top5:
            print(data[simUser][film])
            data[OUR_USER][film]+= sim[simUser] * (data[simUser][film] - average[simUser])
            simBoth+=abs(average[simUser])
        data[OUR_USER][film] /= simBoth
        data[OUR_USER][film] += average[OUR_USER]
        print('"movie ' + str(film+1)+'": ' +str(round(data[OUR_USER][film],2)))
    film+=1
for a in data[OUR_USER]:
    print(round(a,2), end=' ')

reg_a = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
jsargs = {
    "user":14,
    "1": {
"movie 4": 2.97,
"movie 8": 2.78,
"movie 9": 2.85,
"movie 16": 2.96,
"movie 26": 3.12
    }
}
head = {'content-type': 'application/json'}
print()
#r = requests.post(reg_a, json=jsargs,headers=head)
#print(r.json())
