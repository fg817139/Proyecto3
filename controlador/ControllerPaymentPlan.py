import sys
import psycopg2
import SecretConfig
from datetime import date
from Modelos.CreditCard import CreditCard
from Modelos.PaymentPlan import PaymentPlan


def get_cursor():
    """
    Create the connection to the database and return a cursor to execute instructions
    """
    DATABASE = SecretConfig.DATABASE
    USER = SecretConfig.USER
    PASSWORD = SecretConfig.PASSWORD
    HOST = SecretConfig.HOST
    PORT = SecretConfig.PORT
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return connection.cursor()


def create_table():
    """
    Creates  table if it does not exist
    """
    sql = ""
    with open("../sql/create-payment.sql", "r") as f:
        sql = f.read()

    cursor = get_cursor()

    try:
        cursor.execute(sql)
        cursor.connection.commit()
    except:
        # Table already exists
        cursor.connection.rollback()


def delete_table():
    """
    Deletes the table completely and all its data
    """
    sql = "DROP TABLE payment_plans;"
    cursor = get_cursor()
    cursor.execute(sql)
    cursor.connection.commit()


def delete_all_rows():
    """
    Deletes all the rows of the table
    """
    sql = "DELETE FROM payment_plans"
    cursor = get_cursor()
    cursor.execute(sql)
    cursor.connection.commit()


def insert_payment_plan(card_number, purchase_amount, purchase_date, installments):
    """Inserts a payment plan in the database, where each row is an installment"""
    cursor = get_cursor()
    sql = f"""SELECT card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, 
    interest_rate FROM credit_cards WHERE card_number = '{card_number}'"""
    cursor.execute(sql)
    row = cursor.fetchone()

    if row is None:
        raise Exception(f"record with card number: {card_number} was not found")

    credit_card = CreditCard(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    payment_plan = PaymentPlan(card_number, purchase_date, purchase_amount)

    table = payment_plan.calc_payment_plan(credit_card, installments)
    print(table)
    for row in table:
        sql = f"""INSERT INTO payment_plans(
            Number, card_number, purchase_date, purchase_amount, payment_date, payment_amount, interest_amount,
            capital_amount, balance
            )
            VALUES(
                '{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}', '{row[8]}'
            );"""
        cursor.execute(sql)
    cursor.connection.commit()


def get_payment_plan():

    cursor = get_cursor()
    cursor.execute("""SELECT * FROM payment_plans""")
    payment_plan = cursor.fetchall()

    payment_plan_converted = [list(tuple) for tuple in payment_plan]  # Converts from list of tuples to list of lists
    return payment_plan_converted


def calc_total_payment_in_x_interval(initial_date: date, final_date: date):
    """Calculates the sum of the monthly payments in a specified range of months"""
    cursor = get_cursor()
    cursor.execute(f"""SELECT payment_amount FROM payment_plans WHERE payment_date >= '{initial_date}'
                        and payment_date <= '{final_date}'
                    """)
    amounts = cursor.fetchall()
    total: float = 0
    for amount in amounts:
        total += amount[0]

    return total
