# Проект "Самозанятый"

## Стек проекта
Python, DRF (Django REST framework), JS, React, PostgreSQL, Nginx, Celery, Redis, Docker

## Описание
Проект "Самозанятый" представляет собой комплексное веб-приложение, охватывающее различные аспекты работы с клиентами, документами и почтовыми сервисами. Ниже приведены основные задачи, которые необходимо выполнить для завершения проекта.

## UserApp
- ++Разобраться с принципами работы API стороннего почтового сервиса (опционально обсудить иные варианты почтовых сервисов).
- ++Добавить эндпоинт "resend_activation"(подумать над подходящим названием), позволяющий пользователям изменить email и отправить письмо с ссылкой-активатором.
- ++Изменить тип идентификации пользователя с id на токен в recover_password_confirm.
- ++Добавить action для получения письма восстановления пароля.
- ++Подумать над возможностью разделения функционала recover_password.
- (Опционально) Добавить фильтрацию для реквизитов пользователя.
- (Опционально) Улучшить вывод в actions Представления пользователя. Сейчас там бардак с кодами и форматом ответа сервера, что не очень хорошо.

## CustomerApp
- ++Добавить новое поле passport для заказчиков с типом "Физическое лицо".
- ++Разделить функционал Реквизитов и Контактов в отдельные ViewSets.
- Добавить дополнительные actions во все viewsets для выбора и фильтрации записей таблицы.
- (Опционально) Добавить фильтрацию для всех viewsets заказчиков.

## DocumentApp
- Оптимизировать работу Agreement и Additional QuerySet aggregation на работу с менеджером модели.
- ++ Удалить все упоминания сделок как обособленных сущностей и добавить дополнительное поле deal_amount для договоров и дополнений.
- Переработать эндпоинт статистики для возможности выбора временного промежутка.
- Изменить list action для платежей, добавив поля payment_amount и payment_status.
- Добавить фильтрацию для всех операций.

## Общие задачи по проекту
- Добавить тестирование.
- Во всех приложениях обработать значения, возвращаемые представлениями.
- Настроить красивую админку.
- Оптимизировать работу базы данных, улучшив неоптимальные запросы.
- Вынести работу почтовых сервисов в докеризируемый celery + redis.
- Настроить конфиг Nginx или альтернативного веб-сервера.
- Задеплоить приложение.
- Отпразновать успешное завершение проекта!

Каждая из перечисленных задач будет выполнена с учетом лучших практик разработки и будет способствовать улучшению функционала проекта "Самозанятый".