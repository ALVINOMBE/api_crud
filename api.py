from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
import logging

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "customers_and_job"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Setting up logging
logging.basicConfig(level=logging.ERROR)

def data_fetch(query, params=None):
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, params)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        logging.error(f"Error in data_fetch: {str(e)}")
        raise



@app.route("/customer")
def customers_data():
    try:
        query = """Select concat(customers.first_name, " ", customers.last_name) as FULLNAME, 
                        customers.gender,
                        customers.email,
                        customers.street_address,
                        customers.city,
                        customers.country,
                        jobs.date_job_started as "Job start" ,
                        jobs.date_job_complete as " Job complete",
                        invoices.total_cost,
                        invoices.invoice_date as "Invoice date" from customers
                        join jobs on customers.customersid = jobs.customers_customersid 
                        join invoices where jobs.jobid = invoices.jobs_jobid"""
        data = data_fetch(query)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logging.error(f"Error in customers_data route: {str(e)}")
        return make_response(jsonify({"Error": "Internal server error"}), 500)

@app.route("/customer/<int:id>")
def get_by_id(id):
    try:
        query = """SELECT 
                        CONCAT(customers.first_name, " ", customers.last_name) as FULLNAME, 
                        customers.gender,
                        customers.email,
                        customers.street_address,
                        customers.city,
                        customers.country,
                        jobs.date_job_started as "Job start" ,
                        jobs.date_job_complete as " Job complete",
                        invoices.total_cost,
                        invoices.invoice_date as "Invoice date" 
                    FROM customers
                    JOIN jobs ON customers.customersid = jobs.customers_customersid 
                    JOIN invoices ON jobs.jobid = invoices.jobs_jobid
                    WHERE customers.customersid = %s"""
        data = data_fetch(query, (id,))
        return make_response(jsonify(data), 200)
    except Exception as e:
        logging.error(f"Error in get_by_id route: {str(e)}")
        return make_response(jsonify({"Error": "Internal server error"}), 500)