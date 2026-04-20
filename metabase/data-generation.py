# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import random

# # Настройки
# num_rows = 1000  # Сделаем побольше для красоты в Metabase
# start_date = datetime(2024, 1, 1)

# # Словарь категорий с примерными диапазонами цен
# categories_config = {
#     'Фастфуд': (-150, -1200),
#     'Культура': (-500, -6000),
#     'Супермаркеты': (-300, -5000),
#     'Транспорт и Такси': (-100, -1500),
#     'Подписки': (-199, -899),
#     'Гаджеты и техника': (-5000, -80000),
#     'Здоровье и аптеки': (-200, -10000),
#     'Бары и алкоголь': (-1000, -15000),
#     'Случайная фигня в 3 часа ночи': (-500, -3000),
# }

# income_sources = ['Зарплата', 'Перевод от мамы', 'Продажа хлама на Авито', 'Кэшбэк']

# data = []

# for i in range(num_rows):
#     # Дата
#     dt = start_date + timedelta(days=random.randint(0, 364), seconds=random.randint(0, 86400))
    
#     # Решаем: это трата или приход? (80% траты, 20% приходы)
#     if random.random() > 0.2:
#         category = random.choice(list(categories_config.keys()))
#         min_p, max_p = categories_config[category]
#         amount = round(random.uniform(min_p, max_p), 2)
#         trans_type = 'Списание'
#         desc = f"Оплата: {category}"
#     else:
#         category = 'Доход'
#         amount = round(random.uniform(5000, 70000), 2)
#         trans_type = 'Пополнение'
#         desc = random.choice(income_sources)

#     data.append([
#         dt.strftime('%d.%m.%Y'), 
#         dt.strftime('%H:%M'), 
#         category, 
#         trans_type, 
#         amount, 
#         desc
#     ])

# # Сортируем по дате, чтобы в Metabase графики не сошли с ума
# df = pd.DataFrame(data, columns=['Дата', 'Время', 'Категория', 'Тип', 'Сумма', 'Описание'])
# df['dt_obj'] = pd.to_datetime(df['Дата'] + ' ' + df['Время'], dayfirst=True)
# df = df.sort_values('dt_obj').drop(columns=['dt_obj'])

# # Сохраняем
# df.to_csv('spicy_transactions_2024.csv', index=False, encoding='utf-8-sig')

# print(f"Готово! Сгенерировано {num_rows} транзакций. Теперь в твоем Metabase будет на что посмотреть.")


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Settings
num_rows = 1000 
start_date = datetime(2024, 1, 1)

# Categories with typical price ranges (Negative for spending)
categories_config = {
    'Fast Food': (-5, -25),
    'Culture & Events': (-15, -150),
    'Supermarkets': (-10, -200),
    'Transport & Taxi': (-3, -40),
    'Digital Subscriptions': (-5, -20),
    'Gadgets & Tech': (-100, -1500),
    'Health & Pharmacy': (-10, -300),
    'Bars & Nightlife': (-20, -400),
    'Late Night Regrets': (-15, -100),
    'Travel & Hotels': (-150, -2000)
}

income_sources = ['Monthly Salary', 'Transfer from Mom', 'eBay Sale', 'Cashback Bonus']

data = []

for i in range(num_rows):
    # Generate random date/time within the year
    dt = start_date + timedelta(days=random.randint(0, 364), seconds=random.randint(0, 86400))
    
    # Decide: Expense or Income? (80% / 20%)
    if random.random() > 0.2:
        category = random.choice(list(categories_config.keys()))
        min_p, max_p = categories_config[category]
        amount = round(random.uniform(min_p, max_p), 2)
        trans_type = 'Debit'
        description = f"Payment to: {category}"
    else:
        category = 'Income'
        amount = round(random.uniform(500, 5000), 2)
        trans_type = 'Credit'
        description = random.choice(income_sources)

    data.append([
        dt.strftime('%Y-%m-%d'), 
        dt.strftime('%H:%M:%S'), 
        category, 
        trans_type, 
        amount, 
        description
    ])

# Create DataFrame and sort
df = pd.DataFrame(data, columns=['Date', 'Time', 'Category', 'Type', 'Amount', 'Description'])
df['dt_obj'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.sort_values('dt_obj').drop(columns=['dt_obj'])

# Save to CSV
df.to_csv('financial_data_2024.csv', index=False, encoding='utf-8')

print("Done! 'financial_data_2024.csv' is ready for Metabase.")