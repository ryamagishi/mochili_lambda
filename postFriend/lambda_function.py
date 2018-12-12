import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,FriendId,CognitoIdを取得
    body = event["Body"]
    userId = body["UserId"]
    friendId = body["FriendId"]
    cognitoId = event["CognitoId"]
    createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Friendsテーブルにfriendを登録
    result = {}

    # checkUser
    if not (util.checkUser(userId, cognitoId)):
        return {}

    try:
        friendsTable = dynamodb.Table('Friends')
        friendsTable.put_item(
            Item={
                "UserId": userId,
                "FriendId": friendId,
                "CreatedAt": createdAt,
                "UpdatedAt": updatedAt
            },
            ConditionExpression=
            'attribute_not_exists(UserId) AND attribute_not_exists(FriendId)'
        )
        result = {"Status": "OK"}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result