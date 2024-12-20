# Домашняя работа DFR

## Установка и запуск осуществляются с помощью Docker

Команда для создания билда и первого запуска:
   ``` bash
    docker-compose up -d --build
   ```
Команда для запуска::
   ``` bash
    docker-compose up
   ```
Команда для остановки работы программы:
   ``` bash
    docker-compose down
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
| `/users/payments/detail/<pk>/`     | `GET`    |
| `/users/payments/?search=transfer` | `GET`    |
| `/users/login/`                    | `POST`   |
| `/users/token/refresh/`            | `POST`   |

На эндпоинте `/users/login/` получаем токен `access` который нужно использовать для доступа к другим эндпоинтам.

### Docker Compose:
- Оформлен файл Dockerfile.
- Оформлен файл docker-compose.yaml с описанием сервисов 
PostgreSQL, Redis, Celery.
- Зависимости для удобства работы перенес в requirements.txt.

