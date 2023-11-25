from telethon.errors import MsgIdInvalidError, ChannelPrivateError
from telethon.sync import TelegramClient
from urllib.parse import urlparse
from telethon.tl import types
import os

# ВАЖНО ДЛЯ ЗАПОЛНЕНИЯ!!!
api_id = 0
api_hash = 'your_api_hash'
system_version = "Android 10.0"
device_model = "Pixel 3 XL"
##########################

logo = """
▀█▀ █▀▀ ▄▄ █▀█ ▄▀█ █▀█ █▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
░█░ █▄█ ░░ █▀▀ █▀█ █▀▄ ▄█
"""

# -Функция для чистки консоли
def cls_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

# -Определение принтов
def gd_print(value):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    result = f"\n>{green_color} {value} {reset_color}\n"
    print(result)

def bd_print(value):
    red_color = '\033[31m'
    reset_color = '\033[0m'
    result = f"\n>{red_color} {value} {reset_color}\n"
    print(result)

# -Функция для получения комментариев и записи их в файл
async def get_comments(client: TelegramClient, channel: str, message_id: int):
    user_ids = set()
    try:
        async for message in client.iter_messages(channel, reply_to=message_id):
            if isinstance(message, types.Message):
                if message.from_id:
                    user_id = message.from_id
                    if isinstance(user_id, types.PeerUser):
                        user_ids.add(str(user_id.user_id))
                        print(f"> записали юзера: {user_id.user_id}")
    except MsgIdInvalidError:
        bd_print("Ссылка на пост неверная. Проверьте её и запустите скрипт заново.")
        exit()
    except Exception as e:
        bd_print(f"Произошла ошибка при получении комментариев: {e}")

    save_to_file(user_ids)

# -Функция для получения участников чата и записи их в файл
async def save_chat_members(client: TelegramClient, chat_entity: str):
    try:
        participants = await client.get_participants(chat_entity)
        user_ids = {str(participant.id) for participant in participants}
        for user_id in user_ids:
            print(f"> Записали юзера: {user_id}")
        save_to_file(user_ids)
    except Exception as e:
        bd_print(f"Произошла ошибка при получении участников чата: {e}")

# -Функция для получения отправителей сообщений в чате и записи их в файл
async def get_chat_message_senders_from_history(client: TelegramClient, chat_entity: str, limit: int = 100):
    try:
        messages = []
        async for message in client.iter_messages(chat_entity, limit=limit):
            messages.append(message)

        user_ids = {str(message.sender_id) for message in messages if message.sender_id is not None and message.sender_id > 0}
        for user_id in user_ids:
            print(f"> Записали юзера: {user_id}")
        save_to_file(user_ids)
    except Exception as e:
        bd_print(f"Произошла ошибка при получении отправителей сообщений в чате: {e}")

# -Функция для получения участников канала и записи их в файл
async def save_channel_members(client: TelegramClient, channel_username: str):
    try:
        channel = await client.get_entity(channel_username)
        participants = await client.get_participants(channel)
        user_ids = {str(participant.id) for participant in participants}
        for user_id in user_ids:
            print(f"> Записали юзера: {user_id}")
        save_to_file(user_ids)
    except ChannelPrivateError as private_error:
        bd_print(f"Ошибка с доступом к каналу: {private_error}")
        exit()
    except Exception as e:
        bd_print(f"Произошла ошибка при получении участников канала: {e}")


# -Запись полученных юзеров в файл
def save_to_file(user_ids: set):
    with open('user_ids.txt', 'w') as file:
        file.write('\n'.join(user_ids))
        gd_print(f"Список юзеров успешно записан в файл 'user_ids.txt'. Всего уникальных юзеров: {len(user_ids)}")

# -Получение ссылки на пост
def get_url():
    while True:
        try:
            url = input("Ссылка на пост канала с открытыми комментами: ")
            parsed_url = urlparse(url)
            channel_name = parsed_url.path.split('/')[1]
            message_id = parsed_url.path.split('/')[2]
            return channel_name, message_id
        except IndexError:
            bd_print("Ссылка на пост неверная. Проверьте её и введите заново.")

# -Выбор действия
def select_action():
    while True:
        action = input("\nВыберите действие:\n1. Спарсить участников чата\n2. Спарсить юзеров, отправлявших сообщения в чате\n3. Спарсить участников канала\n4. Спарсить комментарии\n\n")
        if action == '1':
            return 'chat'
        elif action == '2':
            return 'message'
        elif action == '3':
            return 'channel'
        elif action == '4':
            return 'postcomment'
        else:
            cls_cmd()
            print(logo)
            bd_print("Неверный выбор. Попробуйте ещё раз.")

# -Проверка на наличие данных для авторизации и их верность
if api_id == 0 or api_hash == 'your_api_hash':
    cls_cmd()
    while True:
        api_id = input("\nВведите ваш API ID: ")
        while not api_id.isdigit():
            bd_print("Неверно. Пожалуйста, проверьте данные и попробуйте ввести api_id снова.")
            api_id = input("Введите ваш API ID: ")
        api_hash = input("\nВведите ваш API hash: ")
        while len(api_hash) != 32:
            bd_print("Неверно. Пожалуйста, проверьте данные и попробуйте ввести api_hash снова.")
            api_hash = input("Введите ваш API hash: ")
        break

# -Запуск скрипта
if __name__ == '__main__':
    cls_cmd()
    print(logo)
    select_action = select_action()
    if select_action == 'chat':
        cls_cmd()
        print(logo)
        chat_username = input("\n@username чата: ")
        print()
        with TelegramClient('SESSION_FOR_TELEGRAM_PARSER', api_id, api_hash, device_model=device_model, system_version=system_version) as client:
            client.loop.run_until_complete(save_chat_members(client, chat_username))
    elif select_action == 'message':
        cls_cmd()
        print(logo)
        chat_username = input("\n@username чата: ")
        count = input("\nМаксимальное количество сообщений для парсинга: ")
        print()
        with TelegramClient('SESSION_FOR_TELEGRAM_PARSER', api_id, api_hash, device_model=device_model, system_version=system_version) as client:
            client.loop.run_until_complete(get_chat_message_senders_from_history(client, chat_username, int(count)))
    elif select_action == 'channel':
        cls_cmd()
        print(logo)
        channel_username = input("\n@username канала: ")
        print()
        with TelegramClient('SESSION_FOR_TELEGRAM_PARSER', api_id, api_hash, device_model=device_model, system_version=system_version) as client:
            client.loop.run_until_complete(save_channel_members(client, channel_username))
    elif select_action == 'postcomment':
        cls_cmd()
        print(logo)
        channel_name, message_id = get_url()
        print()
        with TelegramClient('SESSION_FOR_TELEGRAM_PARSER', api_id, api_hash, device_model=device_model, system_version=system_version) as client:
            client.loop.run_until_complete(get_comments(client, channel_name, int(message_id)))
    else:
        bd_print("bb.")