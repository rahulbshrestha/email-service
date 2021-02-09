import csv
import os.path
import requests
import sys
import json

from re import compile
from flask import Flask, views, request
from email.utils import formatdate
from time import strptime, strftime, gmtime
from calendar import timegm
from config import *

class EmailService(views.MethodView):
    
    ## The constructor
    #
    def __init__(self):     
        
        # Email providers
        self.providers = ['mailgun', 'sendgrid']
        
        # Host names of email providers
        self.hosts = {'mailgun' :
                      "https://api.mailgun.net/v3/sandboxcbd0c7b41cac4c63bb2a9819c4bc534a/messages",
                      'sendgrid' :
                      ""}

        # API Keys for each email provider
        self.APIkeys = {'mailgun' : "102c47a06833e57bee8f3cd36627bbe6-4de08e90-41ae02de",
                     'sendgrid': ""}

        # Fields composed in an email
        self.fields = ['to', 'to_name', 'from','from_name', 'subject', 'body']
    
        ## Function to send emails
    #
    def post(self):
        
        # Loading settings
        self.loadconfig()

        try:
            # Load email json file
            message = json.loads(request.data)

            # validate email
            valErr = self.validate(message)
            
            if valErr is not None:
                return valErr

            # send email
            return self.sendEmail(message)

        except Exception as e:
            return "Exception: {0}!\n".format(e)


    ## Function to verify if email server is still running
    #
    def get(self):
        return "Success: Email Server is running.\n"


    ## Load config file according to what was passed from the argument
    #
    def loadconfig(self):
        
        global config
        
        # Use json file if present
        #if len(sys.argv) >= 2:
        #    fconfig = open(sys.argv[1])
        #    config = json.load(fconfig)
        #    fconfig.close()

        # Pick email service provider
        if 'provider' in config.APIkeys() and config['provider'] in self.providers:
            self.provider = config['provider']
        else:
        # Default email service provider is picked (mailgun) 
            self.provider = self.providers[0]

    ## Function to validate email
    #
    def validate(self, message):
        
        error = ""

        # validate email addresses
        if not self.validateAddress(message['from']):
            error += "  From email address [{0}] is invalid\n".format(message['from'])

        # send back the error message if validation fails
        if error != "":
            return "Invalid email:\n" + error

        return None

    ## Function to check if email address is valid
    #  Should be "[alphanumeric|.]+@[alphanumeric]+(.[alphanumeric]+)"
    #
    def validateAddress(self, addr):
        emailPattern = compile(r'[\w.]+@[\w]+([.][\w]+)+$')
        return (emailPattern.match(addr) is not None)


    ## Function to send email through provider based on config (if not, error responses) 
    #
    def sendEmail(self, message):
        # number of retries if email sending fails on both service providers
        if 'retries' in config.APIkeys():
            retries = config['retries']
        else:
            retries = 1

        # retry if providers fail
        for i in range(len(self.providers) * retries):
            sent = self.sendByProvider(message, self.provider)
            if sent is None:
                return "Success! Email sent: {0}!\n"\
                       .format(self.provider)
            else:
                # Pick next provider from list of providers
                currIndex = self.providers.index(self.provider)
                #self.provider = self.providers[(currIndex+1) % len(self.providers)]
        
        # sent is the error message
        return sent

   
    ## Function to send email through provider
    #
    def sendByProvider(self, message, provider):
        # post an email send request to the provider
        try:
            # send email through mailgun
            if provider == 'mailgun':
                reply = requests.post(
                         self.hosts[provider],
                         auth = ('api', self.APIkeys[provider]),
                         data = self.mailgunData(message))
            # TODO: else, send email through another provider

            if reply.status_code != 200: # Code 200 means succesful delivery
                return "Sending email via {0} failed with status code:"\
                       " [{1}]\n".format(provider, reply.status_code)

        except Exception as e:
            return "ERROR: Mail provder error {0}\n".format(e)

        return None

    ## Function to extract data from messsage for mailgun
    #
    def mailgunData(self, message):
        data = {'from': "{0} <{1}>".format(message['from_name'],
                                              message['from']),
                   'to': ["{0} <{1}>".format(message['to_name'],
                                             message['to'])],
                   'subject': message['subject'],
                   'text': message['body']}

        return data


if __name__ == '__main__':
    
    app = Flask(__name__)
    
    # add an email service
    app.add_url_rule('/email', view_func=EmailService.as_view("email server"))

    # run the service
    app.run()
