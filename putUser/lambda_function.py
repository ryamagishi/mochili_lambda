import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,UserName,CognitoIdを取得
    print(str(event))
    body = event["Body"]
    userId = body["UserId"]
    userName = body["UserName"]
    cognitoId = event["CognitoId"]
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Usersテーブルのuserを更新
    result = {}
    try:
        usersTable = dynamodb.Table('Users')
        usersTable.update_item(
            Key={
                'UserId': userId
            },
            UpdateExpression='set UserName = :userName, updatedAt = :updatedAt',
            ConditionExpression='CognitoId = :cognitoId',
            ExpressionAttributeValues={
                ':userName': userName,
                ':updatedAt': updatedAt,
                ':cognitoId': cognitoId
            }
        )
        result = {"Status": "OK"}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result