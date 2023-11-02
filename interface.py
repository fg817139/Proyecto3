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

if __name__=='__main__':
   interface.run(debug=True)