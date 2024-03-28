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
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import math
m = 32
n = 50
p = 0.55
q = 1 - p
E = 0.09
result = 0
C1 = math.comb(5,2)
C2 = math.comb(25,0)
C3 = math.comb(30,2)
print(C1*C2/C3)


# chislitel = math.factorial(n)
# znamenatel = math.factorial(m) * math.factorial(n-m)
# C = chislitel/znamenatel
# if n <= 15:
#     result = C * (p**m) * (q**(n-m))
# else:
#     alpha = n*p
#     if alpha <= 15:
#         result = ((math.e**(-alpha)) * (alpha**m))/math.factorial(m)
#     else:
#         x = (m - n*p) / ((n*p*q)**0.5)
#         Fx = 0.1781
#         result = Fx / ((n*p*q)**0.5)
#         print(x)
#     print(alpha)


