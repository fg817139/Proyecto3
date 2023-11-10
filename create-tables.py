from controlador import ControllerCreditCard,ControllerPaymentPlan

def create_tables():
    ControllerCreditCard.create_table()
    ControllerPaymentPlan.create_table()

create_tables()
