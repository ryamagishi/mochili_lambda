import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,UserName,CognitoIdを取得
    print(str(event))
    body = event["Body"]
    user_id = body["UserId"]
    user_name = body["UserName"]
    cognito_id = event["CognitoId"]
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Usersテーブルのuserを更新
    result = {}
    try:
        users_table = dynamodb.Table('Users')
        users_table.update_item(
            Key={
                'UserId': user_id
            },
            UpdateExpression='set UserName = :userName, updatedAt = :updatedAt',
            ConditionExpression='CognitoId = :cognitoId',
            ExpressionAttributeValues={
                ':userName': user_name,
                ':updatedAt': updated_at,
                ':cognitoId': cognito_id
            }
        )
        result = {"Status": "OK"}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result