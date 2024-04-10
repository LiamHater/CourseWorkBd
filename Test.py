# # settings.py
# import os
# from dotenv import load_dotenv, find_dotenv, dotenv_values
# import mysql.connector
#
# config = dotenv_values(".env")
#
# try:
#     # Создаем подключение
#     connection = mysql.connector.connect(**config)
#     # Создаем объект "курсора" для выполнения SQL-запросов
#     cursor = connection.cursor()
#     # Пример SQL-запроса
#     try:
#         image_path = r"C:\Users\User\Pictures\ляпота.jpeg"
#         with open(r"C:\Users\User\Pictures\Camera Roll\ляпота.jpeg", "rb") as img:
#             image = img.read()
#         query = f"SELECT Примечания FROM здание;"
#         print(query)
#         cursor.execute(query)
#         print(cursor.fetchall())
#     except mysql.connector.Error as error:
#         print("Failed to insert record into table:", error)
#     # Закрываем курсор и подключение
#     cursor.close()
#     connection.close()
# except Exception as ex:
#     print("Ошибка подключения, причина:")
#     print(ex)
#
#
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(".env")

db_user = os.getenv("user")
db_password = os.getenv("password")
db_hostname = os.getenv("host")
db_name = os.getenv("database")

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_hostname}/{db_name}')

metadata = MetaData()
metadata.reflect(bind=engine)


# Загружаем метаданные таблицы по ее имени
table_name = 'помещение'  # Замените на имя нужной таблицы
table = Table(table_name, metadata, autoload=True, autoload_with=engine)

# Получаем информацию о внешних ключах таблицы
foreign_keys = table.foreign_keys

# Проходимся по внешним ключам
for fk in foreign_keys:
    # Получаем имя таблицы, на которую ссылается внешний ключ
    parent_table_name = fk.column.table.name

    # Получаем имя столбца, на который ссылается внешний ключ
    parent_column_name = fk.column.name

    # Выводим информацию о внешнем ключе
    print(f"Foreign key in {table_name} references {parent_table_name}.{parent_column_name}")

    # Получаем данные из таблицы, на которую ссылается внешний ключ
    parent_table = Table(parent_table_name, metadata, autoload=True, autoload_with=engine)
    conn = engine.connect()
    stmt = select(parent_table.c[parent_column_name])
    result = conn.execute(stmt)

    # Печатаем результаты
    for row in result:
        print(row[0])

