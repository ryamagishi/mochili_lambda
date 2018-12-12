import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,FriendId,CognitoIdを取得
    body = event["Body"]
    user_id = body["UserId"]
    friend_id = body["FriendId"]
    cognito_id = event["CognitoId"]
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Friendsテーブルにfriendを登録
    result = {}

    # checkUser
    if not (util.check_user(user_id, cognito_id)):
        return {}

    try:
        friends_table = dynamodb.Table('Friends')
        friends_table.put_item(
            Item={
                "UserId": user_id,
                "FriendId": friend_id,
                "CreatedAt": created_at,
                "UpdatedAt": updated_at
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