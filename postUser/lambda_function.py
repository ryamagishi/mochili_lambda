import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,UserName,CognitoIdを取得
    body = event["Body"]
    userId = body["UserId"]
    userName = body["UserName"]
    cognitoId = event["CognitoId"]
    password = body["Password"]
    createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Usersテーブルにuserを登録
    result = {}
    try:
        usersTable = dynamodb.Table('Users')
        usersTable.put_item(
            Item={
                "UserId": userId,
                "UserName": userName,
                "CognitoId": cognitoId,
                "Password": password,
                "CreatedAt": createdAt,
                "UpdatedAt": updatedAt
            },
            ConditionExpression='attribute_not_exists(UserId)'
        )
        result = {"Status": "OK"}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result