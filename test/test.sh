#!/usr/bin/env sh

curl -H "Content-Type: application/json" --data @data/$1.json http://127.0.0.1:5000/email > log/$1_$2.log 2> /dev/null
if [[ -n "$(diff log/$1_$2.log expected/$1_$2.log)" ]]; then
  echo "FAIL: Test with $1.json via $2."
else
  rm log/$1_$2.log;
  echo "SUCCESS: Test with $1.json via $2 SUCCEEDED."
fi

#curl -s --user 'api:102c47a06833e57bee8f3cd36627bbe6-4de08e90-41ae02de' \
#	https://api.mailgun.net/v3/sandboxcbd0c7b41cac4c63bb2a9819c4bc534a/messages \
#	-F from='Excited User <mailgun@sandboxcbd0c7b41cac4c63bb2a9819c4bc534a.mailgun.org>' \
#	-F to=YOU@YOUR_DOMAIN_NAME \
#	-F to=rahul.shrestha@tum.de \
#	-F subject='Hello' \
#	-F text='Testing some Mailgun awesomeness!'
