from flask import Flask, request, jsonify, send_from_directory
import json
from rulesr import (
    latest_financial_index,
    total_revenue,
    total_borrowing,
    iscr_flag,
    total_revenue_5cr_flag,
    borrowing_to_revenue_flag
)
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('./templates', 'upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        data = json.load(file)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    financial_index = latest_financial_index(data)

    if financial_index == -1:
        return jsonify({'error': 'No STANDALONE financial data found'}), 404

    total_revenue_value = total_revenue(data, financial_index)
    borrowing_to_revenue_ratio = total_borrowing(data, financial_index) / total_revenue_value if total_revenue_value != 0 else 0

    response = {
        'Index': financial_index,
        'Total Revenue': total_revenue_value,
        'Total Borrowing to Revenue Ratio': borrowing_to_revenue_ratio,
        'ISCR Flag': iscr_flag(data, financial_index),
        'Total Revenue 5cr Flag': total_revenue_5cr_flag(data, financial_index),
        'Borrowing to Revenue Flag': borrowing_to_revenue_flag(data, financial_index)
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
