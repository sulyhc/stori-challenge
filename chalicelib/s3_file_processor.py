import os
import boto3
import codecs
import csv
from .txns_process import TxnsProcess


def process_csv_file(s3_path_file):

    source_client = boto3.client('s3')

    contents = source_client.get_object(
        Bucket=os.environ['S3_TXNS_BUCKET'],
        Key=s3_path_file
    )

    list_txns = []

    counter = 0

    for line in csv.DictReader(codecs.getreader("utf-8")(contents["Body"])):

        list_txns.append(line)

        counter += 1

        if counter == 100:
            counter = 0
            TxnsProcess(None).process_txns_list(list_txns)(list_txns)
            list_txns = []

    if len(list_txns) > 0:
        TxnsProcess(None).process_txns_list(list_txns)(list_txns)
        list_txns=[]

    return True