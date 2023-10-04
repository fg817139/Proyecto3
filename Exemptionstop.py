class ZeroAmountError(Exception):
    print("The amount must be greater than zero")


class NegativeNumberOfPaymentsError(Exception):
    print("The number of installments must be greater than zero")


class CardNotFoundError(Exception):
    print("The indicated card does not exist")


class CreditCardAlreadyExists(Exception):
    print("The credit card already exists")