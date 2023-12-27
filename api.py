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

def execute_query(query, params=None):
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, params)
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return rows_affected
    except Exception as e:
        logging.error(f"Error executing query: {str(e)}")
        raise

def validate_input(info, required_fields):
    for field in required_fields:
        if field not in info:
            return False
    return True


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
    
@app.route("/customer", methods=["POST"])
def add_customers():
    try: 
        info = request.get_json()
        required_fields = ["first_name", "last_name", "middle_name", "gender", "email", "street_address", "city", "country"]
        
        if not validate_input(info, required_fields):
            return make_response(jsonify({"Error": "Missing required fields"}), 400)

        query = """INSERT INTO customers (first_name, last_name, middle_name, gender, email, street_address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (info["first_name"], info["last_name"], info["middle_name"], info["gender"], info["email"], info["street_address"], info["city"], info["country"])
        rows_affected = execute_query(query, params)
        return make_response(jsonify({"message": "customer added successfully", "rows_affected": rows_affected}), 201)
    except Exception as e:
        logging.error(f"Error in add_customers route: {str(e)}")
        return make_response(jsonify({"Error": "Internal server error"}), 500)

@app.route("/customer/<int:id>", methods=["PUT"])
def update_customer(id):
    try: 
        info = request.get_json()
        required_fields = ["first_name", "last_name", "middle_name", "gender", "email", "street_address", "city", "country"]

        if not validate_input(info, required_fields):
            return make_response(jsonify({"Error": "Missing required fields"}), 400)

        query = """UPDATE customers SET first_name = %s, last_name = %s, middle_name = %s, gender = %s, email = %s, street_address = %s, city = %s, country = %s WHERE customersid = %s"""
        params = (info["first_name"], info["last_name"], info["middle_name"], info["gender"], info["email"], info["street_address"], info["city"], info["country"], id)
        rows_affected = execute_query(query, params)
        return make_response(jsonify({"message": "customer updated successfully", "rows_affected": rows_affected}), 200)
    except Exception as e:
        logging.error(f"Error in update_customer route: {str(e)}")
        return make_response(jsonify({"Error": "Internal server error"}), 500)
    
@app.route("/customer/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try: 
        query = """DELETE FROM customers WHERE customersid = %s"""
        params = (id,)
        rows_affected = execute_query(query, params)
        return make_response(jsonify({"message": "customer deleted successfully", "rows_affected": rows_affected}), 200)
    except Exception as e:
        logging.error(f"Error in delete_customer route: {str(e)}")
        return make_response(jsonify({"Error": "Internal server error"}), 500)

if __name__ == "__main__":
    app.run(debug=True)
