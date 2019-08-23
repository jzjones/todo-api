import { CognitoUserPoolEvent } from 'aws-lambda';

export default async (event: CognitoUserPoolEvent) => {
  event.response.autoConfirmUser = true;
  return event;
};