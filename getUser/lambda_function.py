import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


# 暫定的に存在するかしないかを返す関数とする
def lambda_handler(event, context):
    # 送られてくるUserIdを取得
    userId = event["UserId"]

    # Usersテーブルよりuserを取得
    usersTable = dynamodb.Table('Users')
    usersResponse = usersTable.get_item(
        Key={
            'UserId': userId
        }
    )
    # UserIdとUserNameのみ入れて返す
    returnUser = {}
    if 'Item' in usersResponse:
        user = usersResponse['Item']
        returnUser = {'UserId': user['UserId'], 'UserName': user['UserName']}

    return returnUser
