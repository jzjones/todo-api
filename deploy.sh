#!/bin/bash

DEPLOYMENT_BUCKET=$1
aws s3 mb s3://$DEPLOYMENT_BUCKET

python yaml_compile.py .merge-template.yaml

sam build --use-container --template .merge-template.yaml

sam package --output-template-file packaged.yaml --s3-bucket $DEPLOYMENT_BUCKET
sam deploy --template-file packaged.yaml --stack-name todo-api-dev --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ParameterKey=DeploymentBucket,ParameterValue=s3://$DEPLOYMENT_BUCKET
