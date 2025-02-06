# QRkot_spreadseets

## Описание проекта
QR Kot - приложение для Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

**Проекты**

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

**Пожертвования**

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

**Пользователи**

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

## Заполнение .env файла

Пример заполнения **.env** файла находится в файле **.env.example**


## Запуск проекта
1. Клонировать репозиторий и перейти в каталог проекта:
```
git clone https://github.com/soulyraziel/cat_charity_fund
cd cat_charity_fund
```

2. Создать и активировать виртуальное окружение:
```
py -3.9 -m venv venv

source ./venv/bin/activate
```

3. Обновить pip и установить зависимости из ```requirements.txt```
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Создать и заполнить файл **.env** по аналогии с **.env.example**:

```
touch .env
```

5. Выполнить миграции:
```
alembic upgrade head
```

6. Запустить проект:
```
uvicorn app.main:app
```

После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API с примерами запросов досупна по адресам:
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc


**Автор проекта:** Андрей Владимиров