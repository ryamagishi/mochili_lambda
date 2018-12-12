import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,UserName,CognitoIdを取得
    body = event["Body"]
    user_id = body["UserId"]
    user_name = body["UserName"]
    cognito_id = event["CognitoId"]
    password = body["Password"]
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Usersテーブルにuserを登録
    result = {}
    try:
        users_table = dynamodb.Table('Users')
        users_table.put_item(
            Item={
                "UserId": user_id,
                "UserName": user_name,
                "CognitoId": cognito_id,
                "Password": password,
                "CreatedAt": created_at,
                "UpdatedAt": updated_at
            },
            ConditionExpression='attribute_not_exists(UserId)'
        )
        result = {"Status": "OK"}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result