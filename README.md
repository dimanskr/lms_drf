# Домашняя работа DFR

## "Эндпоинты курсов и уроков"
| path                                     | methods                |
|------------------------------------------|------------------------|
| `/courses/`                              | `GET`, `POST`          |
| `/courses/<id>/`                         | `GET`, `PUT`, `DELETE` |
| `/lessons/`                              | `GET`                  |
| `/lessons/<id>`                          | `GET`                  |
| `/lessons/create/`                       | `POST`                 |
| `/lessons/<id>/update/`                  | `PUT`                  |
| `/lessons/<id>/delete/`                  | `DELETE`               |

## "Эндпоинты пользователей и платежей"
| path                                     | methods                |
|------------------------------------------|------------------------|
| `/users/register`                        | `POST`                 |
| `/users/`                                | `GET`                  |
| `/users/<id>`                            | `GET`                  |
| `/update/<id>`                           | `PUT`                  |
| `/delete/<id>/`                          | `DELETE`               |
| `/users/payments/`                       | `GET`                  |
| `/users/payments/create/`                | `POST`                 |
| `/users/payments/?search=transfer`       | `GET`                  |
| `/users/payments/?ordering=payment_date` | `GET`                  |


### Загрузить данные о пользователях и платежах можно из фикстур:
   ``` bash
   python manage.py loaddata users/fixtures/payments.json
   ```

