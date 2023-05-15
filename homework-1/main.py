"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2


def connection():
    path = ["north_data/employees_data.csv", "north_data/customers_data.csv", "north_data/orders_data.csv"]
    fields = [["first_name", "last_name", "title", "birth_date", "notes"],
              ["customer_id", "company_name", "contact_name"],
              ["order_id", "customer_id", "employee_id", "order_date", "ship_city"]]
    query = ["INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", "INSERT INTO customers VALUES (%s, %s, %s)",
             "INSERT INTO orders VALUES (%s, %s, %s, %s, %s)"]

    conn = psycopg2.connect(host='localhost', database='north', user='postgres', password="123321")
    try:
        with conn.cursor() as cur:
            for i in range(len(path)):
                data = load_data(path[i], fields[i])

                count = 1

                for row in data:

                    p = list(row[name] for name in fields[i])
                    if i == 0:
                        p.insert(0, count)

                    cur.execute(query[i], p)
                    count += 1

                conn.commit()
    finally:
        conn.close()


def load_data(path, fields):
    # print(path)
    data = []
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dictionary = {}

            for field in fields:
                dictionary[field] = row[field]
            data.append(dictionary)

        return data


if __name__ == '__main__':
    connection()
