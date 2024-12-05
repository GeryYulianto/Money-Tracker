from flask_app import FlaskApp
from flask import *
from database.database import query_db
from flask_session import Session

class WorkSpaceFeatures(FlaskApp):
    def __init__(self, app):
        super().__init__(app)
    
    def transactions(self):
        if request.method == 'GET':
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            query = '''
                SELECT * FROM transactions
                WHERE username = ?
            '''
            params = [session.get('username')] if session.get('username') else ['admin']

            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)

            transactions = query_db(query, params)
            print(query, params)

            transactions_list = [dict(row) for row in transactions]

            return jsonify(transactions_list)
        elif request.method == 'POST':
            try:
                data = request.json
                category_id = data.get('category_id')
                date = data.get('date')
                amount = data.get('amount')
                username = session.get('username')
                description = data.get('description')

                query_db('''
                    INSERT INTO transactions (category_id, date, amount, username, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', (category_id, date, amount, username, description))

                return jsonify('Success'), 200
            except:
                return jsonify('Failed'), 400
            
    
    def category(self):
        utilities = request.args.get('utilities')
        education = request.args.get('education')
        entertainment = request.args.get('entertainment')
        food = request.args.get('food')
        health = request.args.get('health')

        query = '''
            SELECT * FROM category
            '''

        params = []
        if utilities:
            params.append(1)
        if education:
            params.append(2)
        if entertainment:
            params.append(3)
        if food:
            params.append(4)
        if health:
            params.append(5)

        if params:
            placeholders = ','.join(['?'] * len(params))
            query += f' WHERE category_id IN ({placeholders})'

        categories = query_db(query, params)
        category_list = [dict(row) for row in categories]

        return jsonify(category_list)
        

    def add_workspace_endpoints(self):
        self.add_endpoint('/transactions', 'transactions', self.transactions, ['GET', 'POST'])
        self.add_endpoint('/category', 'category', self.category, ['GET'])