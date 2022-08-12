from .txns_schema import TxnSchema
from .send_email import send_email


class TxnsProcess:

    def __init__(self, db_obj_conn=None):
        self.__db_obj = db_obj_conn


    def process_txns_list(self, txn_list: list) -> None:

        balances = {}

        self.__total_balance = 0.00
        self.__total_debit = 0.00
        self.__total_credit = 0.00
        self.__number_credit = 0
        self.__number_debit = 0

        for t in txn_list:
            obj_txn = TxnSchema().load(t)
            month = obj_txn['txn_date'].month

            if month not in balances:
                balances[month] = {
                    "credit": 0.00,
                    "debit": 0.00,
                    "number": 0
                }

            balance_type = "credit"

            if obj_txn['txn_type'] == 2:
                balance_type = "debit"
                self.__total_debit = self.__total_debit + obj_txn['txn_amount']
                self.__number_debit = self.__number_debit + 1

            else:
                self.__total_credit = self.__total_credit + obj_txn['txn_amount']
                self.__number_credit = self.__number_credit + 1

            balances[month][balance_type] = obj_txn['txn_amount'] + balances[month][balance_type]

            self.__total_balance = self.__total_balance + obj_txn['txn_amount']

            balances[month]["number"] = balances[month]["number"] + 1


        self.__avg_credit = self.__total_credit / self.__number_credit
        self.__avg_debit = self.__total_debit / self.__number_debit

        self.__save_balance(self, balances)

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


    def __send_email(self, balances_obj):

        body_message = "MEASURING:\nTOTAL BALANCE={total_balance}" \
                       "\nNumbers per months:{numbers_months}" \
                       "\nTOTALS:" \
                       "\nCredit :{numbers_c}"\
                       "\nDebit :{numbers_d}"\
                       "\nAvg per Credit :{avg_c}"\
                       "\nAvg per Debit :{avg_d}"

        keys_balances = balances_obj.keys()

        message_per_months = ""

        for k in keys_balances:

            message_per_months = message_per_months + "\n{month}: {numbers}".format(month=k, numbers=balances_obj[k]['number'])


        body_message = body_message.format(total_balance=self.__total_balance,
                                           numbers_months=message_per_months,
                                           numbers_c=self.__number_credit,
                                           numbers_d=self.__number_debit,
                                           avg_c=self.__avg_credit,
                                           avg_d=self.__avg_debit)

        send_email("Balance report", body_message)

        return True


