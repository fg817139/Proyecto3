from datetime import date
import Exemptionstop
from dataclasses import dataclass

MAXANUALINTEREST = 100

@dataclass()
class CreditCard:

    card_number: str
    owner_id: str
    owner_name: str
    bank_name: str
    due_date: date
    franchise: str
    payment_day: int
    monthly_fee: float
    interest_rate: float

    def __init__(self, card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee,
                 interest_rate):
        self.card_number: int = card_number
        self.owner_id: int = owner_id
        self.owner_name: str = owner_name
        self.bank_name: str = bank_name
        self.due_date: date = due_date
        self.franchise: str = franchise
        self.payment_day: int = payment_day
        self.monthly_fee: float = monthly_fee
        self.interest_rate: float = interest_rate
        self.ANUALINTEREST = self.interest_rate * 12
        self.interest_percentage = self.interest_rate/100

    def calc_monthly_payment(self, amount: float, installments: int) -> float:

        if amount == 0:
            raise Exemptionstop.ZeroAmountError
        elif installments <= 0:
            raise Exemptionstop.NegativeNumberOfPaymentsError
        if self.interest_rate == 0:
            return amount / installments
        if installments == 1:
            return amount
        else:
            return round((amount * self.interest_percentage)/(1 - (1 + self.interest_percentage)**(-installments)), 4)

    def calc_total_interest(self, amount: float, installments: int) -> float:

        payment_value: float = self.calc_monthly_payment(amount, installments)
        total_interest: float = round((payment_value * installments) - amount, 2)
        return total_interest

    def calc_planned_saving(self, monthly_amount: float, total_amount: float) -> int:

        total_interest: float = 0
        subtotal: float = 0
        payment_number: int = 0
        while subtotal < total_amount:
            payment_number += 1
            subtotal += round(monthly_amount + total_interest, 4)
            total_interest = round(self.interest_percentage * subtotal, 4)
            print(payment_number)
            if subtotal >= total_amount:
                return payment_number