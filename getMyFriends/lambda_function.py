import boto3
from boto3.dynamodb.conditions import Key, Attr
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId, CognitoIdを取得
    user_id = event['UserId']
    cognito_id = event['CognitoId']

    # checkUser
    if not (util.check_user(user_id, cognito_id)):
        return []

    # Friendsテーブルより友達のUserIdであるFriendIdを取得
    friends_table = dynamodb.Table('Friends')
    friends_response = friends_table.query(
        KeyConditionExpression=Key('UserId').eq(user_id)
    )

    # 取得したFriendIdよりUserテーブルから各User情報を取得
    users_table = dynamodb.Table('Users')
    friends = []
    for friend_item in friends_response['Items']:
        friend_id = friend_item['FriendId']
        user_response = users_table.get_item(
            Key={
                'UserId': friend_id
            }
        )
        # friendsのcreatedAt,updatedAtはFriendsテーブルデータより設定
        friend = {'FriendId': user_response['Item']['UserId'], 'FriendName': user_response['Item']['UserName'],
                  'CreatedAt': friend_item['CreatedAt'], 'UpdatedAt': friend_item['UpdatedAt']}
        friends.append(friend)

    # userの配列であるfriendsを返す
    return friends
