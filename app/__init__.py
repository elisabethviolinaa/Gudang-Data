import sys
import os

#supaya dapat mengimport beberapa hal di bawah ini -> untuk baca filenya 
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for
from models import db, DateDimension, ProductDimension, StoreDimension, CashierDimension, PromotionDimension, PaymentMethodDimension, TravellerShopperDimension, RetailSalesFact

app = Flask(__name__)
from import_data import scheduler

app.secret_key = 'Gudang_Data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/gudang_data_test' #bisa diganti dengan database yang kalian pakai 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#untuk routingnya
@app.route('/')
def display_chart():
    store_dimension = StoreDimension.query.all()
    product_dimension = ProductDimension.query.all()
    return render_template('index.html', store_dimension=store_dimension, product_dimension=product_dimension)

@app.route('/fact-table')
def display_fact_table():
    retail_sales_facts = RetailSalesFact.query.all()
    return render_template('fact_table.html', retail_sales_facts = retail_sales_facts)

@app.route('/promotions')
def display_promotions():
    promotion_dimension = PromotionDimension.query.all()
    retail_sales_facts = RetailSalesFact.query.all()
    product_dimension = ProductDimension.query.all()
    return render_template('promotions.html', promotion_dimension=promotion_dimension, retail_sales_facts=retail_sales_facts, product_dimension=product_dimension)

@app.route('/query_gross_profit')
def query_gross_profit():
    results = RetailSalesFact.query.filter(
    RetailSalesFact.store_key == "2123",
    RetailSalesFact.date_key == "2023-11-02",
    RetailSalesFact.product_key == "1035453804963260181506960"
    ).with_entities(RetailSalesFact.extended_gross_profit_dollar_amount).all()
    for a in results:
        print(a[0])

    return "Done"

@app.route('/gross_margin')
def gross_margin():
    store_key = "2123"
    date_key = "2023-11-02"
    product_key = "1035453804963260181506960"

    query = RetailSalesFact.query.filter(
        RetailSalesFact.store_key == store_key,
        RetailSalesFact.date_key == date_key,
        RetailSalesFact.product_key == product_key
    )

    results = query.with_entities(RetailSalesFact.extended_sales_dollar_amount, RetailSalesFact.extended_cost_dollar_amount).all()

    total_sales = sum(result[0] for result in results)
    total_cost = sum(result[1] for result in results)

    gross_margin = total_sales - total_cost

    return f"Gross Margin for Store {store_key}, Date {date_key}, Product {product_key}: ${gross_margin:.2f}"

