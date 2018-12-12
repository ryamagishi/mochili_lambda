import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId,mochiliMembers,CognitoIdを取得
    body = event["Body"]
    createrId = body["CreaterId"]
    mochiliName = body["MochiliName"]
    mochiliMembers = body["MochiliMembers"]
    cognitoId = event["CognitoId"]
    createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mochiliId = createrId + "--" + createdAt

    result = {}

    # checkUser
    if not (util.checkUser(createrId, cognitoId)):
        return {}

    try:
        # mochiliを登録
        mochilisTable = dynamodb.Table('Mochilis')
        mochilisTable.put_item(
            Item={
                "MochiliId": mochiliId,
                "MochiliName": mochiliName,
                "CreaterId": createrId,
                "UpdaterId": createrId,
                "CreatedAt": createdAt,
                "UpdatedAt": updatedAt
            },
            ConditionExpression=
            'attribute_not_exists(MochiliId)'
        )

        # mochiliSharesを登録
        mochiliSharesTable = dynamodb.Table('MochiliShares')
        for mochiliMemberId in mochiliMembers:
            mochiliSharesTable.put_item(
                Item={
                    "MochiliId": mochiliId,
                    "UserId": mochiliMemberId,
                    "CreatedAt": createdAt
                },
                ConditionExpression=
                'attribute_not_exists(MochiliId) AND attribute_not_exists(UserId)'
            )

        result = {"Status": "OK",
                  "Detail": mochiliId}
    except ClientError as clientError:
        result = {"Status": clientError.response['Error']['Code'],
                  "Detail": str(clientError)}

        # resultを返す
    return result