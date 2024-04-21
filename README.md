* Клонируем проект из github с помощью GUI вашего IDE либо с помощью команды git clone
* Устанавливаем Docker если у вас его нет [сайта Docker'a](https://docs.docker.com/)
* Переходим в папку c файлом Docker и docker-compose.yml
* запускаем команду docker compose build
* запускаем команду docker compose up
* В браузере переходим по адресу http://localhost:7777/api/docs/
* Логин и пароль для админ панели (http://localhost:7777/admin) 
  * login - admin
  * password - 1234

## Задача: 
### Написать sql запрос*, который выводит 10 пользователей, у которых максимальное количество сохраненных ссылок, если количество ссылок одинаково у нескольких пользователей, выведете тех, кто раньше был зарегистрирован.

## Ответ:
```
select auth_user.id, email, date_joined, count(email) as link_count from auth_user
join links_link on auth_user.id = links_link.owners_id
group by email
order by link_count desc, date_joined
limit 10
```
