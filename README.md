# Email Service

## Description

Create a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

Example Email Providers:

SendGrid - Simple Send Documentation

Mailgun - Simple Send Documentation

## Implementation

This repo is divided into 2 main directories: src and test.

src/ contains the implementation of 'email-service'.

test/ consists of two test scripts.
The test script runs the server with the provided configuration (config.py). The test data to be sent is stored in test/data. Each json file is an email. The expected result for each test case is stored in test/expected. test/log stores the logfiles generated after executing each test case.

The test-service.sh consists of multiple calls of the script, test.sh. In test-service.sh, we start the server and run multiple test cases. We also pass the service provider we want to use here. In case of blank or default, as a service provider, the service provider mentioned in config.py is used as defauly. 

## Running

Initializing steps:

```
cd email-service
virtualenv flask
source flask/bin/activate
pip install flask
```

To run the server:

```
python src/main.py
```

To run the test cases:

```
cd test
sh test/test-service.sh
```