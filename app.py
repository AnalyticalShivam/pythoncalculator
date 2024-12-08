from flask import Flask, request, jsonify, render_template
import nest_asyncio
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
nest_asyncio.apply()

# Allow CORS for your frontend (adjust origin if needed)
CORS(app, resources={r"/calculate": {"origins": "https://pythoncalculator-9icg94fpm3t6xipjt3ctqj.streamlit.app/"}})  # Adjust origin as needed

def calculate_loan_details(loan_amount, rate_of_interest, loan_tenure):
    # Convert annual interest rate to monthly and decimal
    monthly_rate = rate_of_interest / (12 * 100)
    tenure_months = loan_tenure * 12

    # EMI formula
    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)

    # Calculate total payment and total interest
    total_payment = emi * tenure_months
    total_interest = total_payment - loan_amount

    return {
        "monthly_emi": round(emi),
        "total_interest": round(total_interest),
        "total_payment": round(total_payment)
    }

@app.route('/')
def index():
    # Serve the HTML page for the graph
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    loan_amount = data['loan_amount']
    rate_of_interest = data['rate_of_interest']
    loan_tenure = data['loan_tenure']

    # Call the calculation function
    result = calculate_loan_details(loan_amount, rate_of_interest, loan_tenure)

    # Return the result as a JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
