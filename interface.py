from flask import Flask, render_template, request, jsonify

from controlador import ControllerCreditCard, ControllerPaymentPlan
from Modelos.CreditCard import CreditCard

from datetime import date

interface = Flask(__name__)


@interface.route("/")
def home():
   return render_template("index.html")


@interface.route("/interface/create-credit-card")
def create_cc():
   return render_template("create-credit-card.html")


@interface.route("/interface/simulate-purchase")
def simule_purchase():
   return render_template("simulate-purchase.html")



@interface.route("/interface/payment-plan")
def payment_plan():
   return render_template("payment-plan.html")



@interface.route("/interface/view-payments")
def view_pay():
   return render_template("view-payments.html")

@interface.route("/interface/delete_credit_card")
def delete_credit():
   return render_template("Delete_CreditCard.html")


#------------------------------------------------------------------------------------------------------------------

@interface.route('/interface/insert/credit-card')
def view_insert_credit_card():
   try:
      card_number = request.args["card_number"]
      owner_id = request.args["owner_id"]
      owner_name = request.args["owner_name"]
      bank_name = request.args["bank_name"]
      due_date = date.fromisoformat(request.args["due_date"])
      franchise = request.args["franchise"]
      payment_day = int(request.args["payment_day"])
      monthly_fee = float(request.args["monthly_fee"])
      interest_rate = float(request.args["interest_rate"])

      credit_card = CreditCard(card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day,
                               monthly_fee, interest_rate)

      ControllerCreditCard.insert_credit_card(credit_card)

      search_credit_card = ControllerCreditCard.search_by_card_id(card_number)

      result: str = f"Tarjeta de credito guardada exitosamente!"
      return result
   except Exception as err:
      return str(err)



@interface.route('/interface/insert/simulate-purchase')
def view_show_purchase():
   try:
      card_number = request.args["card_number"]
      purchase_amount = float(request.args["purchase_amount"])
      payments = int(request.args["payments"])

      search_credit_card = ControllerCreditCard.search_by_card_id(card_number)

      monthly_amount = CreditCard.calc_monthly_payment(search_credit_card, purchase_amount, payments)
      total_interest = CreditCard.calc_total_interest(search_credit_card, purchase_amount, payments)

      planned_saving = CreditCard.calc_planned_saving(search_credit_card, monthly_amount, purchase_amount)

      result: str = f"""
        Pago mensual: ${monthly_amount}... \n
        Interés total a pagar: ${total_interest}... \n

        Te sugerimos ahorrar por {planned_saving} meses para realizar la misma compra de contado.
        """
      return result

   except Exception as err:
      return str(err)



@interface.route('/interface/insert/payment-plan')
def insert_payment_plan():
   try:
      card_number = request.args["card_number"]
      purchase_amount = float(request.args["purchase_amount"])
      purchase_date = date.fromisoformat(request.args["purchase_date"])
      payments = int(request.args["payments"])

      ControllerPaymentPlan.insert_payment_plan(card_number, purchase_amount, purchase_date, payments)

      result: str = "Plan de amortización guardado exitosamente en la base de datos."

      return result

   except Exception as err:
      return str(err)



@interface.route("/interface/insert/view-payments")
def calc_payments():
   try:
      inintial_date = request.args["initial_date"]
      final_date = request.args["final_date"]

      total = ControllerPaymentPlan.calc_total_payment_in_x_interval(date.fromisoformat(inintial_date),
                                                                     date.fromisoformat(final_date))

      result: str = f"El total a pagar desde {inintial_date} hasta {final_date} es: ${total}"

      return result

   except Exception as err:
      return str(err)

@interface.route("/interface/insert/Delete_CreditCard")
def delete_credit_card():
   try:
      card_number = request.args["card_number"]
      # Verifica si la tarjeta existe antes de eliminarla
      if ControllerCreditCard.search_by_card_id(card_number):
         ControllerCreditCard.delete_credit_card(card_number)
         result = f"Tarjeta de crédito con número {card_number} eliminada exitosamente."
      else:
         result = f"No se encontró ninguna tarjeta de crédito con el número {card_number}."
      return result
   except Exception as err:
      return str(err)


if __name__=='__main__':
   interface.run(debug=True)