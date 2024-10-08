from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)

transactions = [] #global transactions list
balances = defaultdict(int) #global balances dictionary 

@app.route('/add', methods=['POST'])
def add_points():
    data = request.get_json()
    payer = data['payer']
    points = data['points']
    #strip and convert timestamp string into a datetime object
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    
    #adding transactions to global transactions list
    transactions.append({
        "payer": payer,
        "points": points,
        "timestamp": timestamp
    })
    
    #Update balance to add the points under the payer's acc
    balances[payer] += points
    return 'Success', 200

@app.route('/spend', methods=['POST'])
def spend_points():
    global balances #get the global balances dictionary
    balance = defaultdict(int) #imitate balance over time
    data = request.get_json()
    #format will be {"points" : 5000}
    points_to_spend = data['points']
    
    #Make sure user has enough points, cant go negative
    total_points = sum(balances.values())
    if points_to_spend > total_points:
        return "The user doesn't have enough points", 400
    
    #Sort transactions by oldest time -> most recent
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])
    
    #Start spending points from the oldest transactions
    points_spent = defaultdict(int)
    for transaction in sorted_transactions:
        payer = transaction['payer']
        points = transaction["points"]
        balance[payer] += points
        #if no points to spend remain, just add the curr transaction points to
        #the payer's balance in the balance dict
        #if the points in this transaction is 0, just continue
        if points_to_spend == 0 or points <= 0:
            continue
        
        elif balance[payer] < 0:  # Skip any transactions that are negative or zero
            #need to give points back, it went negative
         
            points_to_spend += abs(balance[payer])
            points_spent[payer] += abs(balance[payer])
            balance[payer] = 0

        elif points_to_spend >= points:
            #Spend all points from this transaction
            points_spent[payer] -= points 
            balance[payer] -= points
            points_to_spend -= points
        else:
            #Spend only part of the points
            points_spent[payer] -= points_to_spend
            balance[payer] -= points_to_spend
            points_to_spend = 0

    balances = balance #set the global balances dictionary to the new one we
    #just populated
   
    return jsonify(points_spent), 200 #return json response of points spent

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balances), 200 #return json response of balances dict

if __name__ == '__main__':
    app.run(port=8000, debug=True)
