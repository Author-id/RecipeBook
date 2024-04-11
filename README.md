# Проект Recipe Book

![Статус пайплайна](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-2/badges/main/pipeline.svg)

## Требования к системе

* Python 3.11

## ER-диаграмма

![ER-диаграмма](/ER.jpg)
<!--
https://www.quickdatabasediagrams.com/
-->

## Установка
```console
git clone https://gitlab.crja72.ru/django/2024/spring/course/projects/team-2.git
```

## Запуск проекта

1. Создайте и активируйте виртуальное окружение

   для Mac/Linux:

   ```console
   python3 -m venv venv
   source venv/bin/activate
   ```

   для Windows:

   ```console
   python -m venv venv
   venv\Scripts\activate.bat
   ```

2. Установите зависимости

   для Mac/Linux:

   ```console
   pip3 install -r requirements/<режим>.txt
   ```

   для Windows:

   ```console
   pip install -r requirements\<режим>.txt
   ```

   Где режим:
   * prod
   * test
   * dev

3. Настройте переменные окружения
   1. Создайте .env

      для Mac/Linux:

      ```console
      cp <шаблон> .env
      ```

      для Windows:

      ```console
      copy <шаблон> .env
      ```

      Где шаблон:
      * .env.template
      * .env.test.template
      * .env.dev.template

   В prod-режиме:

   2. Замените DJANGO_SECRET_KEY на настоящий
   3. Добавьте DJANGO_ALLOWED_HOSTS, разделяя значения запятой
   4. Установите DJANGO_MAIL

4. Скомпилируйте фалы локализации

   ```console
   django-admin compilemessages
   ```

5. Проведите миграции

   для Mac/Linux:

   ```console
   python3 recipebook/manage.py migrate
   ```

   для Windows:

   ```console
   python recipebook\manage.py migrate
   ```

6. Перейдите в каталог проекта

   ```console
   cd recipebook
   ```

7. Соберите статику

   для Mac/Linux:

   ```console
   python3 manage.py collectstatic
   ```

   для Windows:

   ```console
   python manage.py collectstatic
   ```

8. Запустите сервер

   для Mac/Linux:

   ```console
   python3 manage.py runserver
   ```

   для Windows:

   ```console
   python manage.py runserver
   ```

9. Создайте супер-пользователя (не обязательно)

   для Mac/Linux:

   ```console
   python3 manage.py createsuperuser
   ```

   для Windows:

   ```console
   python manage.py createsuperuser
   ```

## Тестирование

1. Выполните пункты 1-6 раздела "Запуск проекта"
2. Запустите тесты

   для Mac/Linux:

   ```console
   python3 manage.py test
   ```

   для Windows:

   ```console
   python manage.py test
   ```


## Использование фикстур

### Загрузка

```console
cd recipebook
python3 manage.py loaddata fixtures/data.json
cp -r fixtures/media media
```

для Windows:

```console
cd recipebook
python manage.py loaddata fixtures\data.json
xcopy fixtures\media media /s /Y /i
```

### Создание

```console
cd recipebook
mkdir fixtures
python3 -Xutf8 manage.py dumpdata [...<app>] -o fixtures/data.json --indent 4
rmdir -r fixtures/media
rsync -a --exclude={'cache/'} media fixtures/media
```

для Windows:

```console
cd recipebook
mkdir fixtures
python -Xutf8 manage.py dumpdata [...<app>] -o fixtures\data.json --indent 4
rmdir fixtures\media /s /q
echo cache\ > exc.txt
xcopy media fixtures\media /s /Y /i /exclude:exc.txt
del exc.txt
```


## Локализация

На Windows необходимо установить
[gettext](https://mlocati.github.io/articles/gettext-iconv-windows.html)

### Создание файлов локализации

```console
django-admin makemessages -l ru -l en
```

### Компиляция файлов локализации

```console
django-admin compilemessages
```
