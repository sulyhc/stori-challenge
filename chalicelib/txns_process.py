from .txns_schema import TxnSchema


class TxnsProcess:

    def __init__(self, db_obj_conn=None):
        self.__db_obj = db_obj_conn

    @classmethod
    def process_txns_list(cls, txn_list: list) -> None:

        balances = {}

        for t in txn_list:
            obj_txn = TxnSchema().load(t)
            month = obj_txn['txn_date'].month

            if month not in balances:
                balances[month] = {
                    "credit": 0.00,
                    "debit": 0.00
                }

            balance_type = "credit"

            if obj_txn['txn_type'] == 2:
                balance_type = "debit"

            balances[month][balance_type] = obj_txn['txn_amount'] + balances[month][balance_type]

        print(balances)

        cls.__save_balance(cls, balances)

        return None

    def __save_balance(self, balances_obj) -> bool:

        if not self.__db_obj:
            return False

        keys_balances = balances_obj.keys()

        query = """INSERT INTO balances(balance_month, balance_credit_amount,balance_debit_amount,created_at)
                    VALUES """

        subquery = ""

        for k in keys_balances:
            subquery = subquery + "({balance_month}, {balance_credit_amount}," \
                                  "{balance_debit_amount},now()),".format(balance_month=k,
                                                                          balance_credit_amount=balances_obj[k][
                                                                              'credit'],
                                                                          balance_debit_amount=balances_obj[k]['debit'])

        query = query + subquery[:-1]

        print(query)

        cursor = self.__db_obj.cursor()

        cursor.execute(query)

        cursor.commit()

        self.__db_obj.commit()

        self.__db_obj.close()

        return True
