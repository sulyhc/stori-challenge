# Stori Challenge

This is the project for solve the Stori challenge


## Installation

For use this project you will need the follow dependencies:

* python 3.9+
* pip 3
* virtualenv
* git

You must copy the config.json.example as config.json inside the txn_test/.chalice

## Install dependences

```bash
cd txn_test
pip install -r requirements.txt
```

## deploy to aws

```bash
chalice deploy --stage=dev
```

## Csv document format
```bash
id,date,amount
1,2022-12-03 14:05:00,+1500.00
2,2022-12-03 14:05:00,-150.00
3,2022-12-03 14:05:00,+500.00
```
date must in english format
 
