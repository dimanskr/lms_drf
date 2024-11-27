# Домашняя работа DFR

## Установка и запуск

1. Установите зависимости из файла `pyproject.toml`, используя Poetry:
    ``` bash
    poetry install
    ```
2. Создайте базу данных postgresql, пропишите настройки подключения к ней
в файле .env в корне проекта ([шаблон файла](.env.sample))


3. Если вы создавали базу данных ранее, то очистите ее:
   ``` bash
    python manage.py flush
   ```
4. Примените миграции
   ``` bash
    python manage.py migrate
   ```

5. Создайте учетную запись администратора кастомной командой:
   ``` bash
   python manage.py csu
   ```
   *email: admin@mail.ru* \
   *пароль: 11111111*


6. Заполните данные из фикстур (группы, пользователи, материалы, платежи), используя данные фикстур:
   ``` bash
   python manage.py loaddata users/fixtures/groups.json
   python manage.py loaddata users/fixtures/users.json
   python manage.py loaddata materials/fixtures/materials.json
   python manage.py loaddata users/fixtures/payments.json
   ```
   *для всех пользователей пароль: 11111111* \
   *пользователь с email user3@mail.ru - модератор*


7. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
      
## "Эндпоинты курсов и уроков"
| path                             | methods                |
|----------------------------------|------------------------|
| `/courses/`                      | `GET`, `POST`          |
| `/courses/<id>/`                 | `GET`, `PUT`, `DELETE` |
| `/lessons/`                      | `GET`                  |
| `/lessons/<id>`                  | `GET`                  |
| `/lessons/create/`               | `POST`                 |
| `/lessons/<id>/update/`          | `PUT`                  |
| `/lessons/<id>/delete/`          | `DELETE`               |
| `/subscribe-course/<course_id>/` | `POST`                 |

## "Эндпоинты пользователей и платежей"
| path                               | methods  |
|------------------------------------|----------|
| `/users/register/`                 | `POST`   |
| `/users/`                          | `GET`    |
| `/users/<id>`                      | `GET`    |
| `/update/<id>`                     | `PUT`    |
| `/delete/<id>/`                    | `DELETE` |
| `/users/payments/`                 | `GET`    |
| `/users/payments/create/`          | `POST`   |
| `/users/payments/?search=transfer` | `GET`    |
| `/users/login/`                    | `POST`   |
| `/users/token/refresh/`            | `POST`   |

На эндпоинте `/users/login/` получаем токен `access` который нужно использовать для доступа к другим эндпоинтам.

### Документирование и безопасность:
- Подключен и настроен вывод документации для API проекта на эндпоинтах /swagger/ и /redoc/


