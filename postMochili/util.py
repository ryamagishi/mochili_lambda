import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def checkUser(userId, cognitoId):
    # Usersテーブルよりuserを取得
    usersTable = dynamodb.Table('Users')
    usersResponse = usersTable.get_item(
        Key={
            'UserId': userId
        }
    )
    user = usersResponse['Item']

    # cognitoIdを比べて正しければtrueを返す
    if user['CognitoId'] == cognitoId:
        return True
    else:
        return False