from marshmallow import Schema, fields, pre_load
import re


class TxnSchema(Schema):
    txn_id = fields.Integer(data_key='id')
    txn_amount = fields.Float()
    txn_date = fields.DateTime(data_key='date')
    txn_type = fields.Integer()

    @pre_load
    def process_amounts(self, data, **kwargs):

        data['txn_type'] = 1

        str_type_txn = data['amount'][0]

        if str_type_txn == '-':
            data['txn_type'] = 2

        data['txn_amount'] = float(re.sub("[^0-9^.]", "", data["amount"]))

        data.pop('amount')

        return data
