import os
from chalice import Chalice
from chalicelib.s3_file_processor import process_csv_file

app = Chalice(app_name='txn_test')


@app.on_s3_event(bucket=os.environ['S3_TXNS_BUCKET'],
                 events=['s3:ObjectCreated:*'],
                 prefix=os.environ['FOLDER_ACTION'],
                 suffix='.csv')
def read_csv_and_send(event):

    app.log.debug("Received event for bucket: %s, key: %s",
                  event.bucket, event.key)
    # TODO implement
    file_received_path = event.key

    process_csv_file(file_received_path)

    # send data to SQS

    print("success")