import sys
import psycopg2
import SecretConfig
import Exemptionstop
from datetime import date
from Modelos.CreditCard import CreditCard



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
    with open("../sql/create-credit.sql", "r") as f:
        sql = f.read()

    cursor = get_cursor()

    try:
        cursor.execute(sql)
        cursor.connection.commit()
        print("Table created succesfully")
    except Exception as err:
        # Table already exists
        print(err)
        cursor.connection.rollback()


def delete_table():
    """
    Deletes the table completely and all its data
    """
    sql = "DROP TABLE credit_cards;"
    cursor = get_cursor()
    cursor.execute(sql)
    cursor.connection.commit()


def delete_all_rows():
    """
    Deletes all the rows of the table
    """
    sql = "DELETE FROM credit_cards"
    cursor = get_cursor()
    cursor.execute(sql)
    cursor.connection.commit()


def delete_single_credit_card(credit_card):
    """
    Deletes a single credit card from the table
    """
    sql = f"DELETE FROM credit_cards WHERE card_number = '{credit_card.card_number}'"
    cursor = get_cursor()
    cursor.execute(sql)
    cursor.connection.commit()


def insert_credit_card(credit_card: CreditCard):
    """Saves a credit_card in the database"""

    cursor = get_cursor()

    try:

        card_number_search = search_by_card_id(credit_card.card_number)

        if card_number_search is None:
            pass
        elif card_number_search.card_number == credit_card.card_number:
            print("RAISED ASJKJASFASF")
            raise Exemptionstop.CreditCardAlreadyExists
    except Exemptionstop.CardNotFoundError:
        pass
    except Exemptionstop.CreditCardAlreadyExists:
        raise Exemptionstop.CreditCardAlreadyExists

    try:

        cursor.execute(f"""
        INSERT INTO credit_cards (
            card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, interest_rate
        )
        VALUES
        (
            '{credit_card.card_number}', '{credit_card.owner_id}', '{credit_card.owner_name}', 
            '{credit_card.bank_name}', '{credit_card.due_date}', '{credit_card.franchise}', {credit_card.payment_day},
            '{credit_card.monthly_fee}', '{credit_card.interest_rate}'
        );
                        """)

        cursor.connection.commit()
        print("Credit card saved succesfully")
    except Exception as err:
        print(err)
        cursor.connection.rollback()


def search_by_card_id(card_number):
    cursor = get_cursor()
    cursor.execute(f"""SELECT card_number,owner_id,owner_name,bank_name,due_date,franchise,payment_day,monthly_fee,interest_rate FROM credit_cards where card_number = '{card_number}'""")
    row = cursor.fetchone()

    if row is None:
        raise Exemptionstop.CardNotFoundError

    result = CreditCard(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    return result

