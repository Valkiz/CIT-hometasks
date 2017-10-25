import requests

reg_a = 'https://cit-home1.herokuapp.com/api/register'
check_a = 'https://cit-home1.herokuapp.com/api/check_me'
jsargs = {'first name': 'Valery', 'last name': 'Kizko', 'Hello': 'World'}
head = {'content-type': 'application/json'}

#Зарегистрировались
r = requests.get(reg_a, json=jsargs,headers=head)
print(r.json())
#Проверили
check=requests.get(check_a)
print(check.json())