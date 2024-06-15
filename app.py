from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)

# In-memory storage for receipts and points
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts[receipt_id] = points
    return jsonify({"id": receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        return jsonify({"points": receipts[receipt_id]})
    return jsonify({"error": "Receipt not found"}), 404

def calculate_points(receipt):
    points = 0
    retailer = receipt['retailer']
    purchase_date = receipt['purchaseDate']
    purchase_time = receipt['purchaseTime']
    total = float(receipt['total'])
    items = receipt['items']

    # 1 point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in retailer)

    # 50 points if the total is a round dollar amount with no cents
    if total.is_integer():
        points += 50

    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    points += (len(items) // 2) * 5

    # Points for item description length and price
    for item in items:
        description = item['shortDescription'].strip()
        price = float(item['price'])
        if len(description) % 3 == 0:
            points += math.ceil(price * 0.2)

    # 6 points if the day in the purchase date is odd
    day = int(purchase_date.split('-')[2])
    if day % 2 != 0:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    hour = int(purchase_time.split(':')[0])
    minute = int(purchase_time.split(':')[1])
    if 14 <= hour < 16:
        points += 10

    return points

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
