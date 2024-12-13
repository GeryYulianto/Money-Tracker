from flask import *
from database.database import query_db, insert_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions.jwt import JWT

class WorkSpaceFeatures:
    def __init__(self, app):
        self.app = app

    def add_workspace_endpoints(self):
        @self.app.route('/transactions', methods=['GET', 'POST', 'DELETE', 'PUT'])
        @jwt_required()
        def transactions():
            if request.method == 'GET':
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                query = '''
                    SELECT * FROM transactions
                    WHERE username = ?
                '''
                user = get_jwt_identity() 
                params = [user] if user else ['admin']

                if start_date != None and start_date != 'null':
                    print(start_date, 'aaaa')
                    query += ' AND date >= ?'
                    params.append(start_date)
                
                if end_date != None and end_date != 'null':
                    query += ' AND date <= ?'
                    params.append(end_date)

                transactions = query_db(query, params)

                transactions_list = [dict(row) for row in transactions]

                return jsonify(transactions_list)
            
            elif request.method == 'POST':
                try:
                    data = request.json
                    category_id = data.get('category_id')
                    date = data.get('date')
                    amount = data.get('amount')
                    username = get_jwt_identity()
                    description = data.get('description')

                    transaction_id = insert_db('''
                        INSERT INTO transactions (category_id, date, amount, username, description)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (category_id, date, amount, username, description))

                    return jsonify({"Message": "Success", "transaction_id": transaction_id}), 200
                except:
                    return jsonify('Failed'), 400
            elif request.method == 'DELETE':
                try:
                    data = request.json
                    username = get_jwt_identity()
                    transaction_id = data.get('transaction_id')
                    print(transaction_id)

                    query_db('DELETE FROM transactions WHERE transaction_id = ? AND username = ?', (transaction_id, username))
                    return jsonify('Delete Success'), 200
                except:
                    return jsonify('Failed'), 400
            elif request.method == 'PUT':
                try:
                    data = request.json
                    transaction_id = data.get('transaction_id')
                    category_id = data.get('category_id')
                    date = data.get('date')
                    amount = data.get('amount')
                    username = get_jwt_identity()
                    description = data.get('description')

                    query = ('''UPDATE transactions SET''')
                    params = []

                    if category_id:
                        query += ' category_id = ?,'
                        params.append(category_id)
                    
                    if date:
                        query += ' date = ?,'
                        params.append(date)
                    
                    if amount:
                        query += ' amount = ?,'
                        params.append(amount)
                    
                    if description:
                        query += ' description = ?'
                        params.append(description)
                    else:
                        query = query[:-1]
                    
                    query_db(query + ' WHERE transaction_id = ?', params + [transaction_id])

                    return jsonify('Update Success'), 200
                except Exception as e:
                    return jsonify(f'Failed Update, {e}'), 404




        
        @self.app.route('/category', methods=['GET'])
        @jwt_required()
        def category():
            utilities = request.args.get('Utilities')
            education = request.args.get('Education')
            entertainment = request.args.get('Entertainment')
            food = request.args.get('Food')
            health = request.args.get('Health')

            query = '''
                SELECT * FROM category
                '''

            params = []
            if utilities != None and utilities != 'null':
                params.append(1)
            if education != None and education!= 'null':
                params.append(2)
            if entertainment != None and entertainment != 'null':
                params.append(3)
            if food != None and food != 'null':
                params.append(4)
            if health != None and health != 'null':
                params.append(5)

            print(params)
            if params:
                placeholders = ','.join(['?'] * len(params))
                query += f' WHERE category_id IN ({placeholders})'

            categories = query_db(query, params)
            category_list = [{'id': row['category_id'], 'name': row['name'], 'class': row['class']} for row in categories]

            return jsonify(category_list)