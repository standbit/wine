# Новое русское вино

Сайт магазина авторского вина "Новое русское вино"

## Установка
Python3 должен быть установлен
1. Склонируйте репозиторий к себе на компьютер

2. Дальше работайте в консоли. Cоздайте папку виртуального окружения
```python
$ virtualenv venv
```
3. Активируйте виртуальное окружение для изоляции проекта
```python
$ source venv/bin/activate
```
4. Установите зависимости, используя `pip`
```python
$ python3 -m pip install -r requirements.txt
```
5. Скопируйте образец *"example_wine_database.xlsx"* и заполните своими данными, ниже пример таблицы

  |   Категория   |     Название  |     Сорт       |   Цена      |    Картинка    |         Акция        |
  | ------------- |:-------------:|:--------------:|:-----------:|:--------------:|:--------------------:|
  | Белые вина    | Белая леди    | Дамский пальчик|    500      | belaya_ledi.png|                      |
  | Красные вина  | Хванчкара     | Александраули  |    550      | hvanchkara.png |                      |
  | Напитки       | Чача          |                |    400      | chacha.png     | Выгодное предложение!|


## Запуск скрипта
1. Запустите скрипт:
```python
$ python3 main.py --path "PATH to excel-file" (по умолчанию "./example_wine_database.xlsx")
```
2. Перейдите на сайт по адресу [localhost](http://127.0.0.1:8000)

   Наслаждайтесь выбором вин!

* Остановить выполнение программы в консоли: `Ctrl+C`

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](http://dvmn.org)
