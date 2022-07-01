# Уведомление о проверке работ на Девмане
 
Телеграм-бот, отправляющий уведомления при проверке работы преподавателем на курсе [dvmn.org](https://dvmn.org/).

### Установка
1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей, используйте команду pip (или pip3, если есть конфликт с Python2) :
```
pip install -r requirements.txt
```
3. Необходимо [зарегистрировать бота и получить его API-токен](https://telegram.me/BotFather)
4. В директории скрипта создайте файл `.env` и укажите в нём следующие данные:
```
DVMN_TOKEN=`devman_token`
TG_BOT_TOKEN=`telegram_token`
TG_CHAT_ID=`telegram_chat_id`
```
Где:
- `devman_token` - токен для работы с [API Девмана](https://dvmn.org/api/docs/)
- `telegram_token` - токен для Telegram-бота, полученный от Bot Father
- `telegram_chat_id` - идентификатор пользователя в Telegram, можно узнать у бота [@userinfobot](https://t.me/userinfobot)


### Запуск
```
$ python main.py
```
