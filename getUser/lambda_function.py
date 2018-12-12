import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


# 暫定的に存在するかしないかを返す関数とする
def lambda_handler(event, context):
    # 送られてくるUserIdを取得
    user_id = event["UserId"]

    # Usersテーブルよりuserを取得
    users_table = dynamodb.Table('Users')
    users_response = users_table.get_item(
        Key={
            'UserId': user_id
        }
    )
    # UserIdとUserNameのみ入れて返す
    return_user = {}
    if 'Item' in users_response:
        user = users_response['Item']
        return_user = {'UserId': user['UserId'], 'UserName': user['UserName']}

    return return_user
