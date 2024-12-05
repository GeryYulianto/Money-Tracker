from flask_app import FlaskApp
from flask import *
from database.database import query_db
from flask_session import Session

class WorkSpaceFeatures(FlaskApp):
    def __init__(self, app):
        super().__init__(app)
    def get_transactions(self):
        transactions = query_db('''
            SELECT * FROM transactions
            WHERE username = ?
        ''', ('admin',))

        transactions_list = [dict(row) for row in transactions]

        return jsonify(transactions_list)
    
    def add_workspace_endpoints(self):
        self.add_endpoint('/transactions', 'transactions', self.get_transactions, ['GET'])