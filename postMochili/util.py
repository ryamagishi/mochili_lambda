import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def check_user(user_id, cognito_id):
    # Usersテーブルよりuserを取得
    users_table = dynamodb.Table('Users')
    users_response = users_table.get_item(
        Key={
            'UserId': user_id
        }
    )
    user = users_response['Item']

    # cognitoIdを比べて正しければtrueを返す
    if user['CognitoId'] == cognito_id:
        return True
    else:
        return False