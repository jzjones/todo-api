#!/bin/bash
STACK_NAME=$1
DEPLOYMENT_BUCKET=$2
ENV=$3

ENV_FILE=.env.$ENV

aws s3 mb s3://$DEPLOYMENT_BUCKET

python yaml_compile.py .merge-template.yaml

ret=$?
if [ $ret -ne 0 ]; then
  echo "YAML compilation failed"
  exit
fi

ENV_VARS=""
if [ -s $ENV_FILE ]
then
  ENV_VARS=--parameter-overrides $(cat $ENV_FILE)
fi


sam build --use-container --template .merge-template.yaml

sam package --output-template-file packaged.yaml --s3-bucket $DEPLOYMENT_BUCKET
sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM $ENV_VARS

echo "UserPool: "
aws cloudformation describe-stacks --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPool`].OutputValue' \
    --output text

echo "UserPoolClient: "
aws cloudformation describe-stacks --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPoolClient`].OutputValue' \
    --output text
