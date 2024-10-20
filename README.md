# real_time_chat



## Описание проекта

Данный проект представляет собой простое приложение для чата в реальном времени, разработанное на Python с использованием FastAPI и Socket.IO. Проект включает в себя следующие функциональности:

- Подключение пользователей к чату и отправка сообщений.
- Отображение всех сообщений в реальном времени для всех подключенных пользователей.
- Простая аутентификация пользователей с использованием токенов.
- Хранение истории сообщений в базе данных PostgreSQL.
- Поддержка комнат чата, где пользователи могут выбирать комнату для общения.
- Реализация приватных сообщений между пользователями.
- Уведомления о новых сообщениях.


## Установка и запуск

### Запуск через Docker compose (еще в разработке)

### Предварительные требования

- Docker
- Docker Compose

### Инструкция по запуску

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/yourusername/chat_app.git
   cd chat_app

2. **Заполните файл .env**

3. **Соберите образ и примените миграции к базе данных**

    ```Docker
    docker-compose up --build && docker-compose exec web poetry run alembic upgrade head


### Запуск через make 

    
    make develop
    source ~/.venv/bin/activate (activate.fish) в зависимости от вашего терминала
    make run
    

## Дальнейшие правки 

- Переписать миграции и перенеси их в слой infrastucture
- Разделить проект на слой domains, presentors, infrastucture
- Переписать  FrontEnd часть
- Добавить счетчик метрик (Prometheus)
- Добавить лог-сервис