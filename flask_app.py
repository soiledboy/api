from flask import Flask, json, render_template,jsonify
import psycopg2
from datetime import datetime, timedelta
from query import my_query

app = Flask(__name__)

@app.route("/")

@app.route("/privacy")
def about():
    return render_template("privacy.html")

@app.route('/prices/<string:productId>/<string:range>/<string:rarity>', methods=['GET'])
@app.route('/prices/<string:productId>/<string:range>', methods=['GET'])
def get_prices(productId, range, rarity = None):
    # Initialize the database connection
    conn = psycopg2.connect(
    dbname="d4glguq0as3fe6",
    user="ucjrvhda1pfbv1",
    password="pa045091d3e285537e8a31eb863c11df1dfa42659a9a447ce231b18f0070892a1",
    host="ec2-34-195-123-119.compute-1.amazonaws.com",
    port="5432"
    )

    cursor = conn.cursor()

    # Calculate the date range based on the input
    if range.isdigit() and int(range) >= 0:
        start_date = datetime.now() - timedelta(days=int(range))


    else:
        return jsonify({"error": "Invalid date range"}), 400


          # Modify your SQL query or its execution based on the presence of rarity.
    if rarity:
        cursor.execute(my_query, (productId, rarity, rarity, start_date, rarity, rarity))
    else:
        cursor.execute(my_query, (productId, None, None, start_date, None, None))


    rows = cursor.fetchall()
    cursor.close()

    if rows:
        # Extract column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows to list of dictionaries
        data = [dict(zip(column_names, row)) for row in rows]

        # Convert the list of dictionaries to a JSON string
        json_data = json.dumps(data, default=str)  # default=str is to handle date and other non-JSON serializable data types

        return json_data

    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run()
