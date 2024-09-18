import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import random
import csv
import json  # Для работы с JSON
import time
from openpyxl import Workbook  # pip install openpyxl

# Список пользовательских агентов
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/112.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'
]


# Функция для получения случайного пользовательского агента
def get_random_user_agent():
    return random.choice(user_agents)


# Устанавливаем переменные для JSON и XLSX
data_list = []  # Для хранения данных для JSON
wb = Workbook()  # Создаем новую книгу для XLSX
ws = wb.active  # Получаем активный лист
ws.append(['Category', 'Name', 'Address', 'Contacts', 'LINK'])  # Заголовки для XLSX

count = 1
while count <= 275:
    url = f'https://perevozka24.ru/vip/gruzoperevozki?stop={count}'
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    category = block.find('h1', {'class': 'h3'}).text.strip()
    print(category)
    heads = block.find('div', class_='rating-wrapper mt20').find_all('div', class_='c-company-card')
    print(len(heads))

    for head in heads:
        link = head.find('h3', class_='cc-title').find('a')['href']
        print('https://perevozka24.ru' + link)
        get_url = ('https://perevozka24.ru' + link)
        try:
            less = requests.get(get_url, headers=headers).text
            sock = BeautifulSoup(less, 'lxml')
            name = sock.find('h1').text.strip()
            address = sock.find('div', {'class': 'contacts'}).find('p').text.strip()
            print(name)
            print(address)
            contacts = sock.find('div', {'class': 'contacts'}).find_all('span')
            all_cont = []
            for contact in contacts:
                print(contact.text.strip())
                all_cont.append(contact.text.strip())
            time.sleep(2)
            print('\n')
        except Exception as e:
            print(f"Error: {e}")
            continue

        # Формируем запись для JSON и XLSX
        storage = {
            'category': category,
            'name': name,
            'address': address,
            'contacts': '; '.join(all_cont),
            'url': get_url
        }
        data_list.append(storage)  # Добавляем данные в список для JSON
        ws.append([storage['category'], storage['name'], storage['address'], storage['contacts'],
                   storage['url']])  # Добавляем данные в XLSX

    count += 1
    print('page: ' + str(count))

    # Запись данных в JSON файл
    with open(f'{category}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    # Сохраняем XLSX файл
    wb.save(f'{category}.xlsx')

    print(f"Данные сохранены в {category}.json и {category}.xlsx")
