import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,mochiliMembers,CognitoIdを取得
    body = event["Body"]
    creater_id = body["CreaterId"]
    mochili_name = body["MochiliName"]
    mochili_members = body["MochiliMembers"]
    cognito_id = event["CognitoId"]
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mochili_id = creater_id + "--" + created_at

    result = {}

    # checkUser
    if not (util.check_user(creater_id, cognito_id)):
        return {}

    try:
        # mochiliを登録
        mochilis_table = dynamodb.Table('Mochilis')
        mochilis_table.put_item(
            Item={
                "MochiliId": mochili_id,
                "MochiliName": mochili_name,
                "CreaterId": creater_id,
                "UpdaterId": creater_id,
                "CreatedAt": created_at,
                "UpdatedAt": updated_at
            },
            ConditionExpression=
            'attribute_not_exists(MochiliId)'
        )

        # mochiliSharesを登録
        mochili_shares_table = dynamodb.Table('MochiliShares')
        for mochili_member_id in mochili_members:
            mochili_shares_table.put_item(
                Item={
                    "MochiliId": mochili_id,
                    "UserId": mochili_member_id,
                    "CreatedAt": created_at
                },
                ConditionExpression=
                'attribute_not_exists(MochiliId) AND attribute_not_exists(UserId)'
            )

        result = {"Status": "OK",
                  "Detail": mochili_id}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result